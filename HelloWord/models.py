# coding:utf-8

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

#word
class Word(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.TextField(default='')
    example = models.TextField(default='')
    vocabularys = models.ManyToManyField('Vocabulary', related_name='words')

    def __str__(self):
        return self.name

#user
class UserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_words = models.IntegerField(default=50)
    vocabulary = models.ForeignKey('Vocabulary', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

    # words which not be learned
    def unfininshed_count(self):
        return self.words.filter(learntimes__lt=1, vocabulary=self.vocabulary).count()

    # words which have master
    def finished_count(self):
        return self.words.filter(learntimes__gte=5, vocabulary=self.vocabulary).count()

    # words which have learned but not master
    def learned_count(self):
        return self.words.filter(learntimes__gte=1, vocabulary=self.vocabulary).count()

#user
class Note(models.Model):
    content = models.TextField()
    shared = models.BooleanField(default=True)
    user = models.ForeignKey('UserMore', on_delete=models.CASCADE, related_name='notes', null=True)
    word = models.ForeignKey('Word', on_delete=models.CASCADE, related_name='wordnotes', null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
    
    def update(self):
        self.date = timezone.now()

#Recite Vocabulary
class Vocabulary(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

#User's words need to be recited
class UserWord(models.Model):
    words = models.ForeignKey('Word', on_delete=models.CASCADE)
    user = models.ForeignKey('UserMore', on_delete=models.CASCADE, related_name='words')
    vocabulary = models.ForeignKey('Vocabulary', on_delete=models.CASCADE, related_name='vocabularywords')
    learntimes = models.IntegerField(default=0) #a word need to be recited 5 times
    task = models.ForeignKey(
        'Task',
        related_name='taskwords',
        null=True,
        on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.word.name

    def update(self):
        self.date = timezone.now()

    def name(self):
        return self.word.name
    
    def explanation(self):
        return self.word.explanation

    def example(self):
        return self.word.example

    def learn(self):
        self.learntimes += 1
        self.update()
        self.save()

    def unknow(self):
        self.learntimes = 0
        self.update()
        self.save()
    
    def master(self):
        self.learntimes = 5
        self.update()
        self.save()

#every day task
class Task(models.Model):
    user = models.OneToOneField(
        'UserMore',
        on_delete=models.CASCADE,
        related_name='task')
    date = models.DateField(null=True)

    # words that user haven't master
    def user_allcount(self):
        return self.user.words.filter(learntimes__lt=5, vocabulary=self.user.vocabulary).count()

    # the number of word every day task 
    def today_task_count(self):
        return self.taskwords.count()

    # new a task
    def new_task(self):
        self.date = datetime.today().date()
        count = self.user.words.filter(learntimes__lt=5, vocabulary=self.user.vocabulary).count()
        if count < self.user.daily_words:
            words = self.user.words.filter(learntimes__lt=5, vocabulary=self.user.vocabulary).order_by('?')[:count]
            for word in words:
                word.task = self
                word.save()
        else:
            words = self.user.words.filter(learntimes__lt=5, vocabulary=self.user.vocabulary).order_by('?')[:self.user.daily_words]
            for word in words:
                word.task = self
                word.save()

    # update task every day
    def update_task(self):
        if self.date < datetime.today().date():
            self.newtask()
            self.save()