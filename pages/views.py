from django.shortcuts import render, redirect
from django.urls import reverse
import datetime
import logging

# logger = logging.getLogger('userlog')


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


def IndexView(request):
    """Render index page (login with OAuth page)."""
    return render(request, 'index.html')


def LoginHandler(request):
    """Login handler for checking if user already signup or not."""
    if request.user.gender and request.user.birthdate \
            and request.user.contact \
            and request.user.emergency_contact \
            and request.user.first_name and request.user.last_name:
        # logger.info("Successful login from " + get_client_ip(request))
        return redirect('users:profile')
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
