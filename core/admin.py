"""
Admin Dashboard Configuration for ShriekedIn

Registers all core models with customized list displays, filters,
and search fields for easy management.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    UserProfile,
    Location,
    Event,
    Media,
    HauntedPlace,
    Business,
    Coupon,
    Post,
    Like,
    Comment
)


# ================================================================
# USER PROFILE ADMIN
# ================================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'location', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_type', 'location')
        }),
        ('Profile Details', {
            'fields': ('bio', 'favorite_halloween_activity', 'profile_photo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ================================================================
# LOCATION ADMIN
# ================================================================

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'location_type', 'is_verified', 'created_by']
    list_filter = ['location_type', 'is_verified', 'state', 'country']
    search_fields = ['name', 'address', 'city', 'state']
    readonly_fields = ['created_date']
    list_editable = ['is_verified']

    fieldsets = (
        ('Location Information', {
            'fields': ('name', 'location_type', 'description')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Coordinates', {
            'fields': ('latitude', 'longitude'),
            'description': 'Geographic coordinates for map display'
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_date', 'is_verified')
        }),
    )


# ================================================================
# EVENT ADMIN
# ================================================================

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'event_category', 'cost_display', 'is_active', 'is_featured', 'view_count']
    list_filter = ['event_category', 'age_appropriateness', 'is_active', 'is_featured', 'event_date']
    search_fields = ['title', 'description', 'location__name']
    readonly_fields = ['slug', 'created_date', 'modified_date', 'view_count', 'like_count']
    list_editable = ['is_active', 'is_featured']
    prepopulated_fields = {}  # Slug auto-generated in model
    date_hierarchy = 'event_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'event_category')
        }),
        ('Location & Time', {
            'fields': ('location', 'event_date', 'start_time', 'end_time')
        }),
        ('Event Details', {
            'fields': ('cost', 'age_appropriateness', 'capacity')
        }),
        ('Additional Information', {
            'fields': ('performing_artists', 'contact_info', 'website_url'),
            'classes': ('collapse',)
        }),
        ('Management', {
            'fields': ('created_by', 'is_active', 'is_featured')
        }),
        ('Engagement Metrics', {
            'fields': ('view_count', 'like_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_date', 'modified_date'),
            'classes': ('collapse',)
        }),
    )

    def cost_display(self, obj):
        if obj.is_free:
            return format_html('<span style="color: green;">FREE</span>')
        return f"${obj.cost}"
    cost_display.short_description = 'Cost'


# ================================================================
# MEDIA ADMIN
# ================================================================

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'entity_type', 'entity_id', 'file_type', 'uploaded_by', 'upload_date']
    list_filter = ['entity_type', 'file_type', 'upload_date']
    search_fields = ['caption', 'alt_text']
    readonly_fields = ['upload_date']

    fieldsets = (
        ('Association', {
            'fields': ('entity_type', 'entity_id')
        }),
        ('File Information', {
            'fields': ('file', 'file_type', 'caption', 'alt_text')
        }),
        ('Display Order', {
            'fields': ('order',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'upload_date')
        }),
    )


# ================================================================
# HAUNTED PLACE ADMIN
# ================================================================

@admin.register(HauntedPlace)
class HauntedPlaceAdmin(admin.ModelAdmin):
    list_display = ['story_title', 'location', 'scare_level_display', 'is_educational', 'created_by', 'view_count']
    list_filter = ['scare_level', 'is_educational', 'created_date']
    search_fields = ['story_title', 'story_content', 'location__name']
    readonly_fields = ['created_date', 'modified_date', 'view_count', 'visit_count']
    list_editable = ['is_educational']

    fieldsets = (
        ('Location', {
            'fields': ('location',)
        }),
        ('Story Content', {
            'fields': ('story_title', 'story_content', 'historical_context')
        }),
        ('Details', {
            'fields': ('scare_level', 'is_educational', 'year_established')
        }),
        ('Paranormal Information', {
            'fields': ('reported_phenomena', 'famous_for'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_date', 'modified_date')
        }),
        ('Engagement', {
            'fields': ('view_count', 'visit_count'),
            'classes': ('collapse',)
        }),
    )

    def scare_level_display(self, obj):
        colors = {1: '#90EE90', 2: '#FFD700', 3: '#FFA500', 4: '#FF6347', 5: '#8B0000'}
        color = colors.get(obj.scare_level, '#000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, obj.get_scare_level_display()
        )
    scare_level_display.short_description = 'Scare Level'


# ================================================================
# BUSINESS ADMIN
# ================================================================

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'business_type', 'location', 'verified_display', 'is_active']
    list_filter = ['business_type', 'verified', 'is_active', 'created_date']
    search_fields = ['business_name', 'description', 'email']
    readonly_fields = ['slug', 'created_date', 'modified_date', 'verified_date']
    list_editable = ['is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'business_name', 'slug', 'business_type', 'description')
        }),
        ('Location', {
            'fields': ('location',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website', 'hours_of_operation')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_handle'),
            'classes': ('collapse',)
        }),
        ('Verification', {
            'fields': ('verified', 'verified_date')
        }),
        ('Status', {
            'fields': ('is_active', 'created_date', 'modified_date')
        }),
    )

    def verified_display(self, obj):
        if obj.verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        return format_html('<span style="color: gray;">Not Verified</span>')
    verified_display.short_description = 'Verification'


# ================================================================
# COUPON ADMIN
# ================================================================

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['title', 'business', 'discount_code', 'discount_display', 'valid_from', 'valid_until', 'is_active', 'usage_display']
    list_filter = ['is_active', 'valid_from', 'valid_until', 'created_date']
    search_fields = ['title', 'discount_code', 'business__business_name']
    readonly_fields = ['created_date', 'current_uses']
    list_editable = ['is_active']
    date_hierarchy = 'valid_from'

    fieldsets = (
        ('Business', {
            'fields': ('business',)
        }),
        ('Coupon Details', {
            'fields': ('title', 'description', 'discount_code')
        }),
        ('Discount', {
            'fields': ('discount_percentage', 'discount_amount'),
            'description': 'Set either percentage OR amount, not both'
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until', 'terms_and_conditions')
        }),
        ('Usage Limits', {
            'fields': ('max_uses', 'current_uses')
        }),
        ('Status', {
            'fields': ('is_active', 'created_date')
        }),
    )

    def discount_display(self, obj):
        if obj.discount_percentage:
            return f"{obj.discount_percentage}% off"
        elif obj.discount_amount:
            return f"${obj.discount_amount} off"
        return "No discount"
    discount_display.short_description = 'Discount'

    def usage_display(self, obj):
        if obj.max_uses:
            percentage = (obj.current_uses / obj.max_uses) * 100
            return f"{obj.current_uses}/{obj.max_uses} ({percentage:.0f}%)"
        return f"{obj.current_uses}/∞"
    usage_display.short_description = 'Usage'


# ================================================================
# POST ADMIN
# ================================================================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_type', 'content_preview', 'created_date', 'is_public', 'is_active', 'engagement_display']
    list_filter = ['post_type', 'is_public', 'is_active', 'created_date']
    search_fields = ['content', 'user__username']
    readonly_fields = ['created_date', 'modified_date', 'like_count', 'comment_count', 'share_count']
    list_editable = ['is_active']
    date_hierarchy = 'created_date'

    fieldsets = (
        ('Author', {
            'fields': ('user',)
        }),
        ('Content', {
            'fields': ('post_type', 'content')
        }),
        ('Reference (Optional)', {
            'fields': ('reference_type', 'reference_id'),
            'classes': ('collapse',),
            'description': 'Link to related content (event, place, etc.)'
        }),
        ('Visibility', {
            'fields': ('is_public', 'is_active')
        }),
        ('Engagement', {
            'fields': ('like_count', 'comment_count', 'share_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_date', 'modified_date'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:75] + '...' if len(obj.content) > 75 else obj.content
    content_preview.short_description = 'Content'

    def engagement_display(self, obj):
        return f"❤️ {obj.like_count} | 💬 {obj.comment_count}"
    engagement_display.short_description = 'Engagement'


# ================================================================
# LIKE ADMIN
# ================================================================

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'entity_type', 'entity_id', 'created_date']
    list_filter = ['entity_type', 'created_date']
    search_fields = ['user__username']
    readonly_fields = ['created_date']
    date_hierarchy = 'created_date'


# ================================================================
# COMMENT ADMIN
# ================================================================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'entity_type', 'entity_id', 'content_preview', 'is_reply_display', 'created_date', 'is_active']
    list_filter = ['entity_type', 'is_active', 'is_flagged', 'created_date']
    search_fields = ['content', 'user__username']
    readonly_fields = ['created_date', 'modified_date', 'is_edited', 'like_count']
    list_editable = ['is_active']
    date_hierarchy = 'created_date'

    fieldsets = (
        ('Author', {
            'fields': ('user',)
        }),
        ('Content', {
            'fields': ('entity_type', 'entity_id', 'content')
        }),
        ('Threading', {
            'fields': ('parent_comment',),
            'description': 'Leave blank for top-level comment'
        }),
        ('Moderation', {
            'fields': ('is_active', 'is_flagged')
        }),
        ('Engagement', {
            'fields': ('like_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_date', 'modified_date', 'is_edited'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

    def is_reply_display(self, obj):
        if obj.is_reply:
            return format_html('<span style="color: blue;">↳ Reply</span>')
        return format_html('<span style="color: gray;">Top-level</span>')
    is_reply_display.short_description = 'Type'


# ================================================================
# CUSTOM ADMIN SITE CONFIGURATION
# ================================================================

# Customize admin site headers
admin.site.site_header = "🎃 ShriekedIn Admin Dashboard"
admin.site.site_title = "ShriekedIn Admin"
admin.site.index_title = "Halloween Platform Management"
