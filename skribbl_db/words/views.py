import logging
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader

from .models import Word, WordSet
from .forms import NewWordForm, NewWordSetForm

logger = logging.getLogger(__name__)

def words(request):
    if request.method == 'POST':
        form = NewWordForm(request.POST)
        if form.is_valid():
            form.save()
            word_data = Word.objects.all().values()
            list_html = loader.render_to_string('_word_list.html', {'word_data': word_data}, request=request)
            return JsonResponse({'success': True, 'list_html': list_html})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    else:
        form = NewWordForm(initial={'word': ''})
    
    word_data = Word.objects.all().values()
    template = loader.get_template('all_words.html')
    context = {
        'word_data': word_data,
        'form': form
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

def wordsets(request, id):    
    word_data = WordSet.objects.get(id=id).words.all()
    wordset_data = WordSet.objects.all().values()
    template = loader.get_template('wordsets.html')
    context = {
        'word_data': word_data,
        'wordset_data': wordset_data,
    }
    return HttpResponse(template.render(context, request))

def new_wordset(request):
    if request.method == 'POST':
        form = NewWordSetForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/wordsets/{form.instance.id}')
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    else:
        form = NewWordSetForm(initial={'name': '', 'words': ''})

    template = loader.get_template('new_wordset.html')
    context = {'form': form}
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