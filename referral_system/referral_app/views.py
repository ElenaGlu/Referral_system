from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from .forms import LoginForm, AuthenticationForm, InviteForm
from .referral_app_services.user import UserAccount


def user_login(request: HttpRequest) -> HttpResponse:
    """
    User logs in to the system by phone number.
    :param request:
    :return: template html page
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            obj_user = UserAccount()
            authentication_code, token = obj_user.create_update_user(phone_number)
            response = HttpResponsePermanentRedirect('authentication/')
            response.set_cookie("a_code", authentication_code)
            response.set_cookie("jwt", token)
            return response
        else:
            return HttpResponse("Invalid phone number")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def user_authentication(request: HttpRequest) -> HttpResponse:
    """
    User authentication by phone number code and cookies.
    :param request:
    :return: template html page
    """
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        access_token = request.COOKIES["jwt"]
        if form.is_valid():
            authentication_code = form.cleaned_data['authentication_code']
            obj_user = UserAccount()
            obj_user.check_authentication_code(authentication_code, access_token)
            return HttpResponsePermanentRedirect('/account_access/')
        else:
            return HttpResponse("Invalid code")
    else:
        form = AuthenticationForm()
        return render(request, 'authentication.html', {'form': form})


def account_access(request: HttpRequest) -> HttpResponse:
    """
    Provides access to your personal account.
    :param request:
    :return: template html page
    """
    access_token = request.COOKIES["jwt"]
    obj_user = UserAccount()
    data_user = obj_user.get_user_info(access_token)
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            invite_code = form.cleaned_data['invite_code']
            obj_user.activate_invite_code(access_token, invite_code)
            data_user = obj_user.get_user_info(access_token)
    return render(request, 'account.html', {'data_user': data_user})



