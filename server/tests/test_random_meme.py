from typing import Any, Final
from http import HTTPStatus
from rest_framework.test import APITestCase
from django.urls import reverse
from meme_generator.models import Meme, MemeTemplate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


DEFAULT_TOP_TEXT: Final[str] = "top"
DEFAULT_BOTTOM_TEXT: Final[str] = "bottom"


class TestRandomMemeViewSet(APITestCase):
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
        cls.base_name = "random-meme"

    @classmethod
    def list_url(cls, args: list[str | int] = None) -> str:
        return reverse(f"{cls.base_name}-list", args=args)

    def request_list(self, data: dict = None, args: list[str | int] = None) -> Any:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        return self.client.get(self.list_url(args), data=data)

    def list(self, query_params: dict = None, args: list[str | int] = None) -> dict[str, Any]:
        response = self.request_list(query_params, args=args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def test_list(self) -> None:
        response_with_empty_memes = self.request_list()

        assert response_with_empty_memes.status_code == HTTPStatus.NOT_FOUND

        first_meme = Meme.objects.create(
            template=self.template,
            created_by=self.user,
        )
        second_meme = Meme.objects.create(
            template=self.template,
            created_by=self.user,
        )

        response_with_memes = self.list()
        meme_id = response_with_memes["id"]

        assert meme_id in (first_meme.id, second_meme.id)
