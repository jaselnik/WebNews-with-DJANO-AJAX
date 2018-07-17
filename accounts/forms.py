from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


<<<<<<< HEAD

from .models import UserProfile



=======
>>>>>>> 3ec144f17a8518fac5452626e5ad3279f4829cb5
class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )
<<<<<<< HEAD



class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'avatar'
        ]

=======
>>>>>>> 3ec144f17a8518fac5452626e5ad3279f4829cb5
