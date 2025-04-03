from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.urls import reverse

from .models import Feedback
from .forms import FeedbackForm, FeedbackApprovalForm

def feedback_list(request):
    feedback_type = request.GET.get('type')
    
    # Only show approved feedback
    feedbacks = Feedback.objects.filter(status='approved')
    
    # Filter by type if specified
    if feedback_type:
        feedbacks = feedbacks.filter(feedback_type=feedback_type)
    
    # Pagination
    paginator = Paginator(feedbacks, 6)  # Show 6 feedbacks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_type': feedback_type,
    }
    return render(request, 'feedback/feedback_list.html', context)

@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted and is awaiting approval.')
            return redirect('my_feedbacks')
    else:
        form = FeedbackForm()
    
    context = {
        'form': form,
    }
    return render(request, 'feedback/feedback_form.html', context)

@login_required
def feedback_edit(request, slug):
    feedback = get_object_or_404(Feedback, slug=slug)
    
    # Check if the user is the owner of the feedback or an admin
    if feedback.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to edit this feedback.")
    
    # Store the original feedback status
    original_status = feedback.status
    was_approved = original_status == 'approved'
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            updated_feedback = form.save(commit=False)
            
            # Only set back to pending if not admin
            if not request.user.is_superuser:
                updated_feedback.status = 'pending'
                if was_approved:
                    messages.info(request, 'Your feedback has been updated and is now awaiting admin approval again.')
                else:
                    messages.info(request, 'Your feedback has been updated and is awaiting admin review.')
            else:
                messages.success(request, 'Your feedback has been updated successfully.')
            
            updated_feedback.save()
            return redirect('my_feedbacks')
    else:
        form = FeedbackForm(instance=feedback)
    
    context = {
        'form': form,
        'feedback': feedback,
        'is_edit': True,
        'was_approved': was_approved,
    }
    return render(request, 'feedback/feedback_form.html', context)

@login_required
def feedback_delete(request, slug):
    feedback = get_object_or_404(Feedback, slug=slug)
    
    # Only admin users can delete feedback
    if not request.user.is_superuser:
        messages.error(request, "Only administrators can delete feedback.")
        return redirect('my_feedbacks')
    
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback has been deleted successfully.')
        
        # Redirect to appropriate page based on where the admin came from
        referer = request.META.get('HTTP_REFERER', '')
        if 'approval' in referer:
            return redirect('feedback_approval_list')
        else:
            return redirect('my_feedbacks')
    
    context = {
        'feedback': feedback,
    }
    return render(request, 'feedback/feedback_confirm_delete.html', context)

@login_required
def my_feedbacks(request):
    feedbacks = Feedback.objects.filter(user=request.user)
    
    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'feedback/my_feedbacks.html', context)

@login_required
def feedback_approval_list(request):
    # Only superuser can access this view
    if not request.user.is_superuser:
        messages.warning(request, "You don't have permission to view this page.")
        return redirect('home')
    
    # Get all feedbacks for approval, sorted by creation date
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'feedback/feedback_approval_list.html', context)

@login_required
def feedback_approve(request, pk):
    # Only superuser can access this view
    if not request.user.is_superuser:
        messages.warning(request, "You don't have permission to perform this action.")
        return redirect('home')
    
    feedback = get_object_or_404(Feedback, pk=pk)
    original_status = feedback.status
    
    if request.method == 'POST':
        form = FeedbackApprovalForm(request.POST, instance=feedback)
        if form.is_valid():
            updated_feedback = form.save(commit=False)
            new_status = form.cleaned_data['status']
            
            # Ensure we have a status change
            if original_status != new_status:
                updated_feedback.status = new_status
                updated_feedback.save()
                
                status_msg = {
                    'approved': 'Feedback has been approved and published.',
                    'rejected': 'Feedback has been rejected.',
                    'pending': 'Feedback has been set to pending review.'
                }
                messages.success(request, status_msg[new_status])
            else:
                messages.info(request, f"Feedback status remains '{new_status}'.")
                
            return redirect('feedback_approval_list')
    else:
        form = FeedbackApprovalForm(instance=feedback)
    
    context = {
        'form': form,
        'feedback': feedback,
    }
    return render(request, 'feedback/feedback_approval_form.html', context)