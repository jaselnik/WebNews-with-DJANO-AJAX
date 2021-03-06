from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from mainapp.models import Repost

from .forms import EditProfileForm, EditUserProfileForm, RegistrationForm
from .models import UserProfile


class EditUserProfile(LoginRequiredMixin, TemplateView):

    template_name = "accounts/edituserprofile.html"

    def get(self, request, *args, **kwargs):
        form = EditUserProfileForm()

        args = {"form": form}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        form = EditUserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = UserProfile.objects.get(user=request.user)
            user.avatar = form.cleaned_data.get("avatar")
            user.save()
            return redirect("/")
        args = {"form": form}
        return render(request, self.template_name, args)


class RegisterView(TemplateView):

    template_name = "accounts/reg_form.html"

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        args = {"form": form}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            form.save()
            return redirect("/")
        args = {"form": form}
        return render(request, self.template_name, args)


class EditProfileView(LoginRequiredMixin, TemplateView):

    template_name = "accounts/edit_profile.html"

    def get(self, request, *args, **kwargs):
        form = EditProfileForm(instance=request.user)
        args = {"form": form}
        return render(request, "accounts/edit_profile.html", args)

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("accounts:view_profile")


class ChangePasswordView(TemplateView):

    template_name = "accounts/change_password.html"

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user)
        args = {"form": form}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:view_profile")
        else:
            return redirect("accounts:change_password")


class ProfileView(TemplateView):

    template_name = "accounts/profile.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        user = User.objects.get(pk=pk)
        reposts = Repost.objects.filter(author=user).order_by("-timestamp")
        args = {"user": user, "reposts": reposts}
        return render(request, self.template_name, args)
