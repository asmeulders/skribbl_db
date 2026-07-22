from django.db import models

# Create your models here.
class Word(models.Model):
    word = models.CharField(max_length=32)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["word"]

    def __str__(self):
        return f"{self.word}"
    

class WordSet(models.Model):
    name = models.CharField(max_length=24, unique=True)
    num_chars = models.PositiveIntegerField(default=0)
    num_words = models.PositiveIntegerField(default=0)
    words = models.ManyToManyField(Word, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.num_words} words)"