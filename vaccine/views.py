from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date, timedelta

from users.forms import *
from users.models import CustomUser
from vaccine.models import *


def next_date(date: date, duration: int):
    """Return date that need to receive next dose (injuction) of vaccine"""
    return date + timedelta(days=duration)


def create_vaccine(user_id: int, vaccine_name: str, dose_count: int, date_taken: date):
    """Create vaccine including requried dose by duplicate from model"""
    vacModel = VaccineModel.objects.get(
        vaccine_name=vaccine_name)
    user = CustomUser.objects.get(id=user_id)
    vaccine = Vaccine(vaccine_name=vacModel.vaccine_name,
                      required_age=vacModel.required_age,
                      required_gender=vacModel.required_gender,
                      user=user)
    vaccine.save()
    left_dose = list(vacModel.dosemodel_set.all())
    if dose_count > 0:
        left_dose = list(vacModel.dosemodel_set.all()[(dose_count-1):])
    for dose in left_dose:
        status = False
        if next_date(date_taken, dose.dose_duration) == date_taken and dose_count > 0:
            status = True
        user_dose = Dose(vaccine=vaccine,
                         dose_count=dose.dose_count,
                         dose_duration=dose.dose_duration,
                         received=status)
        if dose_count != 0:
            user_dose.date_taken = next_date(date_taken, dose.dose_duration)
        user_dose.save()


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
            date_taken = form.cleaned_data.get('date_taken')
            for dose in vacc_model.dosemodel_set.all():
                user_dose = vaccine.dose_set.get(dose_count=dose.dose_count)
                user_dose.date_taken = next_date(date_taken, dose.dose_duration)
                user_dose.save()
    return redirect(reverse('users:profile', args=(request.user.id,)))


@login_required(login_url='home')
def received_dose(request, dose_id: int):
    """Get input from the user that the user received that dose."""
    if request.method == 'POST':
        status = request.POST['received-btn']
        dose = Dose.objects.get(id=dose_id)
        if status == '✔':
            dose.received = True
            dose.save()
    return redirect(reverse('users:profile', args=(request.user.id,)))


@login_required(login_url='home')
def add_vaccine(request):
    """Get vaccine name, dose, and date taken input from the user and add vaccine"""
    if request.method == 'GET':
        formset = VaccineFormSet(request.GET or None)
    elif request.method == 'POST':
        print(request.POST)
        formset = VaccineFormSet(request.POST)
        user_vac_name = [
            v.vaccine_name for v in request.user.vaccine_set.all()]
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('vaccine_name'):
                    vaccine_name = form.cleaned_data.get('vaccine_name')
                    dose_count = form.cleaned_data.get('dose_count')
                    date_taken = form.cleaned_data.get('date_taken')
                    if vaccine_name not in user_vac_name:
                        create_vaccine(request.user.id,
                                       vaccine_name,
                                       dose_count,
                                       date_taken)
        return HttpResponseRedirect(reverse('users:profile',
                                            args=(request.user.id,)))
    return render(request, 'add_vaccine.html',
                  {'formset': formset,})


def del_vaccine(request, vaccine_id: int):
    """Remove specify vaccine from user's input"""
    vaccine = Vaccine.objects.get(id=vaccine_id)
    vaccine.delete()
    return HttpResponseRedirect(reverse('users:profile',
                                        args=(request.user.id,)))
