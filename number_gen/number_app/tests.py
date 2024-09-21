import unittest
from unittest.mock import patch, Mock
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .views import AsyncTrackingNumberView

class TestPostMethod(TestCase):
    @patch("random.choices")
    def test_post_method_with_valid_data(self, mock_random_choices):
        # Mock the random.choices method to return a valid tracking number
        mock_random_choices.return_value = ["A", "1", "B", "2", "C", "3", "D", "4", "E", "5", "F", "6", "G", "7", "H", "8", "I", "9", "J", "10", "K", "11", "L", "12", "M", "13", "N", "14", "O", "15", "P", "16"]

        # Create an instance of the APIClient for testing
        client = APIClient()

        # Create a valid payload for the POST request
        valid_payload = {
            "origin_country_id": "1",
            "destination_country_id": "2",
            "weight": "10",
            "created_at": "2022-01-01T00:00:00",
            "customer_id": "1",
            "customer_name": "John Doe",
            "customer_slug": "johndoe"
        }

        # Make a POST request to the API endpoint
        response = client.post("/api/tracking-numbers/", valid_payload)

        # Assert that the response status code is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the response contains a valid tracking number
        self.assertIn("tracking_number", response.data)

        # Assert that the response contains a created_at field with a valid ISO format
        self.assertIn("created_at", response.data)
        self.assertTrue(isinstance(response.data["created_at"], str))
        self.assertTrue(datetime.fromisoformat(response.data["created_at"]).isoformat() == "2022-01-01T00:00:00")


    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.force_authenticate(self.client, user=self.user)

    def test_invalid_serializer_returns_400(self):
        """
        Test that a 400 status code is returned when the serializer is not valid.
        """
        url = reverse('tracking-number-list')
        data = {'invalid_field': 'invalid_value'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

