"""oh_app_demo URL Configuration

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
To override specific arguments of views provided by openhumans
    1. Import the specific view : eg. from openhumans.views import delete_file
    2. Before importing openhumans urls, override the specific url import: eg:
    urlpatterns += [
        url(r'^delete/(?P<file_id>\w+)/?$', delete_file.as_view(
        scuccess_url='success', not_authorized_url='login'), name='openhumans')
        ]

"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    url('', include(('openhumans.urls', 'openhumans')))
]
