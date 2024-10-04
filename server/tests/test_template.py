from typing import Final

from meme_generator.models import MemeTemplate
from .base import TestViewSetBase, DEFAULT_TOP_TEXT, DEFAULT_BOTTOM_TEXT

TEMPLATE_NAME: Final[str] = "Template 2"


class TestMemeTemplateViewSet(TestViewSetBase):
    base_name: str

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.second_template = MemeTemplate.objects.create(
            name=TEMPLATE_NAME,
            image=cls.image,
            default_top_text=DEFAULT_TOP_TEXT,
            default_bottom_text=DEFAULT_BOTTOM_TEXT
        )
        cls.base_name = "template"

    def test_list(self) -> None:
        assert self.list() == [
            {
                "id": self.template.id,
                "name": self.template.name,
                "image_url": self.template.image_url,
                "default_top_text": self.template.default_top_text,
                "default_bottom_text": self.template.default_bottom_text,
            },
            {
                "id": self.second_template.id,
                "name": TEMPLATE_NAME,
                "image_url": self.second_template.image_url,
                "default_top_text": self.second_template.default_top_text,
                "default_bottom_text": self.second_template.default_bottom_text,
            }
        ]
