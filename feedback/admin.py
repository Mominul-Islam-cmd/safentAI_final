from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'feedback_type', 'rating', 'status', 'created_at')
    list_filter = ('feedback_type', 'status', 'rating', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

admin.site.register(Feedback, FeedbackAdmin)