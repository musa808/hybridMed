from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, ProfileForm
from .models import Profile


# ================= REGISTER =================


def register_view(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user
            user = user_form.save()

            # Save the profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Account created successfully!")
            return redirect('accounts:login')
        else:
            # Debugging: print errors
            print(user_form.errors)
            print(profile_form.errors)

    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
# ================= LOGIN =================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Role-based redirect
            if user.is_staff:
                return redirect('appointment:admin_dashboard')

            if user.profile.role == "doctor":
                return redirect('doctors:doctor_dashboard')

            if user.profile.role == "patient":
                return redirect('patients:patient_dashboard')

            return redirect('home_view')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('home_view')


# ================= PROFILE =================
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
