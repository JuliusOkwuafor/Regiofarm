from rest_framework import serializers
from user.enums import Role
from user.models import User, UserAddress
from seller.models import Seller
from typing import Any

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from user.validators import password_validator
from user.serializers import UserAddressSerializer


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100,
        min_length=8,
        write_only=True,
        required=True,
        validators=[password_validator],
    )

    class Meta:
        model = User
        fields = ["email", "firstname", "lastname", "password", "currency", "language"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = self.context.get("role", None)
        if role == Role.ADMIN:
            user = User.objects.create_adminuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        return user


class RegisterSellerSerializer(serializers.ModelSerializer):
    user = RegisterUserSerializer()
    address = UserAddressSerializer()

    class Meta:
        model = Seller
        fields = ["user", "name", "ceo", "vat", "address"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data, role=Role.SELLER)
        address_data = validated_data.pop("address")
        UserAddress.objects.create(user=user, **address_data)
        seller_profile = Seller.objects.create(user=user, **validated_data)
        return seller_profile


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, write_only=True, required=True)
    password = serializers.CharField(
        max_length=100, min_length=8, write_only=True, required=True
    )

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )
        if not user.check_password(password):
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )
        if not user.is_verified:
            raise serializers.ValidationError("This user has not been verified.")
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")
        return {"tokens": user.tokens()}


class RefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs: Any) -> Any:
        token = super().validate(attrs)
        data = {
            "code": 20000,
            "msg": "Token refreshed successfully",
            "data": {"tokens": token},
        }
        return data
