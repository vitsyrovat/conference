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


class ContributionManager(models.Manager):

    def create(self, title, presentation_form, authorships):
        # 1 create  contribution without authors
        contribution = Contribution(
            title=title,
            presentation_form=presentation_form,
            user=self.request.user
        )
        contribution.save()
        # 2 for each authorship create author and authorship instance,
        # and add the author to the authorship instance.
        for authorship_data in authorships:
            author = Author(name=authorship_data['author_name'])
            author.save()
            
            authorship = Authorship(
                author=author,
                is_main_author=authorship_data['is_main_author'],
                contribution=contribution,
            )

            # 4 for each affiliation add it to the authorsip instance.
            authorship.affiliation.add(authorship_data['affiliations'])

            authorship.save()

        # 5 finally add the user to the contribution
        return contribution


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

    fee_payed = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(default=0)
    # discount to be set by admin in negative CZK

    objects = ContributionManager

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
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='authorships'
    )
    is_main_author = models.BooleanField(default=False)
    contribution = models.ForeignKey(
        Contribution,
        on_delete=models.CASCADE,
        related_name='authorships')
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
