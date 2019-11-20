from pages.views import handler404
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls'), name='pages'),
    path('users/', include('users.urls'), name='users'),
    path('accounts/', include('allauth.urls'), name='accounts'),
    path('admin/', admin.site.urls, name='admin'),
]

handler404 = 'pages.views.handler404'
