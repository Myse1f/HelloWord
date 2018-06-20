#coding:utf-8

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

    def __str__(sef)
        return self.name

#user
class UserMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_words = models.IntegerField(default=50)
    vocabulary = models.ForeignKey('Vocabulary', null=true)

    def __str__(self):
        return self.user.username

    # words which not be learned
    def unfininshedcount(self):
        return self.words.filter(learntimes__lt=1, vocabulary=self.vocabulary).count()
