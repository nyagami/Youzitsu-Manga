from django.contrib.auth.views import (
    LoginView as OldLoginView, LogoutView as OldLogOutView, PasswordChangeView as OldPasswordChangeView,
    PasswordResetView as OldPasswordResetView
)
from django.utils.decorators import decorator_from_middleware
from django.shortcuts import render
from registration.backends.simple.views import RegistrationView as OldRegistrationView

from django.contrib.auth.models import User
from .form import RegistrationForm
from .models import Profile
from utils.middleware import NotifactionMiddleWare


# Registration
class RegistrationView(OldRegistrationView):
    title = "Đăng kí"
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        if 'page_title' not in kwargs:
            kwargs['page_title'] = self.title

        return super(RegistrationView, self).get_context_data(**kwargs)

    def register(self, form):
        user = super(RegistrationView, self).register(form)
        profile, _ = Profile.objects.get_or_create(user=user)
        cleaned_data = form.cleaned_data
        profile.display_name = cleaned_data.get('display_name') or user.username
        profile.save()
        return user


class LoginView(OldLoginView):
    template_name = "log/login.html"
    extra_context = {
        "page_title": "Đăng nhập",
    }
    redirect_authenticated_user = True


class LogoutView(OldLogOutView):
    template_name = 'log/logout.html'
    extra_context = {
        "page_title": "Đăng xuất",
    }


class PasswordChangeView(OldPasswordChangeView):
    template_name = "password/password_change.html"

    def form_valid(self, form):
        self.request.session['password_pwned'] = False
        return super().form_valid(form)


class PasswordResetView(OldPasswordResetView):
    template_name = "password/password_reset.html"
    html_email_template_name = "password/password_reset_email.html"
    email_template_name = "password/password_reset_email.txt"

@decorator_from_middleware(NotifactionMiddleWare)
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except ValueError:
        return render(request, 'homepage/404_page.html', status=404)
    return render(
        request, 'profile.html',
        {
            "owner": user.username == request.user.username,
            "page_title": username,
            "profile": user.profile
        }
    )
