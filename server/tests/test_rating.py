from freezegun import freeze_time
from typing import Any, Final
from http import HTTPStatus
from rest_framework.test import APITestCase
from django.urls import reverse
from meme_generator.models import Meme, MemeTemplate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


DEFAULT_TOP_TEXT: Final[str] = "top"
DEFAULT_BOTTOM_TEXT: Final[str] = "bottom"
DEFAULT_TIME = "2024-10-03T12:00:00.000000Z"
INCORRECT_MEME_ID: int = 100000000000
INCORRECT_SCORE: int = 77


@freeze_time(DEFAULT_TIME)
class TesRatingViewSet(APITestCase):
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
        cls.meme = Meme.objects.create(
            template=cls.template,
            bottom_text=DEFAULT_BOTTOM_TEXT,
            created_by=cls.user,
        )
        cls.base_name = "rating"

    @classmethod
    def list_url(cls, args: list[str | int] = None) -> str:
        return reverse(f"{cls.base_name}-list", args=args)

    def request_create(self, data: dict[str, Any], args: list = None) -> Any:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        return self.client.post(self.list_url(args), data=data)

    def create(self, data: dict[str, Any], args: list = None) -> dict[str, Any]:
        response = self.request_create(data, args)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.json()

    def create_rating(self, data: dict, args: list = None) -> dict:
        return self.create(data, args)

    def test_create_or_update(self) -> None:
        rating = self.create_rating(
            {
                "score": 4,
            },
            [self.meme.pk]
        )

        assert rating == {
            "score": 4,
        }

        response = self.request_create(
            {
                "score": 3,
            },
            [self.meme.pk]
        )
        assert response.status_code == HTTPStatus.OK

        assert response.json() == {
            "score": 3,
        }

    def test_incorrect_meme(self) -> None:
        response = self.request_create(
            {
                "score": 3,
            },
            [INCORRECT_MEME_ID]
        )

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_incorrect_score(self) -> None:
        response = self.request_create(
            {
                "score": INCORRECT_SCORE,
            },
            [self.meme.pk]
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
