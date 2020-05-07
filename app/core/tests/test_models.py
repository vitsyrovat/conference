from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django.db.utils import IntegrityError

from core.models import Affiliation, Author, Authorship, Contribution


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

    def test_create_author(self):
        """Create a new author with name"""
        name = 'Jan Sychra'
        author = Author.objects.create(name=name)

        self.assertEqual(author.name, name)
        self.assertEqual(Author.objects.count(), 1)

    def test_create_authorship_twice(self):
        """Creating authorship for the same author and contribution
        twice fails
        """
        user = get_user_model().objects.create_user(
            'test@dev.com',
            'asdaf6547'
        )

        name = 'Jan Sychra'
        title = 'Ptaci Brna'
        author = Author.objects.create(name=name)

        contribution = Contribution.objects.create(
            title=title,
            user=user
        )
        Authorship.objects.create(
            author=author,
            contribution=contribution
        )

        with self.assertRaises(IntegrityError):
            Authorship.objects.create(
                author=author,
                contribution=contribution
            )

    def test_create_author_with_variable_affiliations(self):
        """One author may have different affiliations in contributions"""
        user = get_user_model().objects.create_user(
            'test@dev.com',
            'asdaf6547'
        )

        author = Author.objects.create(name='Jan Sychra')
        contribution1 = Contribution.objects.create(
            title='ptaci',
            user=user,
        )
        contribution2 = Contribution.objects.create(
            title='brouci',
            user=user,
        )
        contribution1.authors.add(author)
        contribution2.authors.add(author)
        affiliation1 = Affiliation.objects.create(
            institution='Masaryk univ',
            department='ustav botaniky a zoologie',
            street_address='kotlarska 2',
            city='Brno',
            zip_code='61037',
            country='Ceska Republika',
        )
        affiliation2 = Affiliation.objects.create(
            institution='CSO',
            street_address='Horni dolni 1',
            city='Brno',
            zip_code='60200',
            country='Ceska Republika',
        )

        authorship1 = Authorship.objects.get(contribution=contribution1)
        authorship1.affiliation.add(affiliation1)

        authorship2 = Authorship.objects.get(contribution=contribution2)
        authorship2.affiliation.add(affiliation1, affiliation2)

        self.assertEqual(authorship1.affiliation.count(), 1)
        self.assertEqual(authorship2.affiliation.count(), 2)
