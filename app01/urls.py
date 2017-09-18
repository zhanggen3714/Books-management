from app01.views import *
from django.conf.urls import url,include
urlpatterns = [
    url(r'^menu/author/$',menu_author),
    url(r'^menu/author/add/$',menu_author_add),
    url(r'^menu/author/edit/$',menu_author_edit),
    url(r'^menu/author/del/$',menu_author_del),

    url(r'^menu/publish/$',menu_publish),
    url(r'^menu/publish/add/$',menu_publish_add),
    url(r'^menu/publish/edit/$',menu_publish_edit),
    url(r'^menu/publish/del/$',menu_publish_del),

    url(r'^menu/classify/$',menu_classify),
    url(r'^menu/classify/add/$',menu_classify_add),
    url(r'^menu/classify/edit/$',menu_classify_edit),
    url(r'^menu/classify/del/$',menu_classify_del),

    ]