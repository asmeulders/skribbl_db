from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WordSerializer
from rest_framework import status

from words.models import Word


class WordsView(APIView):
    """
    List all words, or create a new word.
    """
    def get(self, request):
        items = Word.objects.all()
        serializer = WordSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WordDetail(APIView):
    """
    Retrieve, update or delete a word instance.
    """

    def get_object(self, id):
        try:
            return Word.objects.get(id=id)
        except Word.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        word = self.get_object(id)
        serializer = WordSerializer(word)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        word = self.get_object(id)
        serializer = WordSerializer(word, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        word = self.get_object(id)
        word.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)