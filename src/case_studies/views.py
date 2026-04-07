from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CaseStudy
from .forms import CaseStudyForm


def case_study_list(request):
    cases = CaseStudy.objects.all().order_by('-created_at')
    return render(request, 'case_studies/list.html', {'cases': cases})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def case_study_list_admin(request):
    if request.user.is_superuser:
        cases = CaseStudy.objects.all().order_by('-created_at')
    else:
        cases = CaseStudy.objects.filter(added_by=request.user).order_by('-created_at')
    return render(request, 'case_studies/admin_list.html', {'cases': cases})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def case_study_create(request):
    if request.method == 'POST':
        form = CaseStudyForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save(commit=False)
            case.added_by = request.user
            case.save()
            messages.success(request, "Case study added successfully.")
            return redirect('case_studies_admin_list')
    else:
        form = CaseStudyForm()
    return render(request, 'case_studies/case_study_form.html', {'form': form, 'title': 'Add Case Study'})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def case_study_update(request, pk):
    case = get_object_or_404(CaseStudy, pk=pk)
    if not request.user.is_superuser and case.added_by != request.user:
        messages.error(request, "You can only edit your own case studies.")
        return redirect('case_studies_admin_list')
        
    if request.method == 'POST':
        form = CaseStudyForm(request.POST, request.FILES, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated '{case.title}'")
            return redirect('case_studies_admin_list')
    else:
        form = CaseStudyForm(instance=case)
    return render(request, 'case_studies/case_study_form.html', {'form': form, 'title': 'Update Case Study', 'is_update': True})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin)
def case_study_delete(request, pk):
    case = get_object_or_404(CaseStudy, pk=pk)
    if not request.user.is_superuser and case.added_by != request.user:
        messages.error(request, "You can only delete your own case studies.")
        return redirect('case_studies_admin_list')
        
    if request.method == 'POST':
        title = case.title
        case.delete()
        messages.success(request, f"Deleted '{title}'")
        return redirect('case_studies_admin_list')
    return render(request, 'case_studies/case_study_confirm_delete.html', {'object': case, 'title': 'Delete Case Study'})
