from django.urls import path
from .views import SignUpView, signup, vaccination_signup

app_name = 'users'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signup/vaccination', vaccination_signup, name='vaccination'),
]