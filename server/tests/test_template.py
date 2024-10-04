from meme_generator.models import MemeTemplate
from .base import TestViewSetBase, DEFAULT_TOP_TEXT, DEFAULT_BOTTOM_TEXT


class TestMemeTemplateViewSet(TestViewSetBase):
    base_name: str

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.second_template = MemeTemplate.objects.create(
            name="Template 2",
            image_url="https://example.com/template2.jpg",
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
                "name": self.second_template.name,
                "image_url": self.second_template.image_url,
                "default_top_text": self.second_template.default_top_text,
                "default_bottom_text": self.second_template.default_bottom_text,
            }
        ]
