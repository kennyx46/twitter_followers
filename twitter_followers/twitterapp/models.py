from django.db import models

class Follower(models.Model):

    name = models.CharField(max_length=200)
    screen_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    str_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)