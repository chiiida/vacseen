from django.urls import path
from .views import track_first_date, received_dose, add_vaccine, del_vaccine

app_name = 'vaccine'
urlpatterns = [
    path('track/<int:vaccine_id>/', track_first_date, name='trackfirstdate'),
    path('received/dose/<int:dose_id>/', received_dose, name='received'),
    path('add/', add_vaccine, name='addvaccine'),
    path('delete/<int:vaccine_id>/', del_vaccine, name='delvaccine'),
]
