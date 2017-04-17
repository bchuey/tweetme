
from django.conf.urls import url
from django.views.generic.base import RedirectView

# from .views import tweet_detail_view, tweet_list_view
from tweets.api.views import (
        TweetListAPIView,
    )

urlpatterns = [

    url(r'^(?P<username>[\w.@+-]+)/tweet/$', TweetListAPIView.as_view(), name='list'),


]
