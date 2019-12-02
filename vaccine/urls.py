from django.urls import path
from .views import *

app_name = 'vaccine'
urlpatterns = [
    path('<int:vaccine_id>/', track_first_date, name='trackfirstdate'),
    path('received/dose/<int:dose_id>/', received_dose, name='received'),
    path('add/', add_vaccine, name='addvaccine'),
    path('delete/<int:vaccine_id>/', del_vaccine, name='delvaccine'),
]
