from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from cinema.models import CinemaHall, Movie, MovieSession


class OrderApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="testpass123",
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

    def test_cannot_buy_ticket_for_started_movie_session(self):
        movie_session = MovieSession.objects.create(
            show_time=timezone.now() - timedelta(hours=1),
            movie=self.movie,
            cinema_hall=self.cinema_hall,
        )

        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "movie_session": movie_session.id,
                }
            ]
        }

        response = self.client.post(
            reverse("cinema:order-list"),
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "movie_session",
            str(response.data),
        )