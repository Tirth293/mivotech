from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.middleware.csrf import get_token
from .models import Feedback, AdminProfile
import os


# =====================================================
# SUPERUSER CHECK
# =====================================================
def superuser_check(user):
    return user.is_authenticated and user.is_superuser


# =====================================================
# HOME PAGE
# =====================================================

def home(request):
    return render(request, "index.html")


# =====================================================
# ADMIN DASHBOARD
# =====================================================
@user_passes_test(superuser_check)
def admin_dashboard(request):
    feedbacks = Feedback.objects.all().order_by("-created_at")
    return render(request, "admin_panel/dashboard.html", {
        "feedbacks": feedbacks
    })


# =====================================================
# DELETE FEEDBACK
# =====================================================
@user_passes_test(superuser_check)
def delete_feedback(request, id):
    fb = get_object_or_404(Feedback, id=id)
    fb.delete()
    messages.success(request, "Feedback deleted successfully.")
    return redirect("admin_dashboard")


# =====================================================
# SUBMIT FEEDBACK (FROM WEBSITE)
# =====================================================
def submit_feedback(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            Feedback.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, "Thank you for your feedback!")
        else:
            messages.error(request, "All fields are required.")

        return redirect("home")

    return redirect("home")


# =====================================================
# EDIT FEEDBACK
# =====================================================
@user_passes_test(superuser_check)
def edit_feedback(request, id):
    feedback = get_object_or_404(Feedback, id=id)

    if request.method == "POST":
        feedback.message = request.POST.get("message")
        feedback.save()
        messages.success(request, "Feedback updated successfully.")
        return redirect("admin_dashboard")

    return render(request, "admin_panel/edit_feedback.html", {
        "feedback": feedback
    })


# =====================================================
# EDIT ADMIN PROFILE
# =====================================================
@user_passes_test(superuser_check)
def edit_profile(request):
    user = request.user
    
    # Get or create AdminProfile
    try:
        admin_profile = user.adminprofile
    except AdminProfile.DoesNotExist:
        admin_profile = AdminProfile.objects.create(user=user)

    if request.method == "POST":
        # Update user basic info
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()

        # Handle profile image upload
        if request.FILES.get("profile_image"):
            profile_image = request.FILES["profile_image"]
            
            # Validate file type
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = os.path.splitext(profile_image.name)[1].lower()
            
            if ext in valid_extensions:
                # Delete old image if it's not the default
                if admin_profile.profile_image and admin_profile.profile_image.name != 'admin_profiles/default.png':
                    if os.path.isfile(admin_profile.profile_image.path):
                        os.remove(admin_profile.profile_image.path)
                
                # Save new image
                admin_profile.profile_image = profile_image
                admin_profile.save()
                messages.success(request, "Profile image updated successfully.")
            else:
                messages.error(request, "Invalid image format. Please upload JPG, JPEG, PNG, or GIF.")

        messages.success(request, "Profile updated successfully.")
        return redirect("admin_dashboard")

    return render(request, "admin_panel/edit_profile.html", {
        "user": user,
        "admin_profile": admin_profile
    })


# =====================================================
# CHANGE PASSWORD
# =====================================================
@user_passes_test(superuser_check)
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("change_password")

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("change_password")

        # Additional password strength checks
        if new_password.isdigit() or new_password.isalpha():
            messages.error(request, "Password must contain both letters and numbers.")
            return redirect("change_password")

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, "Password updated successfully.")
        return redirect("admin_dashboard")

    return render(request, "admin_panel/change_password.html")


# =====================================================
# ADMIN LOGIN (SUPERUSER ONLY)
# =====================================================
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            # Force CSRF token refresh
            get_token(request)
            messages.success(request, "Welcome back, Admin!")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid credentials or not authorized.")

    return render(request, "admin_panel/login.html")


# =====================================================
# ADMIN LOGOUT
# =====================================================
def admin_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("admin_login")
