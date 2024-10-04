
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from meme_generator.models import Meme, Rating
from meme_generator.serializers import RatingSerializer


class RatingViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = RatingSerializer
    swagger_tags = ["rating"]

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        meme = get_object_or_404(Meme, pk=self.kwargs.get('meme_pk'))
        user = self.request.user
        score = request.data.get('score')

        rating, created = Rating.objects.update_or_create(
            meme=meme,
            user=user,
            defaults={'score': score}
        )
        headers = self.get_success_headers(serializer.data)

        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
