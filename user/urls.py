from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    PasswordChangeDoneView, PasswordResetCompleteView,
    PasswordResetConfirmView, PasswordResetDoneView
)

from .views import RegistrationView, LoginView, LogoutView, PasswordChangeView, PasswordResetView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register_account"),
    path("", TemplateView.as_view(
        template_name="registration/registration_complete.html",
    ), name="registration_complete"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("password/change/done", PasswordChangeDoneView.as_view(
        template_name="password/password_change_done.html",
    ), name="password_change_done"),
    path("password/reset/", PasswordResetView.as_view(), name="reset password"),
    re_path(r'password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$',
            PasswordResetConfirmView.as_view(
                template_name="password/password_reset_confirm.html",
                extra_context={
                    "page_title": "Xác nhận",
                }
            ), name='password_reset_confirm'),
    path("password/reset/complete/", PasswordResetCompleteView.as_view(
        template_name="password/password_change_done.html",
    ), name="password_reset_complete"),
    path("password/reset/done/", PasswordResetDoneView.as_view(
        template_name="password/password_reset_done.html",
    ), name="password_reset_done"),
    # path("<str:user>"),
]
