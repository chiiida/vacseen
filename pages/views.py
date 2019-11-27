from django.shortcuts import render, redirect


def IndexView(request):
    return render(request, 'index.html')


def LoginHandler(request):
    if request.user.gender and \
        request.user.birthdate and \
        request.user.contact and \
        request.user.emergency_contact and \
        request.user.first_name and \
            request.user.last_name:
        return redirect('users:profile')
    else:
        return redirect('users:signup')


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request, *args, **argv):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
