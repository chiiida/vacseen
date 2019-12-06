from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from datetime import date, timedelta

from vaccine.views import create_vaccine, vaccine_suggest
from vaccine.models import Outbreak
from .models import CustomUser
from .forms import CustomUserForm, VaccineFormSet, VaccinationForm
from uuid import UUID


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

    Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

    Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

    Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    if not isinstance(uuid_to_test, str):
        raise TypeError('not a string')
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def get_outbreak(request):
    """
    give outbreak alert to users
    """
    # get user
    # user = CustomUser.objects.get(id=request.user.id)
    # this_year = date.today().year
    # # get user vaccine
    # vaccine_set = user.sorted_vaccine()
    # # get vaccine nearing date
    # for vaccine in vaccine_set:
    #     # TODO get vaccine dose
    #     for dose in vaccine.dose_set.all():
    #         if dose.date_taken and not dose.received:
    #             # TODO compare dose.date_expired with today
    #             if (dose.date_taken.year+vaccine.stimulate_phase <= this_year):
    #                 return True
    # return False
    outbreaks_all = Outbreak.objects.all()
    outbreaks = [str(outbreak) for outbreak in outbreaks_all]
    return outbreaks


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
                      {'form': form, 'have_outbreak': False})


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


@login_required(login_url='home')
def request_user_view(request):
    """Render page for user to request to view other user page."""
    if request.method == 'GET':
        return render(request, 'request_user.html')
    elif request.method == 'POST':
        if is_valid_uuid(request.POST['uuid']):
            try:
                user = CustomUser.objects.get(
                    parental_key=request.POST['uuid'])
            except (KeyError, CustomUser.DoesNotExist):
                return render(request, 'request_user.html', {
                    'error_message': "Could not find user with this uuid.",
                })
            else:
                uuid = request.POST['uuid'][:4]
                return HttpResponseRedirect(reverse('users:parental',
                                                    kwargs={'user_id': user.id,
                                                            'uuid': uuid}))
        else:
            return render(request, 'request_user.html', {
                    'error_message': "Invalid uuid.",


@login_required(login_url='home')
def user_view(request):
    """Render user's page"""
    user = CustomUser.objects.get(id=request.user.id)
    vaccine_set = user.sorted_vaccine()
    have_outbreak = get_outbreak(request)
    upcoming_vaccine_list = upcoming_vaccine(user)
    form = VaccinationForm()
    context = {'user': user,
               'vaccine_set': vaccine_set,
               'have_outbreak': have_outbreak,
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
