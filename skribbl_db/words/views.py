from django.http import HttpResponse
from django.template import loader

from .models import Word

def words(request):
    all_words = Word.objects.all().values()
    template = loader.get_template('all_words.html')
    context = {
        'all_words': all_words
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    word = Word.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'word': word,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],   
  }
  return HttpResponse(template.render(context, request))