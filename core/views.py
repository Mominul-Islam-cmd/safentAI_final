from django.shortcuts import render
from django.db.models import Count
from research_papers.models import ResearchPaper
from blog.models import BlogPost
from expert_topics.models import ResearchTopic


def home(request):
    # Get counts for dashboard display
    research_papers_count = ResearchPaper.objects.filter(status='approved').count()
    blog_count = BlogPost.objects.filter(status='approved').count()
    topics_count = ResearchTopic.objects.filter(status='approved').count()
    
    # Get recent research papers for display
    recent_papers = ResearchPaper.objects.filter(status='approved').order_by('-created_at')[:3]
    
    context = {
        'research_papers_count': research_papers_count,
        'blog_count': blog_count,
        'topics_count': topics_count,
        'recent_papers': recent_papers,
    }
    
    # Check if the new template exists, otherwise fall back to the original
    try:
        return render(request, 'new_designs/home.html', context)
    except:
        return render(request, 'home.html', context)


def about(request):
    # Check if the new template exists, otherwise fall back to the original
    try:
        return render(request, 'new_designs/about.html')
    except:
        return render(request, 'about.html')
