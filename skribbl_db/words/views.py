from django.http import HttpResponse
from django.template import loader

from .models import Word
from .forms import NewWordForm

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

def new_word(request):
    if request.method == 'POST':
        form = NewWordForm(request.POST)
        
        if form.is_valid():
            word = Word(word=form.cleaned_data['word'], active=True)
            word.save()
    else:
        form = NewWordForm(initial={'word': ''})

    context = {
        'form': form
    }

    template = loader.get_template('new_word.html')
    return HttpResponse(template.render(context, request))