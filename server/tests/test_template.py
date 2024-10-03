from typing import Any
from http import HTTPStatus
from rest_framework.test import APITestCase
from django.urls import reverse
from meme_generator.models import MemeTemplate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class MemeTemplateTests(APITestCase):
    base_name: str

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.token = Token.objects.create(user=cls.user)
        cls.first_template = MemeTemplate.objects.create(
            name="Template 1",
            image_url="https://example.com/template1.jpg",
            default_top_text="Top 1",
            default_bottom_text="Bottom 1"
        )
        cls.second_template = MemeTemplate.objects.create(
            name="Template 2",
            image_url="https://example.com/template2.jpg",
            default_top_text="Top 2",
            default_bottom_text="Bottom 2"
        )
        cls.base_name = "template"

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
        res = self.list()
        print("HHH", res)
        assert self.list() == [
            {
                "id": self.first_template.id,
                "name": self.first_template.name,
                "image_url": self.first_template.image_url,
                "default_top_text": self.first_template.default_top_text,
                "default_bottom_text": self.first_template.default_bottom_text,
            },
            {
                "id": self.second_template.id,
                "name": self.second_template.name,
                "image_url": self.second_template.image_url,
                "default_top_text": self.second_template.default_top_text,
                "default_bottom_text": self.second_template.default_bottom_text,
            }
        ]
