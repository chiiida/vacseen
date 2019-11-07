from django.urls import path
from .views import signup, vaccination_signup, user_view

app_name = 'users'
urlpatterns = [
    path('profile/', user_view, name='profile'),
    path('signup/', signup, name='signup'),
    path('signup/vaccination', vaccination_signup, name='vaccination'),
]