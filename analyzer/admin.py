from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Admin interface for managing feedback entries."""
    list_display = ('sentiment', 'compound_score', 'feedback_text', 'created_at')
    list_filter = ('sentiment', 'created_at')
    search_fields = ('feedback_text',)
    readonly_fields = ('created_at',)
