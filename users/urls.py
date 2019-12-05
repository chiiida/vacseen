from django.urls import path
from .views import signup_view, vaccination_signup_view, user_view, request_user_view, parental_view

app_name = 'users'
urlpatterns = [
    path('profile/', user_view, name='profile'),
    path('signup/', signup_view, name='signup'),
    path('signup/vaccination/', vaccination_signup_view, name='vaccination'),
    path('request_user/', request_user_view, name='request_user'),
    path('parental/view/u/<int:user_id>/<str:uuid>/',
         parental_view, name='parental'),
]
