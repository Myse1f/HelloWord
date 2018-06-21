# coding:utf-8
from django.shortcuts import render, render_to_response, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserForm, SettingsForm, NoteForm
from .models import User, UserMore, Vocabulary, UserWord, Task, Word, Note
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def page_not_found(request):
    return render_to_response('404.html')

def index_view(request):
    if request.user.is_authenticated():
        usermore = get_object_or_404(UserMore, user=request.user)
        context = {'usermore': usermore}
        # return the view and model
        return render(request, "words/index.html", context=context)
    else:
        return return render(request, "words/index.html")

def register_view(self):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("words:indexview"))
    else:
        if request.method == 'POST':
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            daily_words = form.cleaned_data['daily_words']
            vocabulary_id = form.cleaned_data['vocabulary']
            vocabulary = Vocabulary.objects.get(id=vocabulary_id)
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            usermore = UserMore.objects.create(user=user)
            usermore.vocabulary = vocabulary
            add_list = []
            for word in vocabulary.words.all():
                add_list.append(UserWord(word=word, user=usermore, vocabulary=vocabulary))
            UserWord.objects.bulk_create(add_list) # bulk add userword
            usermore.daily_words = daily_words
            task = Task.objects.create(user=usermore, date=datetime.today().date())
            task.new_task()
            usermore.save() # register user info
            login(request. user)
            return HttpResponseRedirect(reverse("words:indexview"))
        # get register view
        else:
            form = UserForm()
        return render(request, 'words/register.html', context={ 'form': form })