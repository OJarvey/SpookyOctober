"""
Core Models for ShriekedIn Platform

This file contains all the main database models for the Halloween
networking and events platform.

Models:
- UserProfile: Extended user profile with Halloween-themed fields
- Location: Geographic locations for events and places
- Event: Halloween events and gatherings
- Media: Images and files attached to various entities
- HauntedPlace: Haunted locations with stories
- Business: Halloween-themed businesses
- Coupon: Business promotional offers
- Post: User-generated content
- Like: Likes on content
- Comment: Comments on content
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import uuid


# ================================================================
# USER PROFILE (Sprint 1)
# ================================================================

class UserProfile(models.Model):
    """
    Extended user profile with additional Halloween-themed fields.

    Extends the built-in Django User model with custom fields for
    our platform's specific needs.
    """

    USER_TYPE_CHOICES = [
        ('visitor', 'Visitor'),
        ('business_owner', 'Business Owner'),
        ('city_official', 'City Official'),
        ('event_organizer', 'Event Organizer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='visitor')
    bio = models.TextField(blank=True, help_text="Tell us about yourself and your Halloween interests!")
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    favorite_halloween_activity = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True, help_text="Your city or region")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.user_type})"

    def get_absolute_url(self):
        return reverse('core:profile', kwargs={'username': self.user.username})


# ================================================================
# LOCATION (Sprint 2)
# ================================================================

class Location(models.Model):
    """
    Geographic locations for events, haunted places, and businesses.

    Stores address, coordinates, and metadata for all location-based content.
    """

    LOCATION_TYPE_CHOICES = [
        ('venue', 'Event Venue'),
        ('haunted', 'Haunted Place'),
        ('business', 'Business'),
        ('neighborhood', 'Neighborhood'),
        ('landmark', 'Landmark'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200, help_text="Location name (e.g., 'Central Park')")
    address = models.TextField(help_text="Full street address")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default="USA")

    # Geographic coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES, default='venue')
    description = models.TextField(blank=True)

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='locations_created')
    created_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False, help_text="Verified by administrators")

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['name']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['city', 'state']),
        ]

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"

    def get_absolute_url(self):
        return reverse('core:location_detail', kwargs={'pk': self.pk})


# ================================================================
# EVENT (Sprint 3)
# ================================================================

class Event(models.Model):
    """
    Halloween events and gatherings.

    Users can create, discover, and manage Halloween-themed events.
    """

    EVENT_CATEGORY_CHOICES = [
        ('haunted_house', 'Haunted House'),
        ('costume_party', 'Costume Party'),
        ('trick_or_treat', 'Trick or Treat'),
        ('ghost_tour', 'Ghost Tour'),
        ('pumpkin_carving', 'Pumpkin Carving'),
        ('halloween_market', 'Halloween Market'),
        ('film_screening', 'Film Screening'),
        ('parade', 'Halloween Parade'),
        ('other', 'Other'),
    ]

    AGE_CHOICES = [
        ('all_ages', 'All Ages'),
        ('family_friendly', 'Family Friendly'),
        ('kids_only', 'Kids Only (under 12)'),
        ('teens', 'Teens (13-17)'),
        ('adults', 'Adults Only (18+)'),
    ]

    # Basic info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(help_text="Detailed event description")

    # Location and timing
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='events')
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)

    # Event details
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, help_text="Entry fee (0 = free)")
    age_appropriateness = models.CharField(max_length=20, choices=AGE_CHOICES, default='all_ages')
    event_category = models.CharField(max_length=20, choices=EVENT_CATEGORY_CHOICES)

    # Additional info
    performing_artists = models.CharField(max_length=500, blank=True, help_text="Comma-separated artists/performers")
    contact_info = models.EmailField(blank=True, help_text="Contact email for questions")
    website_url = models.URLField(blank=True)
    capacity = models.IntegerField(null=True, blank=True, help_text="Maximum attendees")

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Featured on homepage")

    # Engagement metrics
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-event_date', '-start_time']
        indexes = [
            models.Index(fields=['event_date']),
            models.Index(fields=['event_category']),
            models.Index(fields=['is_active']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Event.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} on {self.event_date}"

    def get_absolute_url(self):
        return reverse('core:event_detail', kwargs={'slug': self.slug})

    @property
    def is_free(self):
        return self.cost == 0


# ================================================================
# MEDIA (Sprint 3)
# ================================================================

class Media(models.Model):
    """
    Images and files attached to various entities (events, places, etc.).

    Generic media model that can be attached to any content type.
    """

    ENTITY_TYPE_CHOICES = [
        ('event', 'Event'),
        ('haunted_place', 'Haunted Place'),
        ('business', 'Business'),
        ('post', 'Post'),
        ('user_profile', 'User Profile'),
    ]

    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]

    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    entity_id = models.IntegerField(help_text="ID of the related entity")

    file = models.FileField(upload_to='media/%Y/%m/%d/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='image')
    caption = models.CharField(max_length=500, blank=True)
    alt_text = models.CharField(max_length=200, blank=True, help_text="Accessibility text")

    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_uploads')
    upload_date = models.DateTimeField(auto_now_add=True)

    # Order for galleries
    order = models.IntegerField(default=0, help_text="Display order in gallery")

    class Meta:
        verbose_name = "Media File"
        verbose_name_plural = "Media Files"
        ordering = ['entity_type', 'entity_id', 'order']
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
        ]

    def __str__(self):
        return f"{self.file_type} for {self.entity_type} #{self.entity_id}"


# ================================================================
# HAUNTED PLACE (Sprint 4)
# ================================================================

class HauntedPlace(models.Model):
    """
    Haunted locations with stories and legends.

    Database of spooky places with historical context and scary stories.
    """

    SCARE_LEVEL_CHOICES = [
        (1, '1 - Not Scary (Family Friendly)'),
        (2, '2 - Mildly Spooky'),
        (3, '3 - Moderately Scary'),
        (4, '4 - Very Scary'),
        (5, '5 - Terrifying (Adults Only)'),
    ]

    # Location
    location = models.OneToOneField(Location, on_delete=models.CASCADE, related_name='haunted_place')

    # Story content
    story_title = models.CharField(max_length=200, help_text="Title of the ghost story/legend")
    story_content = models.TextField(help_text="The spooky story or legend")
    historical_context = models.TextField(blank=True, help_text="Factual historical information")

    # Metadata
    scare_level = models.IntegerField(choices=SCARE_LEVEL_CHOICES, default=3)
    is_educational = models.BooleanField(default=False, help_text="Suitable for educational purposes")
    year_established = models.IntegerField(null=True, blank=True, help_text="Year location was built/established")

    # Paranormal details
    reported_phenomena = models.TextField(blank=True, help_text="Types of paranormal activity reported")
    famous_for = models.CharField(max_length=500, blank=True, help_text="What makes this place notable")

    # User content
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='haunted_places_created')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Engagement
    view_count = models.IntegerField(default=0)
    visit_count = models.IntegerField(default=0, help_text="People who've visited this location")

    class Meta:
        verbose_name = "Haunted Place"
        verbose_name_plural = "Haunted Places"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.story_title} ({self.location.name})"

    def get_absolute_url(self):
        return reverse('core:haunted_detail', kwargs={'place_id': self.pk})


# ================================================================
# BUSINESS (Sprint 5)
# ================================================================

class Business(models.Model):
    """
    Halloween-themed businesses and vendors.

    Business profiles for costume shops, event organizers, etc.
    """

    BUSINESS_TYPE_CHOICES = [
        ('costume_shop', 'Costume Shop'),
        ('party_supplies', 'Party Supplies'),
        ('event_venue', 'Event Venue'),
        ('haunted_attraction', 'Haunted Attraction'),
        ('decorator', 'Decorator'),
        ('photographer', 'Photographer'),
        ('food_vendor', 'Food Vendor'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]

    # Owner and basic info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    business_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='businesses')

    # Business details
    business_type = models.CharField(max_length=30, choices=BUSINESS_TYPE_CHOICES)
    description = models.TextField(blank=True)

    # Contact information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # Social media
    facebook_url = models.URLField(blank=True)
    instagram_handle = models.CharField(max_length=100, blank=True)

    # Business hours (simplified - could be expanded)
    hours_of_operation = models.TextField(blank=True, help_text="Business hours description")

    # Verification
    verified = models.BooleanField(default=False, help_text="Verified by administrators")
    verified_date = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"
        ordering = ['business_name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.business_name)
            original_slug = self.slug
            counter = 1
            while Business.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.business_name

    def get_absolute_url(self):
        return reverse('core:business_detail', kwargs={'slug': self.slug})


# ================================================================
# COUPON (Sprint 5)
# ================================================================

class Coupon(models.Model):
    """
    Promotional coupons and discounts from businesses.

    Businesses can create coupons for special offers.
    """

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='coupons')

    # Coupon details
    title = models.CharField(max_length=200, help_text="e.g., '20% off costume rentals'")
    description = models.TextField()
    discount_code = models.CharField(max_length=50, unique=True, help_text="Unique code to use at checkout")

    # Discount amount
    discount_percentage = models.IntegerField(null=True, blank=True, help_text="Percentage off (0-100)")
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Fixed dollar amount off")

    # Validity
    valid_from = models.DateField()
    valid_until = models.DateField()
    terms_and_conditions = models.TextField(blank=True, help_text="Fine print and restrictions")

    # Usage limits
    max_uses = models.IntegerField(null=True, blank=True, help_text="Leave blank for unlimited")
    current_uses = models.IntegerField(default=0)

    # Status
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        ordering = ['-valid_until']
        indexes = [
            models.Index(fields=['discount_code']),
            models.Index(fields=['valid_from', 'valid_until']),
        ]

    def __str__(self):
        return f"{self.title} - {self.business.business_name}"

    @property
    def is_valid(self):
        from django.utils import timezone
        today = timezone.now().date()
        return (self.is_active and
                self.valid_from <= today <= self.valid_until and
                (self.max_uses is None or self.current_uses < self.max_uses))


# ================================================================
# POST (Sprint 6)
# ================================================================

class Post(models.Model):
    """
    User-generated posts for the community feed.

    Status updates, photos, and content shared by users.
    """

    POST_TYPE_CHOICES = [
        ('status', 'Status Update'),
        ('photo', 'Photo Post'),
        ('event_share', 'Event Share'),
        ('place_share', 'Place Share'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(help_text="Post content/caption")
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='status')

    # Optional reference to other content
    reference_type = models.CharField(max_length=20, blank=True, help_text="Type of referenced content")
    reference_id = models.IntegerField(null=True, blank=True, help_text="ID of referenced content")

    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Engagement metrics
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)

    # Visibility
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['-created_date']),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

    def get_absolute_url(self):
        return reverse('core:post_detail', kwargs={'pk': self.pk})


# ================================================================
# LIKE (Sprint 6)
# ================================================================

class Like(models.Model):
    """
    Likes on content (events, posts, etc.).

    Tracks user engagement with content.
    """

    ENTITY_TYPE_CHOICES = [
        ('event', 'Event'),
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('haunted_place', 'Haunted Place'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    entity_id = models.IntegerField()

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = [['user', 'entity_type', 'entity_id']]  # One like per user per entity
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.entity_type} #{self.entity_id}"


# ================================================================
# COMMENT (Sprint 6)
# ================================================================

class Comment(models.Model):
    """
    Comments on content (events, posts, etc.).

    Supports threaded discussions.
    """

    ENTITY_TYPE_CHOICES = [
        ('event', 'Event'),
        ('post', 'Post'),
        ('haunted_place', 'Haunted Place'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    entity_id = models.IntegerField()

    # Threading support
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    content = models.TextField(help_text="Comment text")

    # Timestamps
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    # Moderation
    is_active = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)

    # Engagement
    like_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['created_date']
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['parent_comment']),
        ]

    def __str__(self):
        return f"{self.user.username} on {self.entity_type} #{self.entity_id}: {self.content[:30]}"

    @property
    def is_reply(self):
        return self.parent_comment is not None
