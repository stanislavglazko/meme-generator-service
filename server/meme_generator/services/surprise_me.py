import random

from meme_generator.models import Meme, MemeTemplate


FUNNY_PHRASES = [
    "Why so serious?",
    "I'm not lazy, I'm on energy-saving mode.",
    "Do not disturb, I'm disturbed enough already.",
    "I'm not arguing, I'm just explaining why I'm right."
]


class SurpriseMeService:
    @classmethod
    def create_surprise(cls, user) -> Meme:
        template = cls.get_template()
        top_text = cls.create_text()
        bottom_text = cls.create_text()
        return cls.create_meme(
            template,
            top_text,
            bottom_text,
            user
        )

    @classmethod
    def get_template(cls) -> MemeTemplate:
        meme_template_count = MemeTemplate.objects.count()
        random_index = random.randint(0, meme_template_count - 1)
        return MemeTemplate.objects.all()[random_index]

    @classmethod
    def create_text(cls) -> str:
        return random.choice(FUNNY_PHRASES)

    @classmethod
    def create_meme(cls, template: MemeTemplate, top_text: str, bottom_text: str, user) -> Meme:
        return Meme.objects.create(
            template=template,
            top_text=top_text,
            bottom_text=bottom_text,
            created_by=user,
        )
