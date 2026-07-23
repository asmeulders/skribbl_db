import logging
from django.db import models

logger = logging.getLogger(__name__)

class Word(models.Model):
    word = models.CharField(max_length=32, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["word"]

    def __str__(self):
        return f"{self.word}"
    

class WordSet(models.Model):
    name = models.CharField(max_length=24, unique=True)
    words = models.ManyToManyField(Word, blank=True)
    num_chars = models.PositiveIntegerField(default=0)
    num_words = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["name"]

    @classmethod
    def create_with_words(cls, name: str, words: list[str]) -> "WordSet":
        obj = cls.objects.create(name=name, num_chars=get_num_chars(words), num_words=len(words))
        obj.init_word_relations(words)
        return obj

    def init_word_relations(self, words: list[str]) -> None:
        for word in words:
            try:
                word_obj, created = Word.objects.get_or_create(word=word)
                self.words.add(word_obj)
                logger.debug(f"added word: {word} - created: {created}")
            except:
                logger.error("an error occurred when initializing wordset relations")

    def __str__(self):
            return f"{self.name} ({self.num_words} words)"

def get_num_chars(words: list[str]) -> int:
    num: int = 0
    for word in words:
        num += len(word)
    return num