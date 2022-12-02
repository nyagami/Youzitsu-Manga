from django.shortcuts import render

from django.contrib.auth.models import User

from django import forms
from django_registration.backends.one_step.views import RegistrationView as OldRegistrationView
from django_registration.forms import RegistrationForm as OldRegistrationForm

# Create your views here.

class RegistrationForm(OldRegistrationForm):
    username = forms.RegexField(regex=r'^\w+$', max_length=30, label="Tên người dùng",
                                error_messages={'Không hợp lệ': "Tên người dùng chỉ có kí tự hoặc số hoặc _"})

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(('Địa chỉ "%s" đã được sử dụng!.') % self.cleaned_data['email'])
        return self.cleaned_data['email']


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
