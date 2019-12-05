from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from datetime import date, timedelta
import logging

from vaccine.models import VaccineModel, Vaccine, Dose
from vaccine.views import create_vaccine, vaccine_suggest
from .models import CustomUser
from .forms import CustomUserForm, VaccineFormSet, VaccinationForm


# logger = logging.getLogger('userlog')

def get_usernoti(request):
    """
    compute if user have a vaccine that need to be retaken within 1 year.
    """
    # get user
    user = CustomUser.objects.get(id=request.user.id)
    this_year = date.today().year
    # get user vaccine
    vaccine_set = user.sorted_vaccine()
    # get vaccine nearing date
    for vaccine in vaccine_set:
        # TODO get vaccine dose
        for dose in vaccine.dose_set.all():
            if dose.date_taken and not dose.received:
                # TODO compare dose.date_expired with today
                if (dose.date_taken.year+vaccine.stimulate_phase <= this_year):
                    return True
    return False


def calculate_age(born: date):
    """Return user's age computed from birthdate"""
    today = date.today()
    month = abs(today.month - born.month)/10
    return (today.year - born.year)+month


def next_date(date: date, duration: int):
    """Return date that need to receive next dose (injuction) of vaccine"""
    return date + timedelta(days=duration)


def signup_view(request):
    """Get user's infomation from from then create user and save to database"""
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        user = CustomUser.objects.get(pk=request.user.pk)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            contact = form.cleaned_data.get('contact')
            emergency_contact = form.cleaned_data.get('emergency_contact')
            gender = form.cleaned_data.get('gender')
            birthdate = form.cleaned_data.get('birthdate')
            age = calculate_age(birthdate)
            user.update_profile(username=user.email,
                                first_name=first_name,
                                last_name=last_name,
                                contact=contact,
                                emergency_contact=emergency_contact,
                                gender=gender,
                                birthdate=birthdate,
                                age=age)
            user.save()
            return HttpResponseRedirect(reverse('users:vaccination'))
    else:
        form = CustomUserForm()
        return render(request, 'registration/signup.html',
                      {'form': form, 'have_noti': False})


def vaccination_signup_view(request):
    """
    Get user's vaccination from from
    then create vaccine and save to database.
    """
    if request.method == 'GET':
        formset = VaccineFormSet(request.GET or None)
    elif request.method == 'POST':
        formset = VaccineFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('vaccine_name'):
                    vaccine_name = form.cleaned_data.get('vaccine_name')
                    dose_count = form.cleaned_data.get('dose_count')
                    date_taken = form.cleaned_data.get('date_taken')
                    create_vaccine(request.user.id,
                                   vaccine_name,
                                   dose_count,
                                   date_taken)
            vaccine_suggest(request.user)
        return redirect('users:profile')
    return render(request, 'registration/vaccination.html',
                  {'formset': formset, })


def upcoming_vaccine(user: CustomUser):
    """Return list of upcoming vaccines in 10 days"""
    today = date.today()
    upcoming_vaccine_list = []
    for vaccine in user.vaccine_set.all():
        for dose in vaccine.dose_set.all():
            if dose.date_taken:
                delta = dose.date_taken - today
                if not dose.received and 0 <= delta.days <= 7:
                    upcoming_vaccine_list.append(dose)
    return sorted(upcoming_vaccine_list, key=lambda d: d.date_taken)


def request_user_view(request):
    if request.method == 'GET':
        return render(request, 'request_user.html')
    elif request.method == 'POST':
        try:
            user = CustomUser.objects.get(parental_key=request.POST['uuid'])
        except (KeyError, CustomUser.DoesNotExist):
            return render(request, 'request_user.html', {
                'error_message': "Could not find uuid.",
            })
        else:
            uuid = request.POST['uuid'][:4]
            return HttpResponseRedirect(reverse('users:parental',
                                            kwargs={'user_id': user.id,
                                                    'uuid': uuid}))


@login_required(login_url='home')
def user_view(request):
    """Render user's page"""
    print(request.user.id)
    # print(user_id)
    # if user_id == request.user.id:
    user = CustomUser.objects.get(id=request.user.id)
    vaccine_set = user.sorted_vaccine()
    have_noti = get_usernoti(request)
    upcoming_vaccine_list = upcoming_vaccine(user)
    form = VaccinationForm()
    context = {'user': user,
                'vaccine_set': vaccine_set,
                'have_noti': have_noti,
                'upcoming_vaccine': upcoming_vaccine_list,
                'form': form}
    return render(request, 'user.html', context)


@login_required(login_url='home')
def parental_view(request, user_id: int, uuid: str):
    user = CustomUser.objects.get(id=user_id)
    if uuid == user.parental_key[:4]:
        user = CustomUser.objects.get(id=user_id)
        vaccine_set = user.sorted_vaccine()
        upcoming_vaccine_list = upcoming_vaccine(user)
        context = {'user': user,
                   'vaccine_set': vaccine_set,
                   'upcoming_vaccine': upcoming_vaccine_list}
        return render(request, 'parental.html', context)
