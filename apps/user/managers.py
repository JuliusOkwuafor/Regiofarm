from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from .enums import Role


class UserManager(BaseUserManager):

    def create_user(self, email, firstname, lastname, password=None, **extra_fields):
        if not email:
            raise ValidationError("The Email field must be set")
        if not firstname:
            raise ValidationError("The First Name field must be set")
        if not lastname:
            raise ValidationError("The Last Name field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, firstname=firstname, lastname=lastname, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, firstname, lastname, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.ADMIN)
        return self.create_user(email, firstname, lastname, password, **extra_fields)

    def create_adminuser(
        self, email, firstname, lastname, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", Role.ADMIN)
        return self.create_user(email, firstname, lastname, password, **extra_fields)
