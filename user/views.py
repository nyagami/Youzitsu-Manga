from django.contrib.auth.views import (
    LoginView as OldLoginView, LogoutView as OldLogOutView, PasswordChangeView as OldPasswordChangeView,
    PasswordResetView as OldPasswordResetView
)
from django.utils.decorators import decorator_from_middleware
from django.http import HttpResponseForbidden
from django.shortcuts import render
from registration.backends.simple.views import RegistrationView as OldRegistrationView

from django.contrib.auth.models import User
from .form import RegistrationForm
from .models import Profile
from utils.models import Comment
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
    if request.method == 'POST':
        email = request.POST.get('email')
        display_name = request.POST.get('display_name')
        description = request.POST.get('description')
        try:
            prf = Profile.objects.get(user=request.user)
        except ValueError:
            return HttpResponseForbidden()
        if email:
            user.email = email
            user.save()
        if display_name or description:
            if display_name:
                prf.display_name = display_name
            if description:
                prf.description = description
            prf.save()
    return render(
        request, 'profile.html',
        {
            "owner": user.username,
            "page_title": username,
            "profile": user.profile,
            "comments": len(Comment.objects._mptt_filter(author=user.profile))
        }
    )
