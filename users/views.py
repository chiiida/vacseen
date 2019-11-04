from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

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
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def vaccination_signup(request):
    return render(request, 'registration/vaccination.html')
