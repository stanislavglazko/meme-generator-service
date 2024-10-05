import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from .template import MemeTemplate


def fit_text_to_image(text: str, max_width: int, draw: ImageDraw, font: ImageFont) -> str:
    lines = []
    current_line = ""
    for word in text.split():
        test_line = f"{current_line} {word}".strip()
        text_width = draw.textbbox((0, 0), test_line, font=font)[2]
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)


class Meme(models.Model):
    template = models.ForeignKey(MemeTemplate, on_delete=models.CASCADE)
    top_text = models.CharField(max_length=100, blank=True)
    bottom_text = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.top_text:
            self.top_text = self.template.default_top_text
        if not self.bottom_text:
            self.bottom_text = self.template.default_bottom_text

        if not self.pk and self.template.image:
            img = Image.open(self.template.image.path)
            draw = ImageDraw.Draw(img)

            width, height = img.size

            font_size = int(height / 10)
            font = ImageFont.load_default(font_size)

            max_width = width - 20
            top_text = self.top_text or self.template.default_top_text
            bottom_text = self.bottom_text or self.template.default_bottom_text

            top_text = fit_text_to_image(top_text, max_width, draw, font)
            top_text_position = (10, height // 8)
            draw.text(top_text_position, top_text, font=font, fill='white')

            bottom_text = fit_text_to_image(bottom_text, max_width, draw, font)
            bottom_text_position = (10, height - (height // 4))
            draw.text(bottom_text_position, bottom_text, font=font, fill='black')

            unique_filename = f"meme_{self.template.id}_{top_text[:3]}_{bottom_text[:3]}.jpg"
            relative_path = os.path.join('generated_memes', unique_filename)
            image_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            Path(os.path.dirname(image_path)).mkdir(parents=True, exist_ok=True)
            img.save(image_path)
            self.image_url = os.path.join(settings.MEDIA_URL, relative_path)

        super().save(*args, **kwargs)
