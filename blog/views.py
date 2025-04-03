from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from .models import BlogPost
from .forms import BlogPostForm, BlogPostApprovalForm


def blog_list(request):
    category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    posts = BlogPost.objects.filter(status='approved')
    
    if category:
        posts = posts.filter(category=category)
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Count posts by category
    ai_count = BlogPost.objects.filter(status='approved', category='AI').count()
    quantum_count = BlogPost.objects.filter(status='approved', category='Quantum').count()
    hybrid_count = BlogPost.objects.filter(status='approved', category='Hybrid').count()
    
    paginator = Paginator(posts, 9)  # Show 9 posts per page
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
    
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='approved')
    is_liked = False
    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            is_liked = True
    
    return render(request, 'blog/blog_detail.html', {'post': post, 'is_liked': is_liked})


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your blog post has been submitted for approval.')
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/blog_form.html', {'form': form, 'action': 'Create'})


@login_required
def blog_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if user has permission to edit
    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to edit this post.")
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            # Only set back to pending if not admin
            if not request.user.is_superuser:
                edited_post.status = 'pending'
                messages.info(request, 'Your blog post has been updated and submitted for approval.')
            else:
                messages.success(request, 'Your blog post has been updated successfully.')
            edited_post.save()
            
            # Redirect to my posts list if it's pending again, otherwise to the detail page
            if edited_post.status == 'pending':
                return redirect('my_blog_posts')
            else:
                return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/blog_form.html', {'form': form, 'action': 'Edit'})


@login_required
def blog_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if user has permission to delete
    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to delete this post.")
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your blog post has been deleted.')
        return redirect('blog_list')
    
    return render(request, 'blog/blog_confirm_delete.html', {'post': post})


@login_required
def my_blog_posts(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})


@login_required
def blog_approval_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    posts = BlogPost.objects.filter(status='pending')
    return render(request, 'blog/blog_approval.html', {'posts': posts})


@login_required
def blog_approve(request, pk):
    if not request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == 'POST':
        form = BlogPostApprovalForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def like_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({'status': 'success', 'likes_count': post.total_likes(), 'liked': liked})
