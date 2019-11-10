from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from .models import CustomUser
from .forms import CustomUserForm
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
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = CustomUserForm()
        return render(request, 'registration/signup.html', {'form': form})


def vaccination_signup(request):
    return render(request, 'registration/vaccination.html')


@login_required
def user_view(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {'user': user}
    return render(request, 'user.html', context)
