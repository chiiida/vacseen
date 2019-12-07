from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import date, timedelta

from users.forms import DateExpiredForm, VaccineFormSet
from users.models import CustomUser
from pages.views import get_client_ip, logger
from vaccine.models import VaccineModel, Vaccine, Dose


def next_date(date: date, duration: int):
    """Return date that need to receive next dose (injuction) of vaccine"""
    return date + timedelta(days=duration)


def create_vaccine(user_id: int, vacc_name: str, dose_count: int, date: date):
    """Create vaccine including requried dose by duplicate from model"""
    vacModel = VaccineModel.objects.get(
        vaccine_name=vacc_name)
    user = CustomUser.objects.get(id=user_id)
    vaccine = Vaccine(vaccine_name=vacModel.vaccine_name,
                      required_age=vacModel.required_age,
                      required_gender=vacModel.required_gender,
                      stimulate_phase=vacModel.stimulate_phase,
                      user=user)
    vaccine.save()
    if vaccine.stimulate_phase > 0:
        user_dose = Dose(vaccine=vaccine,
                         dose_count=dose_count,
                         date_taken=date,
                         received=True)
        user_dose.save()
        next_dose = Dose(vaccine=vaccine,
                         dose_count=vaccine.dose_set.count() + 1,
                         date_taken=next_date(
                             user_dose.date_taken, vaccine.stimulate_phase))
        next_dose.save()
    else:
        left_dose = list(vacModel.dosemodel_set.all()[(dose_count - 1):])
        for dose in left_dose:
            status = False
            if next_date(date, dose.dose_duration) == date and dose_count > 0:
                status = True
            user_dose = Dose(vaccine=vaccine,
                             dose_count=dose.dose_count,
                             dose_duration=dose.dose_duration,
                             received=status)
            if dose_count != 0:
                user_dose.date_taken = next_date(
                    date, dose.dose_duration)
            user_dose.save()


def filter_vaccine(user: CustomUser):
    """Filter vaccine by user's age and user's gender"""
    vaccine_model = VaccineModel.objects.all()
    user_vaccine_list = []
    if user.vaccine_set:
        user_vaccine_list = [
            vaccine.vaccine_name for vaccine in user.vaccine_set.all()]

    vaccines_list = []
    for vaccine in vaccine_model:
        if vaccine.vaccine_name not in user_vaccine_list:
            if vaccine.required_gender in ('None', user.gender):
                if user.age >= vaccine.required_age:
                    vaccines_list.append(vaccine)
    return vaccines_list


def vaccine_suggest(user: CustomUser):
    """
    Filter vaccine that match with user
    then create vaccine and save to database
    """
    vaccines = filter_vaccine(user)
    for vaccine in vaccines:
        user_vaccine = Vaccine(vaccine_name=vaccine.vaccine_name,
                               required_age=vaccine.required_age,
                               required_gender=vaccine.required_gender,
                               stimulate_phase=vaccine.stimulate_phase,
                               user=user)
        user_vaccine.save()
        if vaccine.stimulate_phase > 0:
            user_dose = Dose(vaccine=user_vaccine,
                             dose_count=1)
            user_dose.save()
        else:
            for dose in vaccine.dosemodel_set.all():
                user_dose = Dose(vaccine=user_vaccine,
                                 dose_count=dose.dose_count,
                                 dose_duration=dose.dose_duration)
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
            if vaccine.stimulate_phase > 0:
                user_dose = vaccine.dose_set.all()[0]
                user_dose.date_taken = date_taken
                user_dose.save()
            else:
                for dose in vacc_model.dosemodel_set.all():
                    user_dose = vaccine.dose_set.get(
                        dose_count=dose.dose_count)
                    user_dose.date_taken = next_date(
                        date_taken, dose.dose_duration)
                    user_dose.save()
        client_ip = get_client_ip(request)
        logger.debug(
            'Request update first date to receive {} from {}'.format(vaccine, client_ip))
    return redirect('users:profile')


@login_required(login_url='home')
def received_dose(request, dose_id: int):
    """Get input from the user that the user received that dose."""
    if request.method == 'POST':
        status = request.POST['receivedbtn']
        dose = Dose.objects.get(id=dose_id)
        if status == 'received':
            dose.received = True
            dose.save()
        if dose.vaccine.stimulate_phase > 0:
            new_dose = Dose(vaccine=dose.vaccine,
                            dose_count=dose.vaccine.dose_set.count() + 1,
                            date_taken=next_date(
                                dose.date_taken, dose.vaccine.stimulate_phase),
                            received=False)
            new_dose.save()
        client_ip = get_client_ip(request)
        logger.debug('Received dose request from {}'.format(client_ip))
    return redirect('users:profile')


@login_required(login_url='home')
def add_vaccine(request):
    """Get vaccine name, dose, and date taken input from the user and add vaccine"""
    if request.method == 'GET':
        formset = VaccineFormSet(request.GET or None)
    elif request.method == 'POST':
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
        client_ip = get_client_ip(request)
        logger.debug('Add vaccines request from {}'.format(client_ip))
        return redirect('users:profile')
    return render(request, 'add_vaccine.html',
                  {'formset': formset, })


@login_required(login_url='home')
def del_vaccine(request, vaccine_id: int):
    """Remove specify vaccine from user's input"""
    if request.method == 'POST':
        vaccine = Vaccine.objects.get(pk=request.POST['delvacc'])
        client_ip = get_client_ip(request)
        logger.debug('Remove {} request from {}'.format(vaccine, client_ip))
        vaccine.delete()
        return redirect('users:profile')
