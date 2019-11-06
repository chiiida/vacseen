from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=request.user)
        user = CustomUser.objects.get(pk=request.user.pk)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        contact = form.cleaned_data.get('contact')
        emergency_contact = form.cleaned_data.get('emergency_contact')
        gender = form.cleaned_data.get('gender')
        birthdate = form.cleaned_data.get('birthdate')
        user.update_profile(first_name=first_name,
                            last_name=last_name,
                            contact=contact,
                            emergency_contact=emergency_contact,
                            gender=gender,
                            birthdate=birthdate)
        return HttpResponseRedirect('home')
    else:
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


def vaccination_signup(request):
    return render(request, 'registration/vaccination.html')


def user_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    context = {'user': user}
    return render(request, 'test.html', context)