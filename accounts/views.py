from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import Hospital
from accidentapp.models import Accident
from django.contrib.auth.forms import UserCreationForm

# ----------------------
# Signup view
# ----------------------
def signup_view(request):
    """Handles user registration for hospital/admin users."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


# ----------------------
# Login view
# ----------------------
def login_view(request):
    """Handles login for hospital/admin users."""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to dashboard of hospital with ID = 1
            return redirect('hospital_dashboard', hospital_id=1)
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'accounts/login.html')

# ----------------------
# Logout view
# ----------------------
def logout_view(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    return redirect('login')

# ---------------------------
# Hospital Dashboard Views
# ---------------------------
@login_required
def dashboard(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)

    accidents = Accident.objects.filter(
        hospital=hospital
    ).order_by('-time')[:10]

    return render(request, "accounts/dashboard.html", {
        "hospital": hospital,
        "accidents": accidents
    })
