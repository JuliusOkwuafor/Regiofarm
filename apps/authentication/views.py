from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.views import APIView

from utils.response import APIResponse

from .serializers import (
    LoginSerializer,
    RegisterSellerSerializer,
    RegisterUserSerializer,
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSellerSerializer

    def post(self, request: Request):
        role = request.query_params.get("role", None)
        if role == "seller":
            serializer = RegisterSellerSerializer(data=request.data)
        else:
            serializer = RegisterUserSerializer(
                data=request.data, context={"role": role}
            )
        if not serializer.is_valid():
            return APIResponse(
                msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST, code=40000
            )
        serializer.save()
        return APIResponse(
            msg="User created successfully", status=status.HTTP_201_CREATED, code=20000
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

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
