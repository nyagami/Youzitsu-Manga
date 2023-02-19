import re
from registration.forms import RegistrationForm as OldRegistrationForm

from django.contrib.auth.models import User

from django import forms


def valid_email(email):
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)


class RegistrationForm(OldRegistrationForm):
    username = forms.RegexField(regex=r'^\w+$', min_length=2, max_length=30, label="Tên người dùng")
    display_name = forms.CharField(max_length=50, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            print('yes')
            raise forms.ValidationError("Tên người dùng đã tồn tại!")
        return username

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(('Địa chỉ "%s" đã được sử dụng!.') % self.cleaned_data['email'])
        if not valid_email(self.cleaned_data['email']):
            raise forms.ValidationError("Mail không hợp lệ!")
        return self.cleaned_data['email']
