from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse


def IndexView(request):
    """Render index page (login with OAuth page)."""
    return render(request, 'index.html')


def LoginHandler(request):
    """Login handler for checking if user already signup or not."""
    if request.user.gender and request.user.birthdate and request.user.contact and request.user.emergency_contact and request.user.first_name and request.user.last_name:
        return redirect(reverse('users:profile', args=(request.user.id,)))
    else:
        return redirect('users:signup')


def handler404(request, exception):
    """Handler page for 404 response status code."""
    return render(request, '404.html', status=404)


def handler500(request, *args, **argv):
    """Handler page for 500 response status code."""
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
