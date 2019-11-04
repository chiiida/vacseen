from django.urls import path
from .views import SignUpView, signup

app_name = 'users'
urlpatterns = [
    path('signup/', signup, name='signup'),
]