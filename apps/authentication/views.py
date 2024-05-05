import random

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import OTP, User

from utils.response import APIResponse
from utils.utils import Utils

from .serializers import (
    LoginSerializer,
    RegisterUserSerializer,RegisterSellerSerializer
)
from .utils import activation_token
from . import openapi
# from seller.serializers import SellerSerializer


class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer

    @swagger_auto_schema(
        manual_parameters=[openapi.role],
        request_body=RegisterUserSerializer,
        responses=openapi.registered_response,
        operation_description="Create a new User",
    )
    def post(self, request: Request):
        role = request.query_params.get("role", None)
        serializer = self.serializer_class(data=request.data, context={"role": role})
        if not serializer.is_valid():
            return APIResponse(
                msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST, code=40000
            )
        serializer.save()
        return APIResponse(
            msg="User created successfully", status=status.HTTP_201_CREATED, code=20000
        )


class RegisterSellerView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSellerSerializer

    @swagger_auto_schema(
        request_body=RegisterSellerSerializer,
        responses=openapi.registered_seller_response,
        operation_description="Create a new Seller",
    )
    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST, code=40000
            )
        serializer.save()
        return APIResponse(
            msg="Seller created successfully",
            status=status.HTTP_201_CREATED,
            code=20000,
        )


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        responses=openapi.verify_email_response,
        operation_description="Activate user account using email confirmation link",
    )
    def get(self, request, uidb64, token) -> Response:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None
        if user is not None and activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return APIResponse(
                data={},
                msg="Email confirmation successful",
                code=20000,
                status=status.HTTP_202_ACCEPTED,
            )
        return APIResponse(
            data={},
            msg="Invalid token",
            code=40000,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses=openapi.login_response,
        operation_description="User login endpoint",
    )
    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return APIResponse(
                msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST, code=40000
            )
        return APIResponse(
            msg="User logged in successfully",
            status=status.HTTP_200_OK,
            code=20000,
            data=serializer.validated_data,
        )


class RequestPasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = []

    def generate_otp(self) -> int:
        return random.randint(100000, 999999)

    @swagger_auto_schema(
        request_body=openapi.request_email_body,
        responses=openapi.request_email_response,
        operation_description="Request a password reset for a user",
    )
    def post(self, request: Request) -> Response:
        email = request.data.get("email")
        if not email:
            return APIResponse(
                data={},
                msg="Email is required",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = Utils.get_or_none(User, email=email)
        if user is None:
            return APIResponse(
                data={},
                msg="User not found",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        code: int = self.generate_otp()
        try:
            otp = Utils.get_or_none(OTP, user=user)
            if otp is not None:
                otp.delete()
                OTP.objects.create(user=user, code=code)
            else:
                OTP.objects.create(user=user, code=code)
        except Exception as e:
            return APIResponse(
                data={},
                msg="Error creating OTP",
                code=50000,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return APIResponse(
            data={},
            msg="Password reset email sent",
            code=20000,
            status=status.HTTP_200_OK,
        )


class CheckResetPasswordOTP(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.check_reset_body,
        responses=openapi.check_reset_response,
        operation_description="Verify OTP sent to user's email",
    )
    def post(self, request: Request) -> Response:
        email = request.data.get("email")
        otp = request.data.get("otp")
        if not email or not otp:
            return APIResponse(
                data={},
                msg="Email and OTP are required",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(email=email).first()
        if user is None:
            return APIResponse(
                data={},
                msg="User not found",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp_instance = OTP.objects.filter(user=user, code=otp).first()
        if otp_instance is None or otp_instance.is_expired:
            return APIResponse(
                data={},
                msg="Invalid or expired OTP",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return APIResponse(
            data={},
            msg="Valid OTP",
            code=20000,
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.reset_password_body,
        responses=openapi.reset_password_response,
        operation_description="Reset user password using email, OTP and new password",
    )
    def patch(self, request: Request) -> Response:
        email = request.data.get("email")
        otp = request.data.get("otp")
        password = request.data.get("password")
        if not email or not otp or not password:
            return APIResponse(
                data={},
                msg="Email, OTP and password are required",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not Utils.validate_password(password):
            return APIResponse(
                data={},
                msg="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit and one special character.",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = Utils.get_or_none(User, email=email)
        if user is None:
            return APIResponse(
                data={},
                msg="User not found",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp_instance = Utils.get_or_none(OTP, user=user, code=otp)
        if otp_instance is None:
            return APIResponse(
                data={},
                msg="Invalid OTP",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(password)
        user.save()
        otp_instance.delete()
        return APIResponse(
            data={},
            msg="Password reset successful",
            code=20000,
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.change_password_body,
        responses=openapi.change_password_response,
        operation_description="Change user password using current password and new password",
    )
    def patch(self, request: Request) -> Response:
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            return APIResponse(
                data={},
                msg="Old and new password are required",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if old_password == new_password:
            return APIResponse(
                data={},
                msg="New password must be different from old password",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.check_password(old_password):
            return APIResponse(
                data={},
                msg="Invalid old password",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not Utils.validate_password(new_password):
            return APIResponse(
                data={},
                msg="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit and one special character.",
                code=40000,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()
        return APIResponse(
            data={},
            msg="Password changed successfully",
            code=20000,
            status=status.HTTP_200_OK,
        )
