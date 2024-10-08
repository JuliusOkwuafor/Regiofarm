import os

from .base import *
import dj_database_url

ALLOWED_HOSTS = [".onrender.com", "127.0.0.1"]
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": dj_database_url.parse(config("DB_URL")),
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = True
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
# print(f"ftp://{config('FTP_USER')}:{config('FTP_PASSWORD')}@{config('FTP_HOST')}:21/")
