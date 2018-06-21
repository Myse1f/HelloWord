from django.contrib import admin

from .models import UserMore, Word, Vocabulary, Note, UserWord, Task

admin.site.register(UserMore)
admin.site.register(UserWord)
admin.site.register(Note)
admin.site.register(Vocabulary)
admin.site.register(Word)
admin.site.register(Task)