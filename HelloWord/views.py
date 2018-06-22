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
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            daily_words = form.cleaned_data['daily_words']
            vocabulary_id = form.cleaned_data['vocabulary']
            vocabulary = Vocabulary.objects.get(id=vocabulary_id)
            user = User.objects.create_user(username=username, email=email, password=password1)
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

def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("words:indexview"))
    else:
        # login
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse("words:indexview"))
                else:
                    error_message = 'Username or password is invalid'
                    return render(request, 'words/login.html', context={
                        'error_message': error_message,
                        'form': form})
            else:
                form = LoginForm()
            return render(request, 'words/login.html', context={'form': form})

@login_required
def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse("words:indexview"))

@login_required
def settings_view(request):
    usermore = get_object_or_404(UserMore, user=request.user)
    data = {
        'vocabulary': usermore.vocabulary.id,
        'daily_words': usermore.daily_words
    }
    form = SettingsForm(initial=data)
    if request.method == 'POST':
        form = SettingsForm(request.POST):
        if form.is_valid():
            daily_words = form.cleaned_data['daily_words']
            vocabulary_id = form.cleaned_data['vocabulary']
            vocabulary = Vocabulary.objects.get(id=vocabulary_id)
            # setting is the same
            if usermore.vocabulary == vocabulary and usermore.daily_words == daily_words:
                pass
            # set the daily words need to be recited
            elif usermore.vocabulary == vocabulary:
                usermore.daily_words = daily_words
                usermore.save()
            # set vocabulary and daily words
            else:
                usermore.vocabulary = vocabulary
                add_list = []
                word = vocabulary.words.all()[0]
                # judge if the vocabulary is in the list
                if not UserWord.objects.filter(word=word, user=usermore, vocabulary=vocabulary).exists():
                    for word in vocabulary.words.all():
                        add_list.append(UserWord(word=word, user=usermore, vocabulary=vocabulary))
                    #bulk import
                    UserWord.objects.bulk_create(add_list)
                usermore.daily_words = daily_words
                usermore.task.updatetask()
                usermore.save() #save the model
            return HttpResponseRedirect(reverse("words:indexview"))
        else:
            return HttpResponseRedirect(reverse("words:settingsview"))
    # GET
    else:
        return render(request, 'words/settings.html', context={'form': form})

@login_required
def task_view(request):
    usermore = UserMore.objects.get(user=request.user)
    task = usermore.task
    # remember to update the task every time come in this veiw
    task.updatetask()
    # the vocabulary is finished
    if task.user_allcount() == 0:
        message = 'This vocabulary is finished! Go and change the vocabualry'
        context = {'usermore': usermore, 'message': message}
        return render(request, "words/index.html", context=context)
    
    if task.today_task_count() == 0:
        message = 'Task today is finished! Want one more task? Click Here!'
        context = {'usermore': usermore, 'message': message}
        return render(request, "words/index.html", context=context)
    taskword = task.taskwords.all().order_by('date')[0]
    if request.method == 'GET':
        return render(request, 'words/task.html', context={
            'taskword': taskword,
            'usermore': usermore,
            'todaytaskcount': task.today_task_count()
        })
    elif request.method == 'POST':
        word_id = taskword.word.id
        # user konw this word, learntime + 1
        if request.POST.get('know', False):
            taskword.learn()
            task.taskwords.remove(taskword)
            task.save()
            return HttpResponseRedirect(reverse("words:detailview", args=[word_id]))
        # user master this word1
        if request.POST.get('master', False):
            taskword.master()
            task.taskwords.remove(taskword)
            task.save()
            return HttpResponseRedirect(reverse("words:detailview", args=[word_id]))
        # user do not know this word, don't remove it from task
        if request.POST.get('unknow', False):
            taskword.unknow()
            task.save()
            return HttpResponseRedirect(reverse("words:detailview", args=[word_id]))
        return HttpResponseRedirect(reverse("words:indexview"))

@login_required
def mynotes_view(request):
    usermore = UserMore.objects.get(user=request.user)
    # '-' means that ordert descendently
    mynotes = usermore.notes.all().order_by('-date')
    context = {'mynotes': mynotes, 'usermore': usermore}
    if not mynotes.exists():
        message = 'You have no notes'
        context['message'] = message
        return render(request, "words/mynotespage.html", context=context)
    paginator = Paginator(mynotes, 4)
    page = request.GET.get('page')

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        # page is not integer, return page 1
        notes = paginator.page(1)
    except EmptyPage:
        # page is oversize, return the last page
        notes = paginator.page(paginator.num_pages)
    
    context = {'notes': notes, 'usermore': usermore}
    return render(request, 'words/mynotespage.html', context=context)

@login_required
def detail_view(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    if request.method == 'POST':
        if request.POST.get('go', False):
            return HttpResponseRedirect(reverse('words:taskview'))
        if request.POST.get('note', False):
            return HttpResponseRedirect(reverse('words:notesview', args=[word_id]))
    return render(request, 'words/word.html', context={'word': word})

@login_required
def notes_view(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    notes = Note.objects.filter(word=word).filter(shared=True)
    usermore = UserMore.objects.get(user=request.user)
    # the note is exist, edit it
    try:
        note = Note.objects.filter(user=usermore, word=word)[0]
        data = {'content': note.content, 'shared': note.shared}
        form = NoteForm(initial=data)
        if request.method == 'POST':
            form = NoteForm(request.POST)
            if form.is_valid():
                note.content = form.cleaned_data['content']
                note.shared = form.cleaned_data['shared']
                note.update()
                note.save()
                return HttpResponseRedirect(reverse("words:detailview", args=[word_id]))
    # new note
    except:
        form = NoteForm()
    if request.method == 'POST':
        if request.POST.get('note', False):
            form = NoteForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                shared = form.cleaned_data['shared']
                Note.objects.create(
                    content=content,
                    shared=shared,
                    word=word,
                    user=usermore)
                return HttpResponseRedirect(reverse("words:detailview", args=[word_id]))
    
    # GET
    context = {'notes': notes, 'word': word, 'form': form}
    return render(request, 'words/notes.html', context=context)

@login_required
def editnote_view(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    usermore = UserMore.objects.get(user=request.user)
    notes = Note.objects.filter(word=word).filter(shared=True)
    note = Note.objects.filter(user=usermore, word=word)[0]
    data = {'content': note.content, 'shared': note.shared}
    form = NoteForm(initial=data)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note.content = form.cleaned_data['content']
            note.shared = form.cleaned_data['shared']
            note.update()
            note.save()
            return HttpResponseRedirect(reverse('words:mynotesview'))
    else:
        context = {'notes': notes, 'form': form, 'word': word}
        return render(request, 'words/editnote.html', context=context)

@login_required
def moretask_view(request):
    usermore = UserMore.objects.get(user=request.user)
    task = usermore.task
    task.new_task()
    return HttpResponseRedirect(reverse('words:taskview'))

@login_required
def deletenoteview(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    usermore = UserMore.objects.get(user=request.user)
    note = Note.objects.filter(user=usermore, word=word)[0]
    note.delete()
    return HttpResponseRedirect(reverse('words:mynotesview'))