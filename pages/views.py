from django.shortcuts import render, redirect
import logging

logger = logging.getLogger('vacseen')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def IndexView(request):
    """Render index page (login with OAuth page)."""
    print(dir(request.GET))
    if str(request.user) == 'AnonymousUser':
        client_ip = get_client_ip(request)
        logger.error('Try to access from {}'.format(client_ip))
    return render(request, 'index.html')


def LoginHandler(request):
    """Login handler for checking if user already signup or not."""
    client_ip = request.META['REMOTE_ADDR']
    if request.user.gender and request.user.birthdate \
            and request.user.contact \
            and request.user.emergency_contact \
            and request.user.first_name and request.user.last_name:
        logger.debug('Successful login as {} from {}'.format(
            request.user.username, client_ip))
        return redirect('users:profile')
    else:
        logger.debug('Signup as {} from {}'.format(
            request.user.username, client_ip))
        return redirect('users:signup')


def handler404(request, exception):
    """Handler page for 404 response status code."""
    client_ip = get_client_ip(request)
    logger.error('404 response status code from {}'.format(client_ip))
    return render(request, '404.html', status=404)


def handler500(request, *args, **argv):
    """Handler page for 500 response status code."""
    client_ip = get_client_ip(request)
    logger.error('500 response status code from {}'.format(client_ip))
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
