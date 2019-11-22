from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView


def IndexView(request):
    return render(request, 'index.html')


def LoginHandler(request):
    if request.user.gender and request.user.birthdate and request.user.contact and request.user.emergency_contact and request.user.first_name and request.user.last_name:
        return redirect('users:profile')
    else:
        return redirect('users:signup')


def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response
