from freezegun import freeze_time

from meme_generator.models import Meme, MemeTemplate, Rating
from meme_generator.views import TOP_MEMES_NUMBER

from .base import TestViewSetBase, DEFAULT_TIME


@freeze_time(DEFAULT_TIME)
class TestTopMemesViewSet(TestViewSetBase):
    base_name: str
    template: MemeTemplate

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.base_name = "top-memes"

    def test_list(self) -> None:
        meme_without_rating = Meme.objects.create(
                template=self.template,
                created_by=self.user,
            )
        low_rated_memes_ids = set()
        for i in range(2):
            low_rated_meme = Meme.objects.create(
                template=self.template,
                created_by=self.user,
            )
            Rating.objects.create(
                meme=low_rated_meme,
                user=self.user,
                score=1,
            )
            low_rated_memes_ids.add(low_rated_meme.id)

        top_memes = self.list()

        top_memes_ids = {meme["id"] for meme in top_memes}
        assert meme_without_rating.id not in top_memes_ids
        assert top_memes_ids == low_rated_memes_ids

        high_rated_memes_ids = set()
        for i in range(10):
            high_rated_meme = Meme.objects.create(
                template=self.template,
                created_by=self.user,
            )
            Rating.objects.create(
                meme=high_rated_meme,
                user=self.user,
                score=5,
            )
            high_rated_memes_ids.add(high_rated_meme.id)

        top_memes = self.list()

        assert len(top_memes) == TOP_MEMES_NUMBER
        top_memes_ids = {meme["id"] for meme in top_memes}
        assert top_memes_ids == high_rated_memes_ids
