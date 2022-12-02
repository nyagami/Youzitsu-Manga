from django.urls import path, include
from .views import RegistrationView

urlpatterns = [
    path("register/", RegistrationView.as_view(success_url='/profile/') , name="register_account"),
    path("", include("django_registration.backends.one_step.urls")),
    path("", include("django.contrib.auth.urls")),
]