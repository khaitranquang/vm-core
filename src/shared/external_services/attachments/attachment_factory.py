from typing import Optional

from shared.external_services.attachments.attachment import AttachmentStorageService
from shared.external_services.attachments.impl.aws_attachment import AWSAttachmentService
from shared.external_services.attachments.impl.do_attachment import DOAttachmentService

ATTACHMENT_AWS = "aws"
ATTACHMENT_DO_SPACES = "do_spaces"


class AttachmentStorageFactory:
    @classmethod
    def get_attachment_service(cls, service_name: str) -> Optional[AttachmentStorageService]:
        if service_name == ATTACHMENT_AWS:
            return AWSAttachmentService()
        elif service_name == ATTACHMENT_DO_SPACES:
            return DOAttachmentService()
        raise Exception("The attachment service name {} does not support".format(service_name))
