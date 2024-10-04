import random
from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet, ViewSet

from meme_generator.models import Meme
from meme_generator.serializers import MemeSerializer


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
