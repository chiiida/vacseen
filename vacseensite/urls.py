from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.generic import RedirectView

from vacseenApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vacseenApp.urls')),
    path('logout/', views.logout_user, name='logout'),
    path('o/', include('social_django.urls', namespace='social')),
    url('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
