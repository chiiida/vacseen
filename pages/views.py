from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'

def LoginHandler(request):
    print(dir(request.user))
    if request.user.gender and request.user.birthdate and request.user.contact and request.user.emergency_contact and request.user.first_name and request.user.last_name:
        return redirect('/users/')
        print("wtf")
        return redirect('users/'+str(request.user.id))
    else:
        user = request.user
        return render(request, 'regisration/signup.html', {'user': user}) 
        return redirect('users/signup/') 