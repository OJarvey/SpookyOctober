from django.contrib import admin
from .models import StoryTemplate, VocabularyWord, CompletedMadLib


@admin.register(StoryTemplate)
class StoryTemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'difficulty', 'word_count', 'is_active', 'created_at']
    list_filter = ['difficulty', 'is_active', 'created_at']
    search_fields = ['title', 'author', 'template_text']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'author', 'difficulty', 'word_count', 'is_active']
        }),
        ('Template Content', {
            'fields': ['original_text', 'template_text'],
            'description': 'Use placeholders like [NOUN], [ADJECTIVE], [VERB], [ADVERB] in template_text'
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(VocabularyWord)
class VocabularyWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'part_of_speech', 'category', 'is_kid_friendly', 'created_at']
    list_filter = ['part_of_speech', 'category', 'is_kid_friendly']
    search_fields = ['word']
    actions = ['mark_kid_friendly', 'mark_not_kid_friendly']

    def mark_kid_friendly(self, request, queryset):
        updated = queryset.update(is_kid_friendly=True)
        self.message_user(request, f'{updated} words marked as kid-friendly.')
    mark_kid_friendly.short_description = "Mark selected as kid-friendly"

    def mark_not_kid_friendly(self, request, queryset):
        updated = queryset.update(is_kid_friendly=False)
        self.message_user(request, f'{updated} words marked as not kid-friendly.')
    mark_not_kid_friendly.short_description = "Mark selected as not kid-friendly"


@admin.register(CompletedMadLib)
class CompletedMadLibAdmin(admin.ModelAdmin):
    list_display = ['template', 'user', 'share_code', 'is_public', 'view_count', 'created_at']
    list_filter = ['is_public', 'created_at', 'template']
    search_fields = ['share_code', 'completed_text', 'user__username']
    readonly_fields = ['share_code', 'created_at', 'view_count', 'completed_text']
    actions = ['make_public', 'make_private']

    def make_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f'{updated} Mad Libs made public.')
    make_public.short_description = "Make selected Mad Libs public"

    def make_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f'{updated} Mad Libs made private.')
    make_private.short_description = "Make selected Mad Libs private"
