from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
# from django.core import serializers
from .models import AccessToken

import requests, base64, json


with open('cards/config.json') as f:
    config = json.load(f)

client_id = config['client_id']
client_secret = config['client_secret']
auth_str = base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')
refresh_token = config['refresh_token']


def index(request):
    if AccessToken.objects.filter(id=1).exists():
        at_obj = AccessToken.objects.get(id=1)
        bearer = {'Authorization': 'Bearer ' + at_obj.token}
        r = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=bearer)
        if r.status_code == 400 or r.status_code == 401:
            return auth(True)
        else:
            items = r.json()['albums']['items']
            return render(request, 'cards/index.html', {'card_list': items})
            # decided not to deserialize to a model
            # new_items = []
            # for item in items:
            #     new = {}
            #     new['pk'] = item.pop('id')
            #     new['model'] = 'cards.Album'
            #     new['fields'] = item
            #     new_items.append(new)
            # formatted = json.dumps(new_items)
            # for obj in serializers.deserialize('json', formatted, ignorenonexistent=True):
            #     print(obj)
    else:
        return auth(False)


def auth(exists):
    basic = {'Authorization': 'Basic ' + auth_str}
    form = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    r = requests.post('https://accounts.spotify.com/api/token', headers=basic, data=form)
    access_token = r.json()['access_token']
    if exists:
        at_obj = AccessToken.objects.get(id=1)
        at_obj.token = access_token
    else:
        at_obj = AccessToken(token=access_token)
    at_obj.save()
    return HttpResponseRedirect(reverse('cards:index'))
