from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class ModelTest(TestCase):

    def test_create_user_w_email_successful(self):
        """Creating a new user with email successful"""
        email = 'vit@email.com'
        password = 'lkajsd654654a'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new iser is normalized"""
        email = 'test@pOKASD.com'
        user = get_user_model().objects.create_user(email, 'asdas5465')

        self.assertEqual(user.email, email.lower())

    def test_new_user_no_email(self):
        """Test creating user with no email raises error"""
        email = None
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email, 'asdjhfksjdh'
            )

    def test_new_user_valid_email(self):
        """Test creating new user with an invalid email raises error"""

        email1 = 'oijo@'
        email2 = 'koko@loko'
        email3 = '--'

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(email1, 'ksdfjklsldk')
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(email2, 'lsdkjfou5i')
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(email3, 'laksflks11d')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@dev.com',
            'asdaf6547'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
