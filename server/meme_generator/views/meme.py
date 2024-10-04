import random
from typing import Any

from django.db.models import Avg
from django.db.models.query import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet, ViewSet

from meme_generator.models import Meme
from meme_generator.serializers import MemeSerializer
from meme_generator.services import SurpriseMeService

TOP_MEMES_NUMBER: int = 10


class MemeViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = MemeSerializer
    queryset = Meme.objects.order_by("id")
    swagger_tags = ["memes"]


class RandomMemeViewSet(ViewSet):
    swagger_tags = ["random_meme"]

    @swagger_auto_schema(
        responses={200: MemeSerializer()},
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        meme_count = Meme.objects.count()
        if meme_count == 0:
            return Response({"detail": "No memes available"}, status=404)
        random_index = random.randint(0, meme_count - 1)
        meme = Meme.objects.all()[random_index]
        serializer = MemeSerializer(meme)
        return Response(serializer.data)


class TopMemesViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MemeSerializer
    swagger_tags = ["top_memes"]

    def get_queryset(self) -> QuerySet:
        return Meme.objects.annotate(
            average_rating=Avg("ratings__score")
        ).order_by("-average_rating", "id")[:TOP_MEMES_NUMBER]


class SurpriseMeViewSet(ViewSet):
    serializer_class = MemeSerializer
    swagger_tags = ["surprise_me"]

    def list(self, request):
        meme = SurpriseMeService.create_surprise(user=request.user)
        serializer = self.serializer_class(meme)
        return Response(serializer.data)
