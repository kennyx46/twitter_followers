"""twitter_followers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from twitterapp.views import twitter_login, \
    twitter_callback, twitter_followers, main, twitter_follower, search

urlpatterns = [
    url(r'^$', main),
    url(r'^login/?$', twitter_login),
    url(r'^twitter_callback', twitter_callback),
    url(r'^twitter_followers/(?P<follower_id>[\w-]+)$', twitter_follower),
    url(r'^twitter_followers', twitter_followers),
    url(r'^search', search),
]
