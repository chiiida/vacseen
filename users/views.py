from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect

from .models import CustomUser
from .forms import  FormThatWork as MekInwRegisForm
import datetime
# Create your views here.


class SignUpView(CreateView):
    form_class = MekInwRegisForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def signup(request):
    if request.method == 'POST':
        form = MekInwRegisForm(request.POST)
        user = CustomUser.objects.get(pk=request.user.pk)
        now = datetime.datetime.now()
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            contact = form.cleaned_data.get('contact')
            emergency_contact = form.cleaned_data.get('emergency_contact')
            gender = form.cleaned_data.get('gender')
            birthdate = form.cleaned_data.get('birthdate')
            age = abs(now.year - birthdate.year)
            user.update_profile(username=user.email,
                                first_name=first_name,
                                last_name=last_name,
                                contact=contact,
                                emergency_contact=emergency_contact,
                                gender=gender,
                                birthdate=birthdate,
                                age=age)
            user.save()
            # might change to redirect to vaccine page later.
            return  HttpResponseRedirect(reverse('users:user', args=[request.user.pk]))
    else:
        form = MekInwRegisForm()
        return render(request, 'registration/signup.html', {'form': form})


def vaccination_signup(request):
    return render(request, 'registration/vaccination.html')


def user_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    context = {'user': user}
    return render(request, 'user.html', context)
