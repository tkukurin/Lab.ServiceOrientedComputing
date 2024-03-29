from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = (
	url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
  url(r'^tweets/$', TweetCreateView.as_view(), name='create'),
	url(r'^tweets/(?P<pk>[0-9]+)/$', TweetDetailsView.as_view(), name='details'),
	url(r'^users/(?P<user_id>[A-Za-z0-9]+)/tweets/$', UserTweetsView.as_view()),
	url(r'^users/$', UserCreateView.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', UserDetailsView.as_view()),
	url(r'^token/$', obtain_auth_token),
)

urlpatterns = format_suffix_patterns(urlpatterns)