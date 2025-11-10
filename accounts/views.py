from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegisterForm, UserForm, ProfileForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            # Profile auto-created by signal
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
