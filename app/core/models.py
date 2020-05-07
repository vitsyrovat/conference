from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import datetime

# from django.utils import timezone

REGISTRATION_DEADLINE = datetime.date(2020, 6, 15)
REGISTRATION_FEES = {
    'Normal': 800,
    'Late': 1200,
}


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


class Affiliation(models.Model):
    """Model for affiliations"""
    institution = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.PositiveIntegerField()
    country = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.department}, {self.institution}'


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Contribution(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, through='Authorship')
    presentation_form = models.CharField(
        max_length=16,
        choices=[
            ('oral', 'Oral'),
            ('poster', 'Poster'),
        ],
        default='Oral',
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(default=0)
    # discount to be set by admin in negative CZK

    @property
    def registration_period(self):
        """Returns registration period based on date"""
        if self.created.date() < REGISTRATION_DEADLINE:
            return 'Normal'
        else:
            return 'Late'

    def __str__(self):
        return f"{self.title[0:20]}... registered by {self.user}"

    @property
    def registration_fee(self):
        """Return registration fee based on registration_period and discount"""
        return REGISTRATION_FEES[self.registration_period] + self.discount


class Authorship(models.Model):
    """Model for unique author-contribution relationships"""
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_main_author = models.BooleanField(default=False)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    affiliation = models.ManyToManyField(Affiliation)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'contribution'],
                name='unique_author_contribution'
            )
        ]

    def __str__(self):
        return f"{self.author} from {self.affiliation.all()}: \
            {self.contribution}"
