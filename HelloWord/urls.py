# coding:utf-8
"""HelloWord URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.index_view, name='indexview'),
    re_path(r'^login/$', views.login_view, name='loginview'),
    re_path(r'^logout/$', views.logout_view, name='logoutview'),
    re_path(r'^register/$', views.register_view, name='registerview'),
    re_path(r'settings/$', views.settings_view, name='setting_view'),
    re_path(r'^task/$', views.task_view, name='taskview'),
    re_path(r'^mynotes/$', views.mynotes_view, name='mynotesview'),
    re_path(r'^detail/(?P<word_id>\d+)$', views.detail_view, name='detailview'),
    re_path(r'^notes/(?P<word_id>\d+)$', views.notes_view, name='notesview'),
    re_path(r'^editnote/(?P<word_id>\d+)$', views.editnote_view, name='editnoteview'),
    re_path(r'^deletenote/(?P<word_id>\d+)$', views.deletenote_view, name='deletenoteview'),
    re_path(r'^moretask/$', views.moretask_view, name='moretaskview')
]

handler404 = "views.page_not_found"
