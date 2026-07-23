import logging
from django import forms
from django.core.exceptions import ValidationError

from .models import Word, WordSet

logger = logging.getLogger(__name__)

class NewWordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['word']
        widgets = {
            'word': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter word here...'
            })
        }

    def clean_word(self):
        data = self.cleaned_data['word']

        try:
            assert isinstance(data, str)
        except AssertionError:
            raise ValidationError("Invalid word: Must be a string.")

        return clean_single_word_input(data)

class NewWordSetForm(forms.ModelForm):
    words = forms.CharField(
        required=False,
        help_text="Comma-separated",
        widget=forms.Textarea(attrs={'placeholder': 'place, words, here'})
    )

    class Meta:
        model = WordSet
        fields = ['name']

    def clean_words(self) -> list[str]:
        logger.debug("clean words")
        raw = self.cleaned_data['words']

        try:
            assert isinstance(raw, str)
        except AssertionError:
            raise ValidationError("Invalid input: words but be a string.")

        return [clean_single_word_input(word) for word in raw.split(',') if word.strip()]

    def save(self, commit=True) -> "WordSet":
        instance = super().save(commit=commit)
        if commit:
            self._save_words(instance)
        return instance

    def save_m2m(self) -> None:
        self._save_words(self.instance)

    def _save_words(self, instance) -> None:
        words = [Word.objects.get_or_create(word=word)[0] for word in self.cleaned_data['words']]
        instance.words.set(words)

def clean_single_word_input(data: str) -> str:
    # Remove padded spaces
    data = data.strip()

    # no special characters outside of spaces and hyphens '-'
    if not data.isalnum():
        special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '=', '+', '[', ']',
                                '{', '}', '\\', '|', '<', '>', '.', '/', '?', '~', '`']
        for char in special_characters:
            if data.find(char) != -1:
                raise ValidationError("Invalid word: No special characters besides spaces and hyphens, '-'.")

    # at least 1 character, at most 32
    if len(data) < 1 or len(data) > 32:
        raise ValidationError("Invalid word: Length must be between 1 and 32.")  

    # Make list of all spaces
    indices = []
    start = 0
    index = data.find(' ')
    while index != -1:
        indices.append(index)
        data = data[start] + data[start+1:index].lower() + data[index:]
        start = index + 1
        index = data.find(' ', start)

    return data