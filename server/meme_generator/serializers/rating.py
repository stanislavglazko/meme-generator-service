from rest_framework.serializers import ModelSerializer


from meme_generator.models import Rating


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score']
