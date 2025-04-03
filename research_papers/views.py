from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from .models import ResearchPaper
from .forms import ResearchPaperForm, ResearchPaperApprovalForm


def research_paper_list(request):
    category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    papers = ResearchPaper.objects.filter(status='approved')
    
    if category:
        papers = papers.filter(category=category)
    
    if search_query:
        papers = papers.filter(
            Q(title__icontains=search_query) | 
            Q(abstract__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Count papers by category for display
    ai_count = ResearchPaper.objects.filter(status='approved', category='AI').count()
    quantum_count = ResearchPaper.objects.filter(status='approved', category='Quantum').count()
    hybrid_count = ResearchPaper.objects.filter(status='approved', category='Hybrid').count()
    
    paginator = Paginator(papers, 9)  # Show 9 papers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'search_query': search_query,
        'ai_count': ai_count,
        'quantum_count': quantum_count,
        'hybrid_count': hybrid_count,
        'total_count': ai_count + quantum_count + hybrid_count,
    }
    
    return render(request, 'research_papers/paper_list.html', context)


def research_paper_detail(request, slug):
    paper = get_object_or_404(ResearchPaper, slug=slug, status='approved')
    return render(request, 'research_papers/paper_detail.html', {'paper': paper})


@login_required
def research_paper_create(request):
    if request.method == 'POST':
        form = ResearchPaperForm(request.POST)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.author = request.user
            paper.save()
            messages.success(request, 'Your research paper has been submitted for approval.')
            return redirect('research_paper_list')
    else:
        form = ResearchPaperForm()
    
    return render(request, 'research_papers/paper_form.html', {'form': form, 'action': 'Create'})


@login_required
def research_paper_edit(request, slug):
    paper = get_object_or_404(ResearchPaper, slug=slug)
    
    # Check if user has permission to edit
    if paper.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to edit this paper.")
    
    if request.method == 'POST':
        form = ResearchPaperForm(request.POST, instance=paper)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your research paper has been updated.')
            return redirect('research_paper_detail', slug=paper.slug)
    else:
        form = ResearchPaperForm(instance=paper)
    
    return render(request, 'research_papers/paper_form.html', {'form': form, 'action': 'Edit'})


@login_required
def research_paper_delete(request, slug):
    paper = get_object_or_404(ResearchPaper, slug=slug)
    
    # Check if user has permission to delete
    if paper.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to delete this paper.")
    
    if request.method == 'POST':
        paper.delete()
        messages.success(request, 'Your research paper has been deleted.')
        return redirect('research_paper_list')
    
    return render(request, 'research_papers/paper_confirm_delete.html', {'paper': paper})


@login_required
def my_research_papers(request):
    papers = ResearchPaper.objects.filter(author=request.user)
    return render(request, 'research_papers/my_papers.html', {'papers': papers})


@login_required
def research_paper_approval_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    papers = ResearchPaper.objects.filter(status='pending')
    return render(request, 'research_papers/paper_approval.html', {'papers': papers})


@login_required
def research_paper_approve(request, pk):
    if not request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    paper = get_object_or_404(ResearchPaper, pk=pk)
    
    if request.method == 'POST':
        form = ResearchPaperApprovalForm(request.POST, instance=paper)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
