from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('vacseenApp.urls')),
    path('admin/', admin.site.urls),
    path('o/', include('social_django.urls', namespace='social')),
]
