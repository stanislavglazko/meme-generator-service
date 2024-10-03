from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from meme_generator.models import MemeTemplate
from meme_generator.serializers import TemplateListSerializer


class TemplatesViewsSet(ListModelMixin, GenericViewSet):
    serializer_class = TemplateListSerializer
    queryset = MemeTemplate.objects.order_by("id")
    swagger_tags = ["templates"]
