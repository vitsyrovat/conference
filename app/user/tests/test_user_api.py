from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the Users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Creating user with valid payload successful"""
        payload = {
            'email': 'pako@emil.com',
            'password': 'kotaP_11445',
            'name': 'kokok'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        # check that user was created and contains the email:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertContains(response, payload['email'], status_code=201)
        # this checks both status_code and email address presence

        # to check password, user is retrieved from the db
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))

        # password is not returned in the response:
        self.assertNotIn('password', response.data)
        self.assertNotContains(response, 'password', status_code=201)
        # this is the same as previous

    def test_user_exists(self):
        """Creating a user that already exists fails"""

        payload = {
            'email': 'pako@mail.com',
            'password': '31asdasfvf84',
            'name': 'pako'
        }

        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Creating user fails with password either:
        1. too short (< 8 characters),
        2. only numeric,
        3. too simple,
        4. or too common.
        """

        # set of passwords to be checked for invalidity
        passwords = ['A_1ku45', '84651005', 'a1111111', 'heavymetal']

        # function that checks one password in a run
        # ------------------------------------------
        def bulk_password_test(password):
            payload = {
                'email': 'pako@mail.com',
                'password': password,
                'name': 'pako'
            }

            response = self.client.post(CREATE_USER_URL, payload)
            # print(response.content)

            # check that response contains password error message
            # and response status_code is BAD_REQUEST:
            self.assertContains(
                response,
                "password",
                status_code=400)

            # check that user is not created:
            user_exists = get_user_model().objects.filter(
                email=payload['email']
                ).exists()
            self.assertFalse(user_exists)

            # which is the same as this:
            user = get_user_model().objects.filter(
                email=payload['email']
            )
            self.assertQuerysetEqual(user, [])
        # ------------------------------------------

        [bulk_password_test(password) for password in passwords]

    def test_create_token(self):
        """Token is returned for a valid user"""
        payload = {
            'name': 'pako',
            'email': 'pako@email.com',
            'password': 'sdko6548as'
        }
        create_user(**payload)

        response = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertContains(response, 'token')
        # last assertion replaces the both above

    def test_create_token_invalid_password(self):
        """Token is not returned if invalid credentials provided"""
        create_user(email='koko@mail.com', password='secretpassword555')
        response = self.client.post(
            CREATE_TOKEN_URL,
            {
                'email': 'koko@mail.com',
                'password': 'wrongpassword001'
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        self.assertNotContains(response, 'token', status_code=400)
        # last assertion replaces the both above

    def test_create_token_non_existing_user(self):
        """Token is not provided to non-existing user"""
        payload = {
            'email': 'pako@email.com',
            'password': 'hasjf8765as'
        }
        response = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertNotContains(response, 'token', status_code=400)

    def test_create_token_no_password(self):
        """Token not returned if password not provided"""
        create_user(email='koko@mail.com', password='koasd5465fsdf')
        response = self.client.post(
            CREATE_TOKEN_URL,
            {'email': 'koko@mail.com', 'password': ''}
        )
        self.assertNotContains(response, 'token', status_code=400)
