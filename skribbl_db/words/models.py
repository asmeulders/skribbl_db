from django.db import models

# Create your models here.
class Word(models.Model):
    word = models.CharField(max_length=32)
    active = models.BooleanField()

    def __str__(self):
        return f"{self.word}"