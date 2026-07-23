import logging
from django.db import models

logger = logging.getLogger(__name__)

class Word(models.Model):
    word = models.CharField(max_length=32)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["word"]

    def __init__(self, word: str, active = True):
        self.word = word
        self.active = active

    def __str__(self):
        return f"{self.word}"
    

class WordSet(models.Model):
    name = models.CharField(max_length=24, unique=True)
    words = models.ManyToManyField(Word, blank=True)
    num_chars = models.PositiveIntegerField(default=0)
    num_words = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["name"]

    def __init__(self, name: str, words: list[str]):
        self.name = name
        # Define words (many to many field)
        self.init_word_relations(words)
        self.num_chars = get_num_chars(words)
        self.num_words = len(words)


    def __str__(self):
        return f"{self.name} ({self.num_words} words)"


    def init_word_relations(self, words: list[str]) -> None:
        for word in words:
            try:
                # Existing word
                fetched_word = Word.objects.get(word=word)
                self.words.add(fetched_word)
                logger.debug("added fetched words")
            except Word.DoesNotExist:
                # New Word
                new_word = Word(word=word)
                new_word.save()
                self.words.add(new_word)
                logger.debug("added new word")
            except:
                logger.warning("an error occurred when initializing wordset relations")

def get_num_chars(words: list[str]) -> int:
    num: int = 0
    for word in words:
        num += len(word)
    return num