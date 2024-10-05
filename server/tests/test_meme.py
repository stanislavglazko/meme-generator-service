from datetime import datetime
from freezegun import freeze_time
from meme_generator.models import Meme, MemeTemplate

from .base import TestViewSetBase, DEFAULT_TIME, DEFAULT_TOP_TEXT, DEFAULT_BOTTOM_TEXT


@freeze_time(DEFAULT_TIME)
class TestMemeViewSet(TestViewSetBase):
    base_name: str
    template: MemeTemplate

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.first_meme = Meme.objects.create(
            template=cls.template,
            bottom_text=DEFAULT_BOTTOM_TEXT,
            created_by=cls.user,
        )
        cls.second_meme = Meme.objects.create(
            template=cls.template,
            top_text=DEFAULT_TOP_TEXT,
            created_by=cls.user,
        )
        cls.base_name = "meme"

    def test_list(self) -> None:
        time_obj = datetime.strptime(DEFAULT_TIME, '%Y-%m-%dT%H:%M:%S.%fZ')
        formatted_time_str = time_obj.strftime('%Y-%m-%dT%H:%M:%SZ')

        assert self.list() == [
            {
                "id": self.first_meme.id,
                "template": self.template.id,
                "top_text": self.template.default_top_text,
                "bottom_text": DEFAULT_BOTTOM_TEXT,
                "created_by": self.user.id,
                "created_at": formatted_time_str,
                "image_url": self.get_meme_image_url(top_text=self.template.default_top_text),
            },
            {
                "id": self.second_meme.id,
                "template": self.template.id,
                "top_text": DEFAULT_TOP_TEXT,
                "bottom_text": self.template.default_bottom_text,
                "created_by": self.user.id,
                "created_at": formatted_time_str,
                "image_url": self.get_meme_image_url(bottom_text=self.template.default_bottom_text),
            },
        ]

    def create_meme(self, data: dict) -> dict:
        return self.create(data)

    def test_create(self) -> None:
        meme = self.create_meme(
            {
                "template": self.template.id,
                "top_text": DEFAULT_TOP_TEXT,
                "bottom_text": DEFAULT_BOTTOM_TEXT,
                "created_by": self.user.id,
            },
        )
        time_obj = datetime.strptime(DEFAULT_TIME, '%Y-%m-%dT%H:%M:%S.%fZ')
        formatted_time_str = time_obj.strftime('%Y-%m-%dT%H:%M:%SZ')

        assert meme == {
                "id": meme["id"],
                "template": self.template.id,
                "top_text": DEFAULT_TOP_TEXT,
                "bottom_text": DEFAULT_BOTTOM_TEXT,
                "created_by": self.user.id,
                "created_at": formatted_time_str,
                "image_url": self.get_meme_image_url(),
            }

    def test_retrieve(self) -> None:
        created_meme = self.create_meme(
            {
                "template": self.template.id,
                "top_text": DEFAULT_TOP_TEXT,
                "bottom_text": DEFAULT_BOTTOM_TEXT,
                "created_by": self.user.id,
                "image_url": self.get_meme_image_url(),
            },
        )

        meme = self.retrieve(created_meme)

        assert meme == created_meme
