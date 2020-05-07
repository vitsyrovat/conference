from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


# CREATE_CONTRIBUTION_URL = reverse('contribution:create')
CONTRIBUTION_URL = reverse('contribution:contribution-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class ContributionTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        payload = {
            'email': 'koko@gmail.com',
            'password': 'ajlkjfs5734',
            'name': 'jjsjsj',
        }
        self.user = create_user(**payload)
        self.client.force_authenticate(user=self.user)

    def test_contribution_created_by_authenticated_user(self):
        """Authorized user may create a contribution"""
        payload = {
            'title': 'Chironomids of the Vltava river',
            'presentation_form': 'oral',
        }

        res = self.client.post(CONTRIBUTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
