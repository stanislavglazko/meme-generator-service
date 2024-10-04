import io
from PIL import Image
from typing import Any, Final
from http import HTTPStatus
from django.urls import reverse
from meme_generator.models import MemeTemplate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


DEFAULT_TOP_TEXT: Final[str] = "top"
DEFAULT_BOTTOM_TEXT: Final[str] = "bottom"
DEFAULT_TEMPLATE_NAME: Final[str] = "Template"
DEFAULT_USERNAME: Final[str] = "testuser"
DEFAULT_PASSWORD: Final[str] = "password123"
DEFAULT_TIME = "2024-10-03T12:00:00.000000Z"
INCORRECT_MEME_ID: int = 100000000000
INCORRECT_SCORE: int = 77


class TestViewSetBase(APITestCase):
    base_name: str
    image: SimpleUploadedFile
    template: MemeTemplate

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.token = Token.objects.create(user=cls.user)
        cls.image = cls.generate_test_image()
        cls.template = MemeTemplate.objects.create(
            name=DEFAULT_TEMPLATE_NAME,
            image=cls.image,
            default_top_text=f"Template{DEFAULT_TOP_TEXT}",
            default_bottom_text=f"Template{DEFAULT_BOTTOM_TEXT}",

        )

    @classmethod
    def list_url(cls, args: list[str | int] = None) -> str:
        return reverse(f"{cls.base_name}-list", args=args)

    def request_list(self, data: dict = None, args: list[str | int] = None) -> Response:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        return self.client.get(self.list_url(args), data=data)

    def list(self, query_params: dict = None, args: list[str | int] = None) -> list[dict[str, Any]]:
        response = self.request_list(query_params, args=args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()["results"]

    def request_create(self, data: dict[str, Any], args: list = None) -> Response:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        return self.client.post(self.list_url(args), data=data)

    def create(self, data: dict[str, Any], args: list = None) -> dict[str, Any]:
        response = self.request_create(data, args)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.json()

    def request_retrieve(
        self, entity: dict, query_params: dict = None, args: list = None
    ) -> Response:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        return self.client.get(self.detail_url(entity["id"], args), data=query_params)

    def retrieve(
        self, entity: dict[str, Any], args: list = None, query_params: dict = None
    ) -> dict[str, Any]:
        response = self.request_retrieve(entity, query_params, args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    @classmethod
    def detail_url(cls, key: str | int, args: list = None) -> str:
        keys = [key]
        if args:
            keys.insert(0, *args)
        return reverse(f"{cls.base_name}-detail", args=keys)

    @classmethod
    def generate_test_image(cls) -> SimpleUploadedFile:
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg')
