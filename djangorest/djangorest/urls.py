from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls), 
    url(r'^', include_docs_urls(title='API reference')),
    url(r'^api/v1/', include('api.urls')),
]
