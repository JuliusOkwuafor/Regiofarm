from .base import *
import dj_database_url

ALLOWED_HOSTS = [
    "regio-backend.onrender.com",
    "127.0.0.1",
    "regiofarm.onrender.com",
    "myregio.farm",
] + config("ALLOWED_HOSTS").split(",")

# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True
# CORS_ALLOWED_ORIGINS = ["*"]

DATABASES = {
    "default": dj_database_url.parse(config("DB_URL")),
}
# DATABASES = {
#     "default": {
#         "ENGINE": "mysql.connector.django",
#         "NAME": config("DB_NAME"),
#         "USER": config("DB_USER"),
#         "PASSWORD": config("DB_PASSWORD"),
#         "HOST": "localhost",
#         "PORT": "3306",
#     }
# }

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True

# DEFAULT_FROM_EMAIL = "noreply@regio.com"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# # FTP Storage settings
# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.ftp.FTPStorage",
#         "OPTIONS": {
#             "location": f"ftps://{config('FTP_USER')}:{config('FTP_PASSWORD')}@{config('FTP_HOST')}:21/",
#             "encoding": "latin-1",
#             "base_url": f"https://myregio.farm/media/",
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

# # S3 settings
# AWS_S3_URL_PROTOCOL = "https"
# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_QUERYSTRING_AUTH = False

# MEDIA_URL = f"{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/media/"

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "region_name": AWS_S3_REGION_NAME,
#             "access_key": AWS_ACCESS_KEY_ID,
#             "secret_key": AWS_SECRET_ACCESS_KEY,
#             "endpoint_url": AWS_S3_CUSTOM_DOMAIN,
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }
