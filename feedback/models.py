from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Status choices for feedback approval
STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

# Feedback type choices
FEEDBACK_TYPE_CHOICES = (
    ('student', 'Student'),
    ('client', 'Client'),
)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    feedback_type = models.CharField(max_length=10, choices=FEEDBACK_TYPE_CHOICES)
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
            while Feedback.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{num}"
                num += 1
            
            self.slug = unique_slug
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"