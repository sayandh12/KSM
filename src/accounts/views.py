from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser
from inquiries.models import Enquiry
from blog.models import Blog
from case_studies.models import CaseStudy
from gallery.models import GalleryImage
import json

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(request, "Registration failed.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def admin_dashboard(request):
    if request.user.is_superuser:
        total_users = CustomUser.objects.count()
        total_enquiries = Enquiry.objects.count()
        total_blogs = Blog.objects.count()
        total_case_studies = CaseStudy.objects.count()
        total_gallery = GalleryImage.objects.count()
    else:
        # Restricted counts for regular admins
        total_users = CustomUser.objects.count() # Still can see total users as per "Admin can view users"
        total_enquiries = Enquiry.objects.count() # Enquiries are usually shared, but user didn't specify. Assuming shared for now.
        total_blogs = Blog.objects.filter(author=request.user).count()
        total_case_studies = CaseStudy.objects.filter(added_by=request.user).count()
        total_gallery = GalleryImage.objects.filter(added_by=request.user).count()

    labels = []
    data = []
    current_date = timezone.now()
    
    for i in range(5, -1, -1):
        month_date = (current_date - timedelta(days=i*30))
        month_label = month_date.strftime('%b')
        labels.append(month_label)
        
        u_count = CustomUser.objects.filter(
            date_joined__year=month_date.year,
            date_joined__month=month_date.month
        ).count()
        e_count = Enquiry.objects.filter(
            created_at__year=month_date.year,
            created_at__month=month_date.month
        ).count()
        
        data.append(u_count + e_count)

    context = {
        'total_users': total_users,
        'total_enquiries': total_enquiries,
        'total_blogs': total_blogs,
        'total_case_studies': total_case_studies,
        'total_gallery': total_gallery,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    }
    return render(request, 'accounts/admin_dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    # Get enquiries linked to this user's email
    enquiries = Enquiry.objects.filter(email=user.email).order_by('-created_at')
    
    context = {
        'target_user': user,
        'enquiries': enquiries,
        'title': f"User Profile: {user.username}"
    }
    return render(request, 'accounts/user_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def user_create(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to create users.")
        return redirect('user_list')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Create User'})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def user_update(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit users.")
        return redirect('user_list')
        
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Update User', 'is_update': True})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def user_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete users.")
        return redirect('user_list')
        
    user = get_object_or_404(CustomUser, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot delete your own account from the dashboard.")
        return redirect('user_list')
        
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('user_list')
    return render(request, 'accounts/user_confirm_delete.html', {'object': user, 'title': 'Delete User'})
