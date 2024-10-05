from django.db import models


class MemeTemplate(models.Model):
    name = models.CharField(max_length=100)
    default_top_text = models.CharField(max_length=100, blank=True)
    default_bottom_text = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="templates/", null=True, blank=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ''
