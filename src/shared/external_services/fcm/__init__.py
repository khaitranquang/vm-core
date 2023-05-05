import ast
import firebase_admin
from firebase_admin import credentials

from django.conf import settings

from shared.log.cylog import CyLog

# CyLog.info(**{"message": "FCM_CRED_SERVICE_ACCOUNT: {}".format(settings.FCM_CRED_SERVICE_ACCOUNT)})

credentials_json_data = ast.literal_eval(str(settings.FCM_CRED_SERVICE_ACCOUNT))

cred = credentials.Certificate(credentials_json_data)
default_app = firebase_admin.initialize_app(cred)
