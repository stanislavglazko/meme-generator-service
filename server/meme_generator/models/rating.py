from django.db import models
from django.contrib.auth.models import User

from .meme import Meme

MIN_SCORE = 1
MAX_SCORE = 5


class Rating(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(MIN_SCORE, MAX_SCORE+1)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('meme', 'user')
