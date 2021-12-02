from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .forms import RegistrationForm, LoginForm


def sign_up(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            my_user = authenticate(email=email, password=raw_password)
            login(request, my_user)
            return HttpResponse(f"Good")
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'movies_auth/sign_up.html', context)


def sign_in(request):
    context = {}

    user = request.user
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return HttpResponse(f"Good, logged in")
    else:
        form = LoginForm()
    context['login_form'] = form
    return render(request, 'movies_auth/sign_in.html', context)


def log_out(request):
    logout(request)
    return HttpResponse(f"Logged out")


# def sign_in(request):
#     if request.POST:
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return HttpResponse(f"Good")
#         else:
#             return HttpResponse(f"Bad", status=403)
#     else:
#         return TemplateResponse(request, 'movies_auth/sign_in.html', {'auth_url': '/auth/'})
#
#
# def sign_up(request):
#     if request.POST:
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         dob = request.POST['dob']
#
#         # user = User(username=username,
#         #             email=email,
#         #             dob=datetime.datetime.strptime(dob, '%Y-%m-%d')
#         #             )
#         # user.set_password(password)
#         # user.save()
#
#         MyUser.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#             dob=datetime.datetime.strptime(dob, '%Y-%m-%d')
#         )
#         return HttpResponse(f"Good")
#     else:
#         return TemplateResponse(request, 'movies_auth/sign_up.html', {'sign_up_url': '/auth/sign_up/'})
#
#
