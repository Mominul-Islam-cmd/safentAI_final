from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

CATEGORY_CHOICES = (
    ('AI', 'AI'),
    ('Quantum', 'Quantum'),
    ('Hybrid', 'Hybrid'),
)

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)


class ResearchPaper(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    co_authors = models.CharField(max_length=255, blank=True)
    abstract = models.TextField()
    paper_link = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the initial slug
            slug = slugify(self.title)
            
            # Check for existing slugs and make this one unique
            unique_slug = slug
            num = 1
            while ResearchPaper.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{num}"
                num += 1
            
            self.slug = unique_slug
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
