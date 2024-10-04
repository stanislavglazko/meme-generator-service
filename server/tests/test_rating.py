from freezegun import freeze_time
from http import HTTPStatus
from meme_generator.models import Meme, MemeTemplate

from .base import TestViewSetBase, DEFAULT_TIME, INCORRECT_MEME_ID, INCORRECT_SCORE


@freeze_time(DEFAULT_TIME)
class TesRatingViewSet(TestViewSetBase):
    base_name: str
    template: MemeTemplate

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.meme = Meme.objects.create(
            template=cls.template,
            created_by=cls.user,
        )
        cls.base_name = "rating"

    def create_rating(self, data: dict, args: list = None) -> dict:
        return self.create(data, args)

    def test_create_or_update(self) -> None:
        rating = self.create_rating(
            {
                "score": 4,
            },
            [self.meme.pk]
        )

        assert rating == {
            "score": 4,
        }

        response = self.request_create(
            {
                "score": 3,
            },
            [self.meme.pk]
        )
        assert response.status_code == HTTPStatus.OK

        assert response.json() == {
            "score": 3,
        }

    def test_incorrect_meme(self) -> None:
        response = self.request_create(
            {
                "score": 3,
            },
            [INCORRECT_MEME_ID]
        )

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_incorrect_score(self) -> None:
        response = self.request_create(
            {
                "score": INCORRECT_SCORE,
            },
            [self.meme.pk]
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
