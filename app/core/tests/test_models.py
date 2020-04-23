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

    def test_create_user_without_email(self):
        """Creating a user without email raises ValueError"""
        email = None
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email, 'test654654'
            )

    def test_create_user_with_invalid_email(self):
        """Creating user with invalid email raises ValidationError"""
        test_emails = ['pako', ' ', 'email.com', 'jesid@seznam',
                       '@seznam.cz', 'joko@']

        def bulk_email_test(email):
            with self.assertRaises(ValidationError):
                get_user_model().objects.create_user(
                    email=email,
                    password='aslkjd676546'
                )

        [bulk_email_test(email) for email in test_emails]

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@dev.com',
            'asdaf6547'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
