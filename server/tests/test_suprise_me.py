from freezegun import freeze_time

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

    def test_create(self) -> None:
        surprise = self.create()
        assert surprise["bottom_text"] in FUNNY_PHRASES
        assert surprise["top_text"] in FUNNY_PHRASES
