# import jwt
#
# from django.conf import settings
#
# from shared.authentications.general_auth import GeneralAuthentication
# from shared.constants.token import TOKEN_TYPE_AUTHENTICATION
# from mycystack_models.models.users.users import User
# from shared.utils.app import now
#
#
# class BasicTokenAuthentication(GeneralAuthentication):
#     def authenticate(self, request):
#         token_value = self._get_token(request)
#         if token_value is None:
#             return None
#
#         try:
#             payload = jwt.decode(token_value, settings.SECRET_KEY, algorithms=['HS256'])
#             token_type = payload.get("token_type", None)
#             email = payload.get("user", None)
#             expired_time = payload.get("expired_time", 0)
#             # Check token type
#             if (token_type != TOKEN_TYPE_AUTHENTICATION) or (email is None):
#                 return None
#             if expired_time < now():
#                 return None
#
#             user = User.objects.get(email=email)
#             return user, token_value
#
#         except (jwt.InvalidSignatureError, jwt.DecodeError, jwt.exceptions.InvalidAlgorithmError, User.DoesNotExist):
#             return None
