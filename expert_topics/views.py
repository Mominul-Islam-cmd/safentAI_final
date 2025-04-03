from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from .models import ResearchTopic
from .forms import ResearchTopicForm, ResearchTopicApprovalForm


def research_topic_list(request):
    category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    topics = ResearchTopic.objects.filter(status='approved')
    
    if category:
        topics = topics.filter(category=category)
    
    if search_query:
        topics = topics.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    paginator = Paginator(topics, 10)  # Show 10 topics per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'search_query': search_query,
    }
    
    return render(request, 'expert_topics/topic_list.html', context)


def research_topic_detail(request, slug):
    topic = get_object_or_404(ResearchTopic, slug=slug, status='approved')
    return render(request, 'expert_topics/topic_detail.html', {'topic': topic})


@login_required
def research_topic_create(request):
    if request.method == 'POST':
        form = ResearchTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            messages.success(request, 'Your research topic has been submitted for approval.')
            return redirect('research_topic_list')
    else:
        form = ResearchTopicForm()
    
    return render(request, 'expert_topics/topic_form.html', {'form': form, 'action': 'Create'})


@login_required
def research_topic_edit(request, slug):
    topic = get_object_or_404(ResearchTopic, slug=slug)
    
    # Check if user has permission to edit
    if topic.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to edit this topic.")
    
    if request.method == 'POST':
        form = ResearchTopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your research topic has been updated.')
            return redirect('research_topic_detail', slug=topic.slug)
    else:
        form = ResearchTopicForm(instance=topic)
    
    return render(request, 'expert_topics/topic_form.html', {'form': form, 'action': 'Edit'})


@login_required
def research_topic_delete(request, slug):
    topic = get_object_or_404(ResearchTopic, slug=slug)
    
    # Check if user has permission to delete
    if topic.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to delete this topic.")
    
    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Your research topic has been deleted.')
        return redirect('research_topic_list')
    
    return render(request, 'expert_topics/topic_confirm_delete.html', {'topic': topic})


@login_required
def my_research_topics(request):
    topics = ResearchTopic.objects.filter(author=request.user)
    return render(request, 'expert_topics/my_topics.html', {'topics': topics})


@login_required
def research_topic_approval_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    topics = ResearchTopic.objects.filter(status='pending')
    return render(request, 'expert_topics/topic_approval.html', {'topics': topics})


@login_required
def research_topic_approve(request, pk):
    if not request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    topic = get_object_or_404(ResearchTopic, pk=pk)
    
    if request.method == 'POST':
        form = ResearchTopicApprovalForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def become_expert_guidelines(request):
    return render(request, 'expert_topics/become_expert_guidelines.html')
