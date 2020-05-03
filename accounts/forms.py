from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    PasswordChangeForm,
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from accounts.models import UserProfile


def password_help_text_html():
    help_texts = [
        "Ваш пароль не может быть слишком похож на другую вашу личную информацию.",
        "Ваш пароль должен содержать не менее 8 символов.",
        "Ваш пароль не может быть часто используемым паролем.",
        "Ваш пароль не может состоять только из цифор.",
    ]
    help_items = [format_html('<li>{}</li>', help_text) for help_text in help_texts]
    return _('<ul>%s</ul>' % ''.join(help_items) if help_items else '')


class RegistrationForm(UserCreationForm):

    username = forms.CharField(label=_("Логин"))
    email = forms.EmailField(label=_("Email"), required=True)
    first_name = forms.CharField(label=_("Имя"))
    last_name = forms.CharField(label=_("Фамилия"))
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Повторите пароль"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Повторно введите пароль для подтверждения"),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class EditUserForm(UserChangeForm):
    email = forms.CharField(label=_("Email"))
    first_name = forms.CharField(label=_("Имя"))
    last_name = forms.CharField(label=_("Фамилия"))

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].label = _("Пароль")
        self.fields['password'].help_text = _("")


class EditUserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label=_("Фотография пользователя"))

    class Meta:
        model = UserProfile
        fields = ("avatar",)

    def save(self, user_id, commit=True):
        profile = UserProfile.objects.get(user_id=user_id)
        profile.avatar = self.cleaned_data.get("avatar")

        profile.save()
        return profile


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = _("Старый пароль")
        self.fields['new_password1'].label = _("Новый пароль")
        self.fields['new_password2'].label = _("Повторите новый пароль")
        self.fields['new_password1'].help_text = password_help_text_html()
