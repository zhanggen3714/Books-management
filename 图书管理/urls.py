"""图书管理 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01.views import *
from django.conf.urls import url,include
urlpatterns = [
    url(r'^ul/',include('app01.urls')),
    url(r'^$',log_in),
    url(r'^login/',log_in),
    url(r'^regist/',register),
    url(r'^set_password/',set_password),
    url(r'^logout/',logout),
    url(r'^index/',index),
    url(r'^addbook/',addbook),
    url(r'^delbook/',delbook),
    url(r'^editbook/',editbook),
    url(r'^query/',query),
    url(r'^orm/',ormadd),
    url(r'^ormquery/',ormquery),
    url(r'^queryset/',queryset),
    url(r'^relationQueryset/',relation),
    url(r'^relationQueryset/',relation),
    url(r'^aggregate/',aggregate_annotate),
    url(r'^fandq/',FandQ),
]
