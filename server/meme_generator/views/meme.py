from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from meme_generator.models import Meme
from meme_generator.serializers import MemeSerializer


class MemeViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = MemeSerializer
    queryset = Meme.objects.order_by("id")
    swagger_tags = ["templates"]
