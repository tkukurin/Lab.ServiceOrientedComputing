from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
import views as web_views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls), 
    url(r'^api/', include_docs_urls(title='API reference')),
    url(r'^api/v1/', include('api.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^$', web_views.home, name='home'),
]
