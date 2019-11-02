from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    path('', include('vacseenApp.urls')),
    path('admin/', admin.site.urls),
    path('', include('vacseenApp.urls')),
    path('o/', include('social_django.urls', namespace='social')),
    url('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
