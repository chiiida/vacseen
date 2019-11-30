from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from users.views import next_date
from users.forms import DateExpiredForm
from vaccine.models import *


@login_required(login_url='home')
def track_first_date(request, vaccine_id: int):
    """
    Get input from the user which is the first date that user will receive 
    the first dose of that vaccine and track other dose if have.
    """
    vaccine = Vaccine.objects.get(id=vaccine_id)
    vacc_model = VaccineModel.objects.get(vaccine_name=vaccine.vaccine_name)
    if request.method == 'POST':
        form = DateExpiredForm(request.POST)
        if form.is_valid():
            expired = form.cleaned_data.get('expired')
            for dose in vacc_model.dosemodel_set.all():
                user_dose = vaccine.dose_set.get(dose_count=dose.dose_count)
                user_dose.date_taken = next_date(expired, dose.dose_duration)
                user_dose.save()
    return redirect(reverse('users:profile', args=(request.user.id,)))


@login_required(login_url='home')
def received_dose(request, dose_id: int):
    """Get input from the user that the user received that dose."""
    if request.method == 'POST':
        status = True
        dose = Dose.objects.get(id=dose_id)
        dose.received = status
        dose.save()
    return redirect(reverse('users:profile', args=(request.user.id,)))
