from datetime import datetime
from freezegun import freeze_time
from typing import Any, Final
from http import HTTPStatus
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from meme_generator.models import Meme, MemeTemplate, Rating
from meme_generator.views import TOP_MEMES_NUMBER


DEFAULT_TOP_TEXT: Final[str] = "top"
DEFAULT_BOTTOM_TEXT: Final[str] = "bottom"
DEFAULT_TIME = "2024-10-03T12:00:00.000000Z"


@freeze_time(DEFAULT_TIME)
class TestTopMemeSViewSet(APITestCase):
    base_name: str
    template: MemeTemplate

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.token = Token.objects.create(user=cls.user)
        cls.template = MemeTemplate.objects.create(
            name="Template",
            image_url="https://example.com/template1.jpg",
            default_top_text=f"Template{DEFAULT_TOP_TEXT}",
            default_bottom_text=f"Template{DEFAULT_BOTTOM_TEXT}",

        )
        cls.base_name = "top-memes"

    @classmethod
    def list_url(cls, args: list[str | int] = None) -> str:
        return reverse(f"{cls.base_name}-list", args=args)

    def request_list(self, data: dict = None, args: list[str | int] = None) -> Any:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        return self.client.get(self.list_url(args), data=data)

    def list(self, query_params: dict = None, args: list[str | int] = None) -> list[dict[str, Any]]:
        response = self.request_list(query_params, args=args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()["results"]

    def test_list(self) -> None:
        high_rated_memes_ids = set()
        for i in range(10):
            high_rated_meme = Meme.objects.create(
                template=self.template,
                created_by=self.user,
            )
            Rating.objects.create(
                meme=high_rated_meme,
                user=self.user,
                score=5,
            )
            high_rated_memes_ids.add(high_rated_meme.id)
        low_rated_memes_ids = set()
        for i in range(2):
            low_rated_meme = Meme.objects.create(
                template=self.template,
                created_by=self.user,
            )
            Rating.objects.create(
                meme=low_rated_meme,
                user=self.user,
                score=1,
            )
            low_rated_memes_ids.add(low_rated_meme.id)

        top_memes = self.list()

        assert len(top_memes) == TOP_MEMES_NUMBER
        top_memes_ids = {meme["id"] for meme in top_memes}
        assert top_memes_ids == high_rated_memes_ids
