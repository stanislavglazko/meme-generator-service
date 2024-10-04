from freezegun import freeze_time
from http import HTTPStatus
from typing import Any

from meme_generator.models import MemeTemplate
from meme_generator.services import FUNNY_PHRASES

from .base import TestViewSetBase, DEFAULT_TIME


@freeze_time(DEFAULT_TIME)
class TestSurpriseMeViewSet(TestViewSetBase):
    base_name: str
    template: MemeTemplate

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.base_name = "surprise-me"

    def list(self, query_params: dict = None, args: list[str | int] = None) -> dict[str, Any]:
        response = self.request_list(query_params, args=args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def test_list(self) -> None:
        surprise = self.list()
        assert surprise["bottom_text"] in FUNNY_PHRASES
        assert surprise["top_text"] in FUNNY_PHRASES
