from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken

from .forms import RegistrationForm, LoginForm
from .serializers import RegistrationSerializer


def sign_up(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            my_user = authenticate(username=username, password=raw_password)
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
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

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


class ApiSignIn(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "status":
                {
                    "message": "Logged in",
                    "code": f"{status.HTTP_200_OK} OK",
                }
        })


class ApiLogout(APIView):
    """"
    View for logging out
    """
    permission_classes = (permissions.IsAuthenticated,)  # Allows access only to authenticated users
    # cause we have TokenAuth it checks if header has a token

    def post(self, request, format=None):
        request.user.auth_token.delete()  # deletes the token
        return Response(status=status.HTTP_200_OK)  # returns empty response, 'status' basically says that it's ok
        # request was successfully received


class ApiSignUp(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "status": {
                        "message": "User created",
                        "code": f"{status.HTTP_200_OK} OK",
                    },
                }
            )
        return Response(
            {
                "error": serializer.errors,
                "status": f"{status.HTTP_203_NON_AUTHORITATIVE_INFORMATION} NON AUTHORITATIVE INFORMATION",
            }
        )
