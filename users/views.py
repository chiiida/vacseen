from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import CustomUser
from .forms import CustomUserCreationForm
# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data('first_name')
            last_name = form.cleaned_data('last_name')
            contact = form.cleaned_data('contact')
            emergency_contact = form.cleaned_data('emergency_contact')
            gender = form.cleaned_data('gender')
            birthdate = form.cleaned_data('birthdate')
            user = CustomUser(username='hana', email='hana@gmail.com', first_name=first_name, last_name=last_name, contact=contact, emergency_contact=emergency_contact, gender=gender, birthdate=birthdate)
            print(user.first_name)
            user.save()
            login(request, user)
            return HttpResponseRedirect('home')
    else:
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

def vaccination_signup(request):
    return render(request, 'registration/vaccination.html')
