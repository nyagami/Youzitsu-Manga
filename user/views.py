from django.contrib.auth.views import LoginView as OldLoginView, LogoutView as OldLogOutView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect

from registration.backends.simple.views import RegistrationView as OldRegistrationView

from .form import RegistrationForm

from utils.pw_valid import PwnedPasswordsValidator


# Create your views here.

#Registration
class RegistrationView(OldRegistrationView):
    title = "Đăng kí"
    form_class = RegistrationForm
    success_url = '/user/register/complete'

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

    def form_valid(self, form):
        password = form.cleaned_data['password']
        validator = PwnedPasswordsValidator()
        try:
            validator.validate(password)
        except ValidationError:
            self.request.session['password_pwned'] = True
        else:
            self.request.session['password_pwned'] = False
        return super().form_valid(form)


class LogoutView(OldLogOutView):
    template_name = 'log/logout.html'
    extra_context = {
        "page_title": "Đăng xuất",
    }