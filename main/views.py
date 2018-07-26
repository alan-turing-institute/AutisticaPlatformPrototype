import json
import logging
try:
    from urllib2 import HTTPError
except ImportError:
    from urllib.error import HTTPError

from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.safestring import mark_safe

import ohapi
import requests

from .helpers import oh_code_to_member, oh_client_info

logger = logging.getLogger(__name__)

OH_BASE_URL = settings.OPENHUMANS_OH_BASE_URL
OH_API_BASE = OH_BASE_URL + '/api/direct-sharing'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'

OH_OAUTH2_REDIRECT_URI = '{}/complete'.format(settings.OPENHUMANS_APP_BASE_URL)


def raise_http_error(url, response, message):
    raise HTTPError(url, response.status_code, message, hdrs=None, fp=None)


def upload_file_to_oh(oh_member, filehandle, metadata):
    """
    This demonstrates using the Open Humans "large file" upload process.
    The small file upload process is simpler, but it can time out. This
    alternate approach is required for large files, and still appropriate
    for small files.
    This process is "direct to S3" using three steps: 1. get S3 target URL from
    Open Humans, 2. Perform the upload, 3. Notify Open Humans when complete.
    """
    # Get the S3 target from Open Humans.
    upload_url = '{}?access_token={}'.format(
        OH_DIRECT_UPLOAD, oh_member.get_access_token(**oh_client_info()))
    req1 = requests.post(upload_url,
                         data={'project_member_id': oh_member.oh_id,
                               'filename': filehandle.name,
                               'metadata': json.dumps(metadata)})
    if req1.status_code != 201:
        raise raise_http_error(upload_url, req1,
                               'Bad response when starting file upload.')

    # Upload to S3 target.
    req2 = requests.put(url=req1.json()['url'], data=filehandle)
    if req2.status_code != 200:
        raise raise_http_error(req1.json()['url'], req2,
                               'Bad response when uploading to target.')

    # Report completed upload to Open Humans.
    complete_url = ('{}?access_token={}'.format(
        OH_DIRECT_UPLOAD_COMPLETE, oh_member.get_access_token(
            **oh_client_info())))
    req3 = requests.post(complete_url,
                         data={'project_member_id': oh_member.oh_id,
                               'file_id': req1.json()['id']})
    if req3.status_code != 200:
        raise raise_http_error(complete_url, req2,
                               'Bad response when completing upload.')


def get_auth_url():
    if settings.OPENHUMANS_CLIENT_ID and settings.OPENHUMANS_REDIRECT_URI:
        auth_url = ohapi.api.oauth2_auth_url(
            client_id=settings.OPENHUMANS_CLIENT_ID,
            redirect_uri=settings.OPENHUMANS_REDIRECT_URI)
    else:
        auth_url = ''
    return auth_url


def index(request):
    """
    Starting page for app.
    """
    auth_url = get_auth_url()
    if not auth_url:
        messages.info(request,
                      mark_safe(
                          '<b>You need to set up your ".env"'
                          ' file!</b>'))
    context = {'auth_url': auth_url}
    if request.user.is_authenticated:
        return redirect('overview')
    return render(request, 'main/index.html', context=context)


def overview(request):
    if request.user.is_authenticated:
        oh_member = request.user.openhumansmember
        context = {'oh_id': oh_member.oh_id,
                   'oh_member': oh_member}
        return render(request, 'main/overview.html', context=context)
    return redirect('index')


def login_member(request):
    code = request.GET.get('code', '')
    try:
        oh_member = oh_code_to_member(code=code)
    except Exception:
        oh_member = None
    if oh_member:
        # Log in the user.
        user = oh_member.user
        login(request, user,
              backend='django.contrib.auth.backends.ModelBackend')


def complete(request):
    """
    Receive user from Open Humans. Store data, start data upload task.
    """
    logger.debug("Received user returning from Open Humans.")

    login_member(request)
    if not request.user.is_authenticated:
        logger.debug('Invalid code exchange. User returned to start page.')
        return redirect('/')
    else:
        return redirect('overview')


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
            upload_file_to_oh(
                request.user.openhumansmember,
                uploaded_file,
                metadata)
        return redirect('index')
    else:
        if request.user.is_authenticated:
            return render(request, 'main/upload.html')
    return redirect('index')


def list_files(request):
    if request.user.is_authenticated:
        oh_member = request.user.openhumansmember
        data = ohapi.api.exchange_oauth2_member(
                    oh_member.get_access_token(**oh_client_info()))
        context = {'files': data['data']}
        return render(request, 'main/list.html',
                      context=context)
    return redirect('index')
