from rest_framework.serializers import ModelSerializer


from meme_generator.models import MemeTemplate


class TemplateListSerializer(ModelSerializer):
    class Meta:
        model = MemeTemplate
        fields = [
            "id",
            "name",
            "image_url",
            "default_top_text",
            "default_bottom_text",
        ]
