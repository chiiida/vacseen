from django.urls import path
from .views import track_first_date, received_dose

app_name = 'vaccine'
urlpatterns = [
    path('<int:vaccine_id>/', track_first_date, name='trackfirstdate'),
    path('received/dose/<int:dose_id>/', received_dose, name='received'),
]
