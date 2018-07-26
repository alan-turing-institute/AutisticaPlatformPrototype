from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^complete/?$', views.complete, name='complete'),
    url(r'^logout/?$', views.logout_user, name='logout'),
    url(r'^overview/?$', views.overview, name='overview'),
    url(r'^upload/?$', views.upload, name='upload'),
    url(r'^list/?$', views.list_files, name='list')
]
