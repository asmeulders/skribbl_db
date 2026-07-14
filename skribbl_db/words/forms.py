from django import forms
from django.core.exceptions import ValidationError

from .models import Word

class NewWordForm(forms.ModelForm):
    # word = forms.CharField(help_text="Enter a word to be used in Skribbl.io.", 
    #                        min_length=1, max_length=32)
    
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

        # all lowercase
        data = data.lower()

        return data
        

