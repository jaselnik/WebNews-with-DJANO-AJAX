from django.contrib.auth.views import (
    login,
    logout,
    password_reset,
    password_reset_complete,
    password_reset_confirm,
    password_reset_done,
)
from django.urls import path, re_path

from accounts.views import (
    ChangePasswordView,
    EditUserView,
    EditUserProfileView,
    ProfileView,
    RegisterView,
)

app_name = "accounts"

urlpatterns = [
    re_path(r"^(?P<pk>\d+)/$", ProfileView.as_view(), name="view_profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", login, {"template_name": "accounts/login.html"}, name="login"),
    path("logout/", logout, {"template_name": "accounts/logout.html"}, name="logout"),
    path("edit/", EditUserView.as_view(), name="edit_user"),
    path("edit-profile/", EditUserProfileView.as_view(), name="edit_profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path(
        "reset-password/",
        password_reset,
        {
            "template_name": "accounts/reset_password.html",
            "post_reset_redirect": "accounts:password_reset_done",
            "email_template_name": "accounts/reset_password_email.html",
        },
        name="reset_password",
    ),
    path(
        "reset-password/done/",
        password_reset_done,
        {"template_name": "accounts/reset_password_done.html"},
        name="password_reset_done",
    ),
    re_path(
        r"reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        password_reset_confirm,
        {
            "template_name": "accounts/reset_password_confirm.html",
            "post_reset_redirect": "accounts:password_reset_complete",
        },
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        password_reset_complete,
        {"template_name": "accounts/reset_password_complete.html"},
        name="password_reset_complete",
    ),
]
