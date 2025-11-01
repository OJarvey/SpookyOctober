"""
Admin Dashboard Configuration for ShriekedIn

Registers all core models with customized list displays, filters,
and search fields for easy management.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.http import HttpResponseRedirect
import csv
import io
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
    Comment,
    ContactMessage
)
from .forms import ImportHauntedPlacesForm


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

    def get_urls(self):
        """Add custom URL for CSV import"""
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='core_hauntedplace_import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        """Handle CSV import view"""
        if request.method == 'POST':
            form = ImportHauntedPlacesForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                update_existing = form.cleaned_data['update_existing']

                # Decode the CSV file
                try:
                    decoded_file = csv_file.read().decode('utf-8')
                    io_string = io.StringIO(decoded_file)
                    reader = csv.DictReader(io_string)

                    imported_count = 0
                    updated_count = 0
                    skipped_count = 0
                    errors = []

                    for row_num, row in enumerate(reader, start=2):
                        try:
                            # Create or update Location
                            location, created = Location.objects.get_or_create(
                                name=row['name'],
                                defaults={
                                    'address': row['address'],
                                    'city': row['city'],
                                    'state': row['state'],
                                    'zip_code': row['zip_code'],
                                    'country': row['country'],
                                    'location_type': row['location_type'],
                                    'created_by': request.user,
                                    'is_verified': True
                                }
                            )

                            if not created:
                                # Update existing location
                                location.address = row['address']
                                location.city = row['city']
                                location.state = row['state']
                                location.zip_code = row['zip_code']
                                location.country = row['country']
                                location.location_type = row['location_type']
                                location.save()

                            # Create or update HauntedPlace
                            try:
                                haunted_place = HauntedPlace.objects.get(location=location)

                                if update_existing:
                                    # Update existing
                                    haunted_place.story_title = row['story_title']
                                    haunted_place.story_content = row['story_content']
                                    haunted_place.historical_context = row['historical_context']
                                    haunted_place.scare_level = int(row['scare_level'])
                                    haunted_place.year_established = int(row['year_established']) if row['year_established'] else None
                                    haunted_place.reported_phenomena = row['reported_phenomena']
                                    haunted_place.famous_for = row['famous_for']
                                    haunted_place.view_count = int(row['view_count']) if row['view_count'] else 0
                                    haunted_place.visit_count = int(row['visit_count']) if row['visit_count'] else 0
                                    haunted_place.save()
                                    updated_count += 1
                                else:
                                    skipped_count += 1

                            except HauntedPlace.DoesNotExist:
                                # Create new
                                HauntedPlace.objects.create(
                                    location=location,
                                    story_title=row['story_title'],
                                    story_content=row['story_content'],
                                    historical_context=row['historical_context'],
                                    scare_level=int(row['scare_level']),
                                    year_established=int(row['year_established']) if row['year_established'] else None,
                                    reported_phenomena=row['reported_phenomena'],
                                    famous_for=row['famous_for'],
                                    created_by=request.user,
                                    view_count=int(row['view_count']) if row['view_count'] else 0,
                                    visit_count=int(row['visit_count']) if row['visit_count'] else 0,
                                )
                                imported_count += 1

                        except KeyError as e:
                            errors.append(f'Row {row_num}: Missing column {e}')
                        except Exception as e:
                            errors.append(f'Row {row_num}: {str(e)}')

                    # Display results
                    if imported_count > 0:
                        messages.success(request, f'Successfully imported {imported_count} haunted place(s).')
                    if updated_count > 0:
                        messages.success(request, f'Successfully updated {updated_count} haunted place(s).')
                    if skipped_count > 0:
                        messages.warning(request, f'Skipped {skipped_count} existing haunted place(s).')
                    if errors:
                        for error in errors[:10]:  # Show first 10 errors
                            messages.error(request, error)
                        if len(errors) > 10:
                            messages.error(request, f'... and {len(errors) - 10} more errors')

                    return redirect('..')

                except Exception as e:
                    messages.error(request, f'Error processing CSV file: {str(e)}')

        else:
            form = ImportHauntedPlacesForm()

        context = {
            'site_title': 'Import Haunted Places',
            'title': 'Import Haunted Places from CSV',
            'form': form,
            'opts': self.model._meta,
            'has_view_permission': self.has_view_permission(request),
        }

        return render(request, 'admin/core/hauntedplace/import_csv.html', context)

    def changelist_view(self, request, extra_context=None):
        """Add import button to changelist"""
        extra_context = extra_context or {}
        extra_context['import_csv_url'] = 'import-csv/'
        return super().changelist_view(request, extra_context=extra_context)


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
# CONTACT MESSAGE ADMIN
# ================================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['status_display', 'name', 'email', 'subject_preview', 'submitted_at', 'is_spam_display', 'user']
    list_filter = ['is_read', 'is_spam', 'is_responded', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message', 'ip_address']
    readonly_fields = ['submitted_at', 'ip_address', 'user_agent', 'honeypot', 'user']
    date_hierarchy = 'submitted_at'
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_spam', 'mark_as_not_spam', 'mark_as_responded']

    fieldsets = (
        ('Message Information', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_responded', 'is_spam', 'response_notes')
        }),
        ('Security Information', {
            'fields': ('ip_address', 'user_agent', 'honeypot', 'submitted_at'),
            'classes': ('collapse',),
            'description': 'Security tracking data for spam prevention'
        }),
        ('User Link', {
            'fields': ('user',),
            'classes': ('collapse',),
            'description': 'Linked user if submitted while logged in'
        }),
    )

    def status_display(self, obj):
        """Display read/unread status with color coding."""
        if obj.is_spam:
            return format_html('<span style="background-color: #DC2626; color: white; padding: 3px 8px; border-radius: 3px;">SPAM</span>')
        elif obj.is_responded:
            return format_html('<span style="background-color: #059669; color: white; padding: 3px 8px; border-radius: 3px;">✓ RESPONDED</span>')
        elif obj.is_read:
            return format_html('<span style="background-color: #3B82F6; color: white; padding: 3px 8px; border-radius: 3px;">READ</span>')
        else:
            return format_html('<span style="background-color: #F59E0B; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">● NEW</span>')
    status_display.short_description = 'Status'

    def subject_preview(self, obj):
        """Show truncated subject."""
        return obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
    subject_preview.short_description = 'Subject'

    def is_spam_display(self, obj):
        """Display spam flag with icon."""
        if obj.is_spam:
            return format_html('<span style="color: red;">🚫 Yes</span>')
        return format_html('<span style="color: green;">✓ No</span>')
    is_spam_display.short_description = 'Spam?'

    # Admin actions
    def mark_as_read(self, request, queryset):
        """Mark selected messages as read."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = 'Mark selected as read'

    def mark_as_unread(self, request, queryset):
        """Mark selected messages as unread."""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_as_unread.short_description = 'Mark selected as unread'

    def mark_as_spam(self, request, queryset):
        """Flag selected messages as spam."""
        updated = queryset.update(is_spam=True)
        self.message_user(request, f'{updated} message(s) flagged as spam.')
    mark_as_spam.short_description = 'Flag as spam'

    def mark_as_not_spam(self, request, queryset):
        """Unflag selected messages as spam."""
        updated = queryset.update(is_spam=False)
        self.message_user(request, f'{updated} message(s) unflagged as spam.')
    mark_as_not_spam.short_description = 'Unflag as spam'

    def mark_as_responded(self, request, queryset):
        """Mark selected messages as responded."""
        updated = queryset.update(is_responded=True, is_read=True)
        self.message_user(request, f'{updated} message(s) marked as responded.')
    mark_as_responded.short_description = 'Mark as responded'


# ================================================================
# CUSTOM ADMIN SITE CONFIGURATION
# ================================================================

# Customize admin site headers
admin.site.site_header = "🎃 ShriekedIn Admin Dashboard"
admin.site.site_title = "ShriekedIn Admin"
admin.site.index_title = "Halloween Platform Management"
