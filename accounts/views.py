from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, UserForm, ProfileForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            # Profile auto-created by signal (or fallback in profile view)
            login(request, user)
            messages.success(request, "Welcome to Rowdy Mart! Your account is ready.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        uform = UserForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, instance=profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Account settings updated.")
            return redirect("profile")
    else:
        uform = UserForm(instance=request.user)
        pform = ProfileForm(instance=profile)

    context = {
        "uform": uform,
        "pform": pform,
    }
    return render(request, "accounts/profile.html", context)
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_to_login(request):
    logout(request)
    return redirect("login")
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  # ✅ actually updates the password in the DB
            update_session_auth_hash(request, user)  # ✅ keep user logged in
            messages.success(request, "Your password was updated successfully.")
            return redirect("password_change_done")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "accounts/password_change.html", {"form": form})
