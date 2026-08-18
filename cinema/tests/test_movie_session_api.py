from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from cinema.models import CinemaHall, Movie


class MovieSessionApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test description",
            duration=120,
        )

        self.cinema_hall = CinemaHall.objects.create(
            name="Test Hall",
            rows=10,
            seats_in_row=10,
        )

    def test_cannot_create_movie_session_in_past(self):
        payload = {
            "show_time": (
                timezone.now() - timedelta(hours=1)
            ).isoformat(),
            "movie": self.movie.id,
            "cinema_hall": self.cinema_hall.id,
        }

        response = self.client.post(
            reverse("cinema:moviesession-list"),
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("show_time", response.data)
