from .base import *
import dj_database_url

ALLOWED_HOSTS = ["regio-backend.onrender.com", "127.0.0.1"]

# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True
CORS_ALLOW_ALL_ORIGINS = True

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
