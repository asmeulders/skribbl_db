from rest_framework import serializers
from words.models import Word, WordSet


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'

class WordSetSerializer(serializers.ModelSerializer):
    words = serializers.CharField(max_length=5000, read_only=True)
    
    class Meta:
        model = WordSet
        fields = ['name', 'words']