from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import GalleryImage
from .forms import GalleryForm

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def gallery_list_admin(request):
    if request.user.is_superuser:
        images = GalleryImage.objects.all().order_by('-uploaded_at')
    else:
        images = GalleryImage.objects.filter(added_by=request.user).order_by('-uploaded_at')
    return render(request, 'gallery/admin_list.html', {'images': images})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def gallery_create(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.added_by = request.user
            image.save()
            messages.success(request, "Photo added to gallery.")
            return redirect('gallery_admin_list')
    else:
        form = GalleryForm()
    return render(request, 'gallery/gallery_form.html', {'form': form, 'title': 'Add Photo'})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def gallery_update(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    if not request.user.is_superuser and image.added_by != request.user:
        messages.error(request, "You can only edit your own gallery photos.")
        return redirect('gallery_admin_list')
        
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo updated successfully.")
            return redirect('gallery_admin_list')
    else:
        form = GalleryForm(instance=image)
    return render(request, 'gallery/gallery_form.html', {'form': form, 'title': 'Update Photo', 'is_update': True})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def gallery_delete(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    if not request.user.is_superuser and image.added_by != request.user:
        messages.error(request, "You can only delete your own gallery photos.")
        return redirect('gallery_admin_list')
        
    if request.method == 'POST':
        image.delete()
        messages.success(request, "Photo deleted successfully.")
        return redirect('gallery_admin_list')
    return render(request, 'gallery/gallery_confirm_delete.html', {'object': image, 'title': 'Delete Photo'})
