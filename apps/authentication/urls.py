from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordView,
    CheckResetPasswordOTP,
    LoginView,
    RegisterView,
    RequestPasswordResetView,
    ResetPasswordView,
    VerifyEmailView,
)

app_name = "authentication"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "email-verify/<slug:uidb64>/<slug:token>/",
        VerifyEmailView.as_view(),
        name="email_verify",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "request-reset-email/",
        RequestPasswordResetView.as_view(),
        name="request-reset-email",
    ),
    path("check-reset-otp/", CheckResetPasswordOTP.as_view(), name="check-reset-otp"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
