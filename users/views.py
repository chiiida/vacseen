from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from django import forms
from .models import CustomUser
from vaccine.models import VaccineModel, Vaccine, DoseModel, Dose
from .forms import CustomUserForm, VaccinationForm, VaccineFormSet
from datetime import date

def calculate_age(born):
    today = date.today()
    month = abs(today.month - born.month)/10
    return (today.year - born.year)+month

def signup(request):
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

def get_doseset(vaccine_name):
    print(vaccine_name)
    vaccine = VaccineModel.objects.get(vaccine_name=vaccine_name)
    dose_choice = []
    doses = vaccine.dose_set.all()
    for dose in doses:
        d = (dose, str(dose))
        dose_choice.append(d)
    return dose_choice

def vaccination_signup(request):
    if request.method == 'GET':
        formset = VaccineFormSet(request.GET or None)
    elif request.method == 'POST':
        formset = VaccineFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                vaccine_name = form.cleaned_data.get('vaccine_name')
                dose_count = form.cleaned_data.get('dose_count')
                expired = form.cleaned_data.get('expired')
                vacc_model = VaccineModel.objects.get(vaccine_name=vaccine_name)
                vaccine = Vaccine(vaccine_name=vacc_model.vaccine_name, 
                                required_age=vacc_model.required_age, 
                                required_gender=vacc_model.required_gender,
                                user=request.user)
                vaccine.save()
                left_dose = list(vacc_model.dosemodel_set.all()[(dose_count-1):])
                for dose in left_dose:
                    user_dose = Dose(vaccine=vaccine,
                                    dose_count=dose.dose_count,
                                    dose_duration=dose.dose_duration,
                                    date_expired=expired)
                    user_dose.save()
            return HttpResponseRedirect(reverse('users:profile'))
    return render(request, 'registration/vaccination.html', {'formset': formset,})

@login_required(login_url='home')
def user_view(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {'user': user}
    return render(request, 'user.html', context)
