from datetime import datetime
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


@freeze_time(DEFAULT_TIME)
class TestMemeViewsSet(APITestCase):
    base_name: str
    template: MemeTemplate

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.token = Token.objects.create(user=cls.user)
        cls.template = MemeTemplate.objects.create(
            name="Template",
            image_url="https://example.com/template1.jpg",
            default_top_text=DEFAULT_TOP_TEXT,
            default_bottom_text=DEFAULT_BOTTOM_TEXT,

        )
        cls.first_meme = Meme.objects.create(
            template=cls.template,
            top_text=DEFAULT_TOP_TEXT,
            bottom_text=DEFAULT_BOTTOM_TEXT,
            created_by=cls.user,
        )
        cls.second_meme = Meme.objects.create(
            template=cls.template,
            top_text=DEFAULT_TOP_TEXT,
            bottom_text=DEFAULT_BOTTOM_TEXT,
            created_by=cls.user,
        )
        cls.base_name = "meme"

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
        time_obj = datetime.strptime(DEFAULT_TIME, '%Y-%m-%dT%H:%M:%S.%fZ')
        formatted_time_str = time_obj.strftime('%Y-%m-%dT%H:%M:%SZ')

        assert self.list() == [
            {
                "id": self.first_meme.id,
                "template": self.template.id,
                "top_text": DEFAULT_TOP_TEXT,
                "bottom_text": DEFAULT_BOTTOM_TEXT,
                "created_by": self.user.id,
                "created_at": formatted_time_str,
            },
            {
                "id": self.second_meme.id,
                "template": self.template.id,
                "top_text": DEFAULT_TOP_TEXT,
                "bottom_text": DEFAULT_BOTTOM_TEXT,
                "created_by": self.user.id,
                "created_at": formatted_time_str,
            },
        ]
