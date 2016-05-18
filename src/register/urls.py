from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.search, name='search_page'),
    url(r'^apostille/(?P<id>[0-9]+)$', views.apostille_detail, name='apostille_detail'),
]