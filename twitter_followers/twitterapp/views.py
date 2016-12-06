from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from django.core.urlresolvers import reverse

from .models import Follower

import tweepy


def get_api(request):
  """
  set up and return a twitter api object
  """
  oauth = tweepy.OAuthHandler(
    settings.CONSUMER_KEY,
    settings.CONSUMER_SECRET,
  )
  access_key = request.session['access_key_tw']
  access_secret = request.session['access_secret_tw']
  oauth.set_access_token(access_key, access_secret)
  api = tweepy.API(oauth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
  return api


def main(request):
  """
  main view of app, either login page or info page
  """
  # if we haven't authorised yet, direct to login page
  if check_key(request):
    return redirect('/twitter_followers')
  else:
    return render_to_response('twitterapp/login.html')


def twitter_login (request):
  oauth = tweepy.OAuthHandler(
    settings.CONSUMER_KEY,
    settings.CONSUMER_SECRET,
    'http://localhost:8000/twitter_callback')
  # direct the user to the authentication url
  # if user is logged-in and authorized then transparently goto the callback URL
  auth_url = oauth.get_authorization_url(True)
  response = redirect(auth_url)

  # store the request token
  request.session['unauthed_token_tw'] = (
    oauth.request_token['oauth_token'],
    oauth.request_token['oauth_token_secret']
  )
  return response


def twitter_callback (request):
  verifier = request.GET.get('oauth_verifier')
  oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
  token = request.session.get('unauthed_token_tw', None)
  # remove the request token now we don't need it
  request.session.delete('unauthed_token_tw')
  oauth.request_token = {
    'oauth_token': token[0] ,
    'oauth_token_secret': token[1]
  }

  # get the access token and store
  try:
    oauth.get_access_token(verifier)
  except tweepy.TweepError:
    print('Error, failed to get access token')

  request.session['access_key_tw'] = oauth.access_token
  request.session['access_secret_tw'] = oauth.access_token_secret

  api = get_api(request)
  current_user = api.me()

  for user in tweepy.Cursor(api.followers, screen_name=current_user.screen_name).items():
    Follower.objects.get_or_create(
      name=user.name,
      screen_name=user.screen_name,
      location=user.location,
      str_id=user.id_str,
      user_id=current_user.id
    )

  return redirect('/twitter_followers')


def twitter_followers (request):
  if check_key(request):
    api = get_api(request)

    current_user = api.me()
    followers = Follower.objects.filter(user_id=current_user.id)

    return render_to_response("twitterapp/followers.html", {
      'followers': followers,
      'user': current_user
    })
  else:
    return redirect('/')


def twitter_follower (request, follower_id):
  if check_key(request):
    follower = get_object_or_404(Follower, str_id=follower_id)
    return render_to_response("twitterapp/follower.html", {'follower':follower})
  else:
    return redirect("/")


def search (request):
  screen_name = request.GET['screen_name']

  followers = Follower.objects.filter(screen_name__contains=screen_name)
  return render_to_response("twitterapp/search.html", {'followers':followers})


def check_key(request):
  try:
    access_key = request.session.get('access_key_tw', None)
    if not access_key:
      return False
  except KeyError:
    return False
  return True
