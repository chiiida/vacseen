from django.urls import path
from .views import signup_view, vaccination_signup_view, user_view, request_user_view

app_name = 'users'
urlpatterns = [
    path('profile/<int:user_id>/', user_view, name='profile'),
    path('signup/', signup_view, name='signup'),
    path('signup/vaccination/', vaccination_signup_view, name='vaccination'),
    path('request_user/', request_user_view, name='request_user')
]
