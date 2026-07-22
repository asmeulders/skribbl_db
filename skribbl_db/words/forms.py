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

class NewWordSetForm(forms.Form):
    name = forms.CharField(max_length=24)
    custom_words = forms.CharField(widget=forms.Textarea)

    def clean_custom_words(self):
        logger.debug("clean custom_words")
        data = self.cleaned_data['custom_words']

        try:
            assert isinstance(data, str)
        except AssertionError:
            raise ValidationError("Invalid input: custom_words but be a string.")

        word_list = make_word_list_from_input(data)
        self.cleaned_data['word_list'] = word_list
        
        return ','.join(word_list)
        

def make_word_list_from_input(data: str):
    # Remove padded spaces
    data = data.strip()

    # Separate into a list by commas
    return [clean_single_word_input(word) for word in data.split(',')]
    

def clean_single_word_input(data: str):
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