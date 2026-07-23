from rest_framework import serializers
from words.models import Word, WordSet


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'

class WordSetSerializer(serializers.ModelSerializer):
    words = WordSerializer(many=True) # many-to-many
    words_data = serializers.CharField(max_length=5000)

    class Meta:
        model = WordSet
        fields = ['name', 'words']

    def create(self, validated_data):
        words_data = validated_data.get('words_data')
        word_set = WordSet.objects.create(**validated_data)
        