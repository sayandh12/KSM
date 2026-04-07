from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Blog
from .forms import BlogForm

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog/list.html', {'blogs': blogs})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def blog_list_admin(request):
    if request.user.is_superuser:
        blogs = Blog.objects.all().order_by('-created_at')
    else:
        blogs = Blog.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/admin_list.html', {'blogs': blogs})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, "Blog post published successfully.")
            return redirect('blog_list_admin')
    else:
        form = BlogForm()
    return render(request, 'blog/blog_form.html', {'form': form, 'title': 'Create Blog'})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if not request.user.is_superuser and blog.author != request.user:
        messages.error(request, "You can only edit your own blog posts.")
        return redirect('blog_list_admin')
        
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated '{blog.title}'")
            return redirect('blog_list_admin')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_form.html', {'form': form, 'title': 'Update Blog', 'is_update': True})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if not request.user.is_superuser and blog.author != request.user:
        messages.error(request, "You can only delete your own blog posts.")
        return redirect('blog_list_admin')
        
    if request.method == 'POST':
        title = blog.title
        blog.delete()
        messages.success(request, f"Deleted '{title}'")
        return redirect('blog_list_admin')
    return render(request, 'blog/blog_confirm_delete.html', {'object': blog, 'title': 'Delete Blog'})
