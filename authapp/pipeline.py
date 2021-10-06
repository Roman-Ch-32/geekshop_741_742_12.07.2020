from collections import OrderedDict
from datetime import datetime

from urllib.parse import urlencode, urlparse, urlunparse

import requests
from django.shortcuts import render
from django.utils import timezone
from requests import request
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https', 'api.vk.com', '/method/users.get', None,
                            urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                            access_token=response['access_token'], v='5.131')),
                          None))
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.about_me = data['about']

    user.save()
    return render(request, 'index.html')
