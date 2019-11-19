from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from .models import CustomUser
from vaccine.models import VaccineModel, Vaccine, Dose
from .forms import CustomUserForm, VaccineFormSet
from datetime import date, time, timedelta


def calculate_age(born):
    """Return user's age compute from birthdate"""
    today = date.today()
    month = abs(today.month - born.month)/10
    return (today.year - born.year)+month


def next_date(date: date, duration: int):
    """Return date that need to receive next dose (injuction) of vaccine"""
    return date + timedelta(days=duration)


def signup(request):
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
        return render(request, 'registration/signup.html', {'form': form})


def vaccine_suggest(user: CustomUser):
    """Filter vaccine that match with user then create vaccine and save to database"""
    vaccine_model = VaccineModel.objects.all()
    user_vaccine_list = [vaccine.vaccine_name for vaccine in user.vaccine_set.all()]
    vaccines = [vaccine for vaccine in vaccine_model if user.age >= vaccine.required_age 
                and vaccine.vaccine_name not in user_vaccine_list]
    for vaccine in vaccines:
        user_vaccine = Vaccine(vaccine_name=vaccine.vaccine_name,
                                required_age=vaccine.required_age,
                                required_gender=vaccine.required_gender,
                                user=user)
        user_vaccine.save()
        for dose in vaccine.dosemodel_set.all():
            user_dose = Dose(vaccine=user_vaccine,
                            dose_count=dose.dose_count,
                            dose_duration=dose.dose_duration)
            user_dose.save()


def vaccination_signup(request):
    """Get user's vaccination from from then create vaccine and save to database"""
    if request.method == 'GET':
        formset = VaccineFormSet(request.GET or None)
    elif request.method == 'POST':
        formset = VaccineFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                vaccine_name = form.cleaned_data.get('vaccine_name')
                dose_count = form.cleaned_data.get('dose_count')
                expired = form.cleaned_data.get('expired')
                vacc_model = VaccineModel.objects.get(
                    vaccine_name=vaccine_name)
                vaccine = Vaccine(vaccine_name=vacc_model.vaccine_name,
                                  required_age=vacc_model.required_age,
                                  required_gender=vacc_model.required_gender,
                                  user=request.user)
                vaccine.save()
                left_dose = list(vacc_model.dosemodel_set.all()[
                                 (dose_count-1):])
                for dose in left_dose:
                    user_dose = Dose(vaccine=vaccine,
                                     dose_count=dose.dose_count,
                                     dose_duration=dose.dose_duration,
                                     date_expired=next_date(expired, dose.dose_duration))
                    user_dose.save()
                vaccine_suggest(request.user)
            return HttpResponseRedirect(reverse('users:profile'))
    return render(request, 'registration/vaccination.html',
                  {'formset': formset, })

def upcoming_vaccine(user: CustomUser):
    """Return list of upcoming vaccines in 10 days"""
    today = date.today()
    upcoming_vaccine_list = []
    for vaccine in user.vaccine_set.all():
        for dose in vaccine.dose_set.all():
            if dose.date_expired:
                delta = dose.date_expired - today
                if 0 < delta.days <= 10:
                    upcoming_vaccine_list.append(dose)
    return upcoming_vaccine_list

@login_required(login_url='home')
def user_view(request):
    """Render user's page"""
    user = CustomUser.objects.get(id=request.user.id)
    vaccine_set = user.vaccine_set
    upcoming_vaccine_list = upcoming_vaccine(user)
    context = {'user': user, 'vaccine_set': vaccine_set, 'upcoming_vaccine': upcoming_vaccine_list}
    return render(request, 'user.html', context)
