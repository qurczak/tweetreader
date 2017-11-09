from django.conf.urls import url

from apps.tweetreader import views as tweetreader_views

urlpatterns = [
    url(r'^tweets/', tweetreader_views.tweets, name='tweets'),
]
