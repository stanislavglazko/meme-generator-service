from rest_framework.serializers import ModelSerializer


from meme_generator.models import Meme


class MemeSerializer(ModelSerializer):
    class Meta:
        model = Meme
        fields = [
            "id",
            "template",
            "top_text",
            "bottom_text",
            "created_by",
            "created_at"
        ]
