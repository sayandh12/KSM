from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Enquiry

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def enquiry_list(request):
    enquiries = Enquiry.objects.all().order_by('-created_at')
    return render(request, 'inquiries/enquiry_list.html', {'enquiries': enquiries})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def enquiry_view(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    return render(request, 'inquiries/enquiry_detail.html', {'enquiry': enquiry})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def enquiry_delete(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        enquiry.delete()
        return redirect('enquiry_list')
    return render(request, 'inquiries/enquiry_confirm_delete.html', {'object': enquiry, 'title': 'Delete Enquiry'})
