from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, AuthenticationForm, InviteForm
from .referral_app_services.user import UserAccount


def user_login(request: HttpRequest) -> HttpResponse:
    """
    User logs in to the system by phone number.
    :param request: dict object containing key - phone_number
    :return: template html page
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            try:
                obj_user = UserAccount()
                authentication_code, token = obj_user.create_update_user(phone_number)
                response = redirect('user_authentication')
                response.set_cookie("a_code", authentication_code)
                response.set_cookie("jwt", token, max_age=3600, httponly=True, secure=True)
                return response
            except Exception as e:
                messages.error(request, f"Ошибка при входе: {str(e)}")
                return redirect('user_login')
        else:
            messages.error(request, "Пожалуйста, введите корректный номер телефона.")
            return redirect('user_login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def user_authentication(request: HttpRequest) -> HttpResponse:
    """
    User authentication by phone number code and cookies.
    :param request: dict object containing key - authentication_code
    :return: template html page
    """
    access_token = UserAccount.login_required(request)
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            authentication_code = form.cleaned_data['authentication_code']
            try:
                obj_user = UserAccount()
                obj_user.check_authentication_code(authentication_code, access_token)
                return redirect('account_access')
            except Exception as e:
                messages.error(request, f"Ошибка: {str(e)}")
                return redirect('user_authentication')
        else:
            messages.error(request, "Некорректный код.")
            return redirect('user_authentication')
    else:
        form = AuthenticationForm()
        return render(request, 'authentication.html', {'form': form})


def account_access(request: HttpRequest) -> HttpResponse:
    """
    Provides access to your personal account.
    :param request: dict object containing key - invite_code
    :return: template html page
    """
    access_token = UserAccount.login_required(request)
    obj_user = UserAccount()
    data_user = obj_user.get_user_info(access_token)

    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            invite_code = form.cleaned_data['invite_code']
            try:
                obj_user.activate_invite_code(access_token, invite_code)
                data_user = obj_user.get_user_info(access_token)
            except Exception as e:
                messages.error(request, f"Ошибка активации: {str(e)}")
                return redirect('account_access')
        else:
            messages.error(request, "Некорректный код приглашения.")
            return redirect('account_access')
    return render(request, 'account.html', {'data_user': data_user})
