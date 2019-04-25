from django.db import models


# this is how I store the access token on the server (so I don't have to query
# the server for a new one until this one expires)
class AccessToken(models.Model):
    token = models.CharField(max_length=1000)


# decided not to deserialize to a model
# class Album(models.Model):
#     album_type = models.CharField(max_length=100)
#     href = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     release_date = models.CharField(max_length=100)
#     release_date_precision = models.CharField(max_length=100)
#     total_tracks = models.IntegerField()
#     type = models.CharField(max_length=100)
#     uri = models.CharField(max_length=100)
