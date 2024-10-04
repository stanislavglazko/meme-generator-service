from typing import Any
from http import HTTPStatus
from meme_generator.models import Meme, MemeTemplate

from .base import TestViewSetBase


class TestRandomMemeViewSet(TestViewSetBase):
    base_name: str
    template: MemeTemplate

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.base_name = "random-meme"

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
