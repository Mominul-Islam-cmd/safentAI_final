from django.contrib import admin
from .models import ResearchTopic


@admin.register(ResearchTopic)
class ResearchTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'subject', 'category', 'status', 'created_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'subject', 'description', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
