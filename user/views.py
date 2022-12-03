from django.contrib.auth.views import (
    LoginView as OldLoginView, LogoutView as OldLogOutView, PasswordChangeView as OldPasswordChangeView,
    PasswordResetView as OldPasswordResetView
)
from registration.backends.simple.views import RegistrationView as OldRegistrationView

from .form import RegistrationForm


#Registration
class RegistrationView(OldRegistrationView):
    title = "Đăng kí"
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        if 'page_title' not in kwargs:
            kwargs['page_title'] = self.title

        return super(RegistrationView, self).get_context_data(**kwargs)

    def register(self, form):
        user = super(RegistrationView, self).register(form)
        return user

# Login
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

# Password

class PasswordChangeView(OldPasswordChangeView):
    template_name = "password/password_change.html"
    def form_valid(self, form):
        self.request.session['password_pwned'] = False
        return super().form_valid(form)

class PasswordResetView(OldPasswordResetView):
    template_name = "password/password_reset.html"
    html_email_template_name = "password/password_reset_email.html"
    email_template_name = "password/password_reset_email.txt"