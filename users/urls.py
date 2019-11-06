from django.urls import path
from .views import SignUpView, signup, vaccination_signup, user_view

app_name = 'users'
urlpatterns = [
    path('<int:user_id>/', user_view, name='user'),
    path('signup/', signup, name='signup'),
    path('signup/vaccination', vaccination_signup, name='vaccination'),
]