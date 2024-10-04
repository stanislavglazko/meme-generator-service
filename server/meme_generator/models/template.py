from django.db import models


class MemeTemplate(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    default_top_text = models.CharField(max_length=100, blank=True)
    default_bottom_text = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="templates/", null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        self.image_url = self.image.url
        super().save(*args, **kwargs)
