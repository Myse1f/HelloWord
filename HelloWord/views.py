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