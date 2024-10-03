from django.db import models
from django.contrib.auth.models import User

from .template import MemeTemplate


class Meme(models.Model):
    template = models.ForeignKey(MemeTemplate, on_delete=models.CASCADE)
    top_text = models.CharField(max_length=100)
    bottom_text = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.top_text:
            self.top_text = self.template.default_top_text
        if not self.bottom_text:
            self.bottom_text = self.template.default_bottom_text
        super().save(*args, **kwargs)
