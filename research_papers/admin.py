from django.contrib import admin
from .models import ResearchPaper


@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'abstract', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
