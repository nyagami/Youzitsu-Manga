from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import RegistrationView, LoginView, LogoutView

urlpatterns = [
    # path(""),
    path("register/", RegistrationView.as_view() , name="register_account"),
    path("register/complete/", TemplateView.as_view(
        template_name = "registration/registration_complete.html",
    )),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("password/change/"),
    # path("password/change/done"),
    # path("password/reset/"),
    # re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', name='password_reset_confirm'),
    # path("password/reset/complete/"),
    # path("password/reset/done/"),
    # path("<str:user>"),
    path("", include("registration.backends.simple.urls")),
]