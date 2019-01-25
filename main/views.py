import json
import logging

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from openhumans.models import OpenHumansMember

logger = logging.getLogger(__name__)


def index(request):
    """
    Starting page for app.
    """
    auth_url = OpenHumansMember.get_auth_url()
    context = {'auth_url': auth_url,
               'oh_proj_page': settings.OH_PROJ_PAGE}
    if request.user.is_authenticated:
        return redirect('overview')
    return render(request, 'main/index.html', context=context)


def overview(request):
    if request.user.is_authenticated:
        oh_member = request.user.openhumansmember
        context = {'oh_id': oh_member.oh_id,
                   'oh_member': oh_member,
                   'oh_proj_page': settings.OH_PROJ_PAGE}
        return render(request, 'main/overview.html', context=context)
    return redirect('index')


def logout_user(request):
    """
    Logout user
    """
    if request.method == 'POST':
        logout(request)
    return redirect('index')


def upload(request):
    if request.method == 'POST':
        desc = request.POST['file_desc']
        tags = request.POST['file_tags'].split(',')
        uploaded_file = request.FILES.get('data_file')
        if uploaded_file is not None:
            metadata = {'tags': tags,
                        'description': desc}
            request.user.openhumansmember.upload(
                stream=uploaded_file,
                filename=uploaded_file.name,
                metadata=metadata)
        return redirect('index')
    else:
        if request.user.is_authenticated:
            return render(request, 'main/upload.html')
    return redirect('index')


def list_files(request):
    if request.user.is_authenticated:
        context = {'files': request.user.openhumansmember.list_files()}
        return render(request, 'main/list.html',
                      context=context)
    return redirect('index')
