import traceback
from typing import List, Optional, Union
from urllib.parse import urlparse
import urllib.parse
import datetime
import boto3
from botocore.config import Config
from botocore.errorfactory import ClientError
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from shared.external_services.attachments.attachment import AttachmentStorageService
from shared.external_services.attachments.exceptions import *
from shared.log.cylog import CyLog
from shared.utils.app import now


class DOAttachmentService(AttachmentStorageService):
    def __init__(self, access_key: str = settings.DO_SPACES_ACCESS_KEY, secret_key: str = settings.DO_SPACES_SECRET_KEY,
                 endpoint_url: str = settings.DO_SPACES_ENDPOINT_URL):
        super(DOAttachmentService, self).__init__(access_key, secret_key, endpoint_url)
        self.spaces_client = boto3.client(
            's3',
            region_name=settings.DO_SPACES_REGION_NAME,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': "virtual"}
            )
        )

    @classmethod
    def validate_url(cls, attachment_url: str) -> Union[str, bool]:
        url_validator = URLValidator(schemes=['http', 'https'])
        try:
            url_validator(attachment_url)
            return attachment_url
        except ValidationError:
            return False

    @classmethod
    def get_file_path(cls, attachment_url: str) -> str:
        """
        GEt key from DO Spaces attachment url
        :param attachment_url: (str) DO Spaces Attachment url
        :return: key file
        """
        parse_object = urlparse(attachment_url)
        parse_path = parse_object.path
        # Remove first character (/)
        if parse_path.startswith("/"):
            parse_path = parse_path[1:]
        return parse_path

    def check_file_exist(self, file_path: str, source: str = None) -> bool:
        """
        Check the file path exists or not
        :param file_path: (str) DO Spaces key
        :param source: (str) DO Spaces bucket name
        :return: True if the file exists otherwise return Fales
        """
        try:
            self.spaces_client.head_object(Bucket=source, Key=file_path)
            return True
        except ClientError:
            # Not found file
            return False

    def get_file_size(self, file_path: str, source: str = None) -> Optional[float]:
        """
        Get DO Spaces file size
        :param file_path: (str) DO Spaces file path
        :param source: (str) DO Spaces bucket name
        :return: Size of file if the file exists
        """
        try:
            response = self.spaces_client.head_object(Bucket=source, Key=file_path)
            return response['ContentLength']
        except ClientError:
            return None

    def generate_upload_form(self, upload_file_path: str, destination: str = settings.DO_SPACES_BUCKET, **metadata):
        """
        Crete new pre-signed upload url for the client
        :param upload_file_path:
        :param destination: (str) Destination DO Space bucket name
        :param metadata:
        :return:
        """
        acl = metadata.get("acl", "private")
        if acl and acl not in ["private", "public-read"]:
            raise AttachmentACLException

        fields = {"success_action_status": "201", "acl": acl}
        conditions = [
            {"success_action_status": "201"},
            {"acl": acl}
        ]

        content_type = metadata.get("content_type")         # File content type
        limit = metadata.get("limit")                       # Limit size
        if content_type:
            fields.update({"Content-Type": content_type})
            conditions.append({"Content-Type": content_type})
        if limit and isinstance(limit, int) and limit > 0:
            conditions.append(["content-length-range", 0, limit])

        try:
            response = self.spaces_client.generate_presigned_post(
                Bucket=destination,
                Key=upload_file_path,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=600
            )
            return response
        except (ClientError, Exception):
            tb = traceback.format_exc()
            CyLog.warning(**{"message": "Exception generate_upload_form: {}".format(tb)})
            raise AttachmentCreateUploadFormException

    def copy_file(self, old_file_path: str, new_file_path: str,
                  source: str = settings.DO_SPACES_BUCKET, destination: str = settings.DO_SPACES_BUCKET,
                  **metadata) -> str:
        """
        Copy DO Spaces attachment
        :param old_file_path: (str) The old file path
        :param new_file_path: (str) The new file path
        :param source: (str) Source bucket
        :param destination: (str) Destination bucket
        :param metadata:
        :return:
        """
        try:
            acl = metadata.get("acl", "private")
            if acl and acl not in ["private", "public-read"]:
                raise AttachmentACLException
            copy_source = {
                'Bucket': source,
                'Key': old_file_path
            }
            extra_args = {'ACL': acl}
            self.spaces_client.meta.client.copy(copy_source, destination, new_file_path, extra_args)
            return new_file_path
        except (ClientError, Exception):
            raise AttachmentCopyException

    def delete_files(self, file_paths: List[str], source: str = None) -> bool:
        """
        Delete multiple DO Spaces files
        :param file_paths: (list) List DO Spaces key files
        :param source: (str) Bucket source
        :return:
        """
        for file_path in file_paths:
            if not file_path or not file_path.strip():
                continue
            try:
                self.spaces_client.delete_object(Bucket=source, Key=file_path)
            except ClientError:
                continue
        return True

    def delete_prefix(self, prefix: str, source: str = settings.DO_SPACES_BUCKET) -> bool:
        """
        Delete a DO Spaces prefix
        :param prefix: (str) specific dir
        :param source: (str) DO Space bucket name
        :return:
        """
        try:
            s3 = boto3.resource(
                's3',
                region_name=settings.DO_SPACES_REGION_NAME,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                config=Config(
                    signature_version='s3v4',
                    s3={'addressing_style': "virtual"}
                )
            )
            bucket = s3.Bucket(source)
            bucket.objects.filter(Prefix=prefix).delete()
            return True
        except ClientError:
            return False

    def list_files(self, prefix: str, source: str = settings.DO_SPACES_BUCKET,
                   max_keys: int = 1000, marker: str = '', filter_type: str = None) -> tuple:
        """
        Get list files by prefix
        :param prefix: (str) specific dir
        :param source: (str) DO Spaces bucket name
        :param max_keys: (int) The maximum number of keys returned in the response
        :param marker: (str) Marker is where we want DO Spaces to start listing from. DO Spaces starts listing after it
        :param filter_type: (str) Filter type param
        :return: (tuple) is_truncated, next_marker, keys
        """
        # if not prefix.endswith("/"):
        #     prefix = prefix + "/"
        try:
            list_objects = self.spaces_client.list_objects(
                Bucket=source, Prefix=prefix, Delimiter="/", MaxKeys=max_keys, Marker=marker
            )
            is_truncated = list_objects.get("IsTruncated")
            next_marker = list_objects.get("NextMarker")
            keys_content = list_objects.get("Contents", [])
            keys = [key_content.get("Key") for key_content in keys_content]

            # Filter keys
            filter_keys = keys
            if filter_type == "image":
                extensions = [".png", ".jpg", ".jpeg", ".webp", ".gif"]
                filter_keys = [key for key in keys if key.lower().endswith(tuple(extensions))]
            elif filter_type == "file":
                extensions = [".png", ".jpg", ".jpeg", ".webp", ".gif"]
                filter_keys = [key for key in keys if not key.lower().endswith(tuple(extensions))]

            # If response does not include the NextMarker and it is truncated, we can use the value of the last Key
            # in the response as the marker in the subsequent request to get the next set of object keys.
            if is_truncated is True and next_marker is None and len(keys) > 0:
                next_marker = keys[-1]
            return is_truncated, next_marker, filter_keys
        except ClientError:
            tb = traceback.format_exc()
            CyLog.warning(**{"message": "Exception generate_upload_form: {}".format(tb)})
            raise AttachmentListObjectsException

    def generate_onetime_url(self, file_path: str, is_cdn=False, source: str = settings.DO_SPACES_BUCKET, **kwargs) -> str:
        """
        Generate onetime url to access DO Spaces private file
        :param file_path: (str) DO Spaces key
        :param is_cdn: (str) Access via CDN url
        :param source: (str) Bucket name
        :param kwargs: (dict) {expired: 60, response_content_disposition: 'inline'}
        :return: Onetime url
        """
        if is_cdn:
            expired = kwargs.get("expired", 60)
            expire_date = datetime.datetime.utcfromtimestamp(now() + expired)  # 1 minute
            cloudfront_signer = CloudFrontSigner(settings.AWS_CLOUDFRONT_PUBLIC_KEY_ID, self._rsa_signer)

            # Addition headers
            response_content_disposition = kwargs.get("response_content_disposition")
            if response_content_disposition:
                encode_response_content_disposition = urllib.parse.unquote(
                    response_content_disposition
                ).replace("+", "%20")
                file_path = "{}?response-content-disposition={}".format(file_path, encode_response_content_disposition)

            # Create a signed url that will be valid until the specific expiry date provided using a canned policy.
            signed_url = cloudfront_signer.generate_presigned_url(file_path, date_less_than=expire_date)
            return signed_url

        else:
            expired_in = kwargs.get("expired_in", 120)
            response_content_disposition = kwargs.get("response_content_disposition", None)
            bucket_params = {
                'Bucket': source,
                'Key': file_path,
            }
            if response_content_disposition:
                bucket_params.update({"ResponseContentDisposition": response_content_disposition})
            pre_signed_params = {
                "Params": bucket_params,
                "ExpiresIn": expired_in
            }
            url = self.spaces_client.generate_presigned_url(
                'get_object',
                **pre_signed_params
            )
            url = url.replace("https://{}.sgp1.digitaloceanspaces.com".format(source), settings.DO_SPACES_SUB_URL)
            return url

    @staticmethod
    def _rsa_signer(message):
        private_key = serialization.load_pem_private_key(
            settings.AWS_CLOUDFRONT_PRIVATE_KEY_PEM.encode(),
            password=None,
            backend=default_backend()
        )
        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())
