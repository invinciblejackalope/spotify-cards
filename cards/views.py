from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
# from django.core import serializers
from .models import AccessToken

import requests, base64, json


# load auth info from config.json so that I don't have to put it on GitHub
with open('cards/config.json') as f:
    config = json.load(f)

client_id = config['client_id']
client_secret = config['client_secret']
# this is how the Spotify API wants the auth to be passed
auth_str = base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')
# because access tokens expire after a short time, the refresh token is used
# (along with the client id and secret) to get a new one
# it can be stored in config.json because as long as the client secret
# doesn't change, we don't need to ask for a new refresh token
refresh_token = config['refresh_token']


def index(request):
    # if there is an access token on the server
    if AccessToken.objects.filter(id=1).exists():
        # get the first one because there should only be one
        at_obj = AccessToken.objects.get(id=1)
        # Spotify wants this passed as a header
        bearer = {'Authorization': 'Bearer ' + at_obj.token}
        r = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=bearer)
        # if access token is empty or invalid
        if r.status_code == 400 or r.status_code == 401:
            # get a new access token (True means the access token object already
            # exists)
            return auth(True)
        else:
            # retrieve the list of new releases from the JSON
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
        # get a new access token (False means the access token object doesn't
        # exist yet)
        return auth(False)


def auth(exists):
    # Spotify wants this stuff passed to it as a header and form data,
    # respectively
    basic = {'Authorization': 'Basic ' + auth_str}
    form = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    r = requests.post('https://accounts.spotify.com/api/token', headers=basic, data=form)
    # retrieve access token from the JSON (this breaks if the API returns an
    # error message but oh well)
    access_token = r.json()['access_token']
    if exists:
        # modify existing AccessToken object
        at_obj = AccessToken.objects.get(id=1)
        at_obj.token = access_token
    else:
        # create new AccessToken object
        at_obj = AccessToken(token=access_token)
    at_obj.save()
    # redirect back to index
    return HttpResponseRedirect(reverse('cards:index'))
