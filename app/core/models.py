from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Ceates and saves a new user"""

        if not email:
            raise ValueError("Users must have an email address.")
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Invalid email address.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save superuser"""
        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_staff = True
        superuser.is_superuser = True

        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email instead of user name"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
