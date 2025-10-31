"""
Core Views for ShriekedIn Platform

This file contains all the main views for the core functionality:
- Home page
- Login/Logout
- Dashboard with technical statistics

For developers new to Django:
- Views are like controllers in other frameworks
- They receive HTTP requests and return HTTP responses
- They can render HTML templates or return data
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import connection
from django.conf import settings
import sys

# Import our models
from .models import Location, Event, HauntedPlace, Business


def home(request):
    """
    Home Page View

    This is the landing page that visitors see when they first arrive.
    It displays platform statistics and introduces the main features.

    Template: templates/home.html
    URL: / (root URL)
    """
    # Get real statistics from the database
    stats = {
        'total_users': User.objects.count(),
        'total_events': Event.objects.filter(is_active=True).count(),
        'total_locations': Location.objects.count(),
        'total_businesses': Business.objects.filter(is_active=True).count(),
    }

    return render(request, 'home.html', {
        'stats': stats
    })


def user_login(request):
    """
    Login View

    Handles both GET and POST requests:
    - GET: Display the login form
    - POST: Process login credentials and authenticate user

    Template: templates/login.html
    URL: /login/
    """
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    # Handle POST request (form submission)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login successful
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}! 👻')

            # Redirect to 'next' parameter or dashboard
            next_url = request.GET.get('next', 'core:dashboard')
            return redirect(next_url)
        else:
            # Login failed
            messages.error(request, 'Invalid username or password. Try again!')

    # Display login form (GET request or failed POST)
    return render(request, 'login.html', {
        'debug': settings.DEBUG  # Show demo credentials in development
    })


@login_required(login_url='core:login')
def user_logout(request):
    """
    Logout View

    Logs out the current user and redirects to home page.
    The @login_required decorator ensures only logged-in users can access this.

    URL: /logout/
    """
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye, {username}! See you next Halloween! 🎃')
    return redirect('core:home')


@login_required(login_url='core:login')
def dashboard(request):
    """
    Dashboard View

    Displays content management tools and platform statistics.
    Only accessible to logged-in users.

    Template: templates/dashboard.html
    URL: /dashboard/
    """

    # Gather content statistics
    from .models import Coupon

    stats = {
        'total_events': Event.objects.filter(is_active=True).count(),
        'total_haunted_places': HauntedPlace.objects.count(),
        'total_businesses': Business.objects.filter(is_active=True).count(),
        'total_coupons': Coupon.objects.filter(is_active=True).count(),
    }

    return render(request, 'dashboard.html', {
        'stats': stats
    })


def get_technical_stats():
    """
    Helper function to gather technical statistics

    This demonstrates how to query Django's internals and database
    to get useful system information.
    """

    # Get database size (PostgreSQL specific)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT pg_size_pretty(pg_database_size(current_database())) as size;
            """)
            db_size = cursor.fetchone()[0]
    except Exception:
        db_size = "N/A"

    # Get all database tables with row counts
    database_tables = []
    try:
        with connection.cursor() as cursor:
            # Get all tables in the current database
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()

            # Get row count for each table
            for table in tables:
                table_name = table[0]
                try:
                    cursor.execute(f'SELECT COUNT(*) FROM "{table_name}";')
                    count = cursor.fetchone()[0]
                    database_tables.append({
                        'name': table_name,
                        'count': count
                    })
                except Exception:
                    database_tables.append({
                        'name': table_name,
                        'count': 'N/A'
                    })
    except Exception:
        database_tables = [{'name': 'Error fetching tables', 'count': 'N/A'}]

    # Get installed apps (non-Django apps only)
    installed_apps = [
        app for app in settings.INSTALLED_APPS
        if not app.startswith('django.')
    ]

    return {
        # User Statistics
        'total_users': User.objects.count(),
        'active_sessions': Session.objects.count(),

        # System Information
        'django_version': settings.DJANGO_VERSION_STRING if hasattr(settings, 'DJANGO_VERSION_STRING') else 'Django 5.2.7',
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'database_engine': settings.DATABASES['default']['ENGINE'].split('.')[-1],
        'debug_mode': settings.DEBUG,
        'allowed_hosts': ', '.join(settings.ALLOWED_HOSTS) if settings.ALLOWED_HOSTS else 'None',

        # Database Information
        'db_size_mb': db_size,
        'database_tables': database_tables[:10],  # Limit to first 10 tables

        # Applications
        'installed_apps': installed_apps,

        # Server Status
        'server_status': 'Running',
    }


def haunted_places(request):
    """
    Haunted Places Listing View

    This view displays a list of haunted locations with ghost stories and legends.
    Pulls data from the HauntedPlace model in the database.

    For junior developers:
    ----------------------
    This is a simple view that renders a template with context data.

    Context data is a dictionary that gets passed to the template.
    In the template, you can access these variables using {{ variable_name }}

    Example:
        context = {'name': 'Ghost House'}
        In template: {{ name }} displays "Ghost House"

    Template: templates/haunted_places.html
    URL: /haunted/
    """

    # Get all haunted places from the database, ordered by view count (most popular first)
    haunted_places_list = HauntedPlace.objects.select_related('location').order_by('-view_count', 'story_title')

    # Context dictionary - data passed to the template
    context = {
        'haunted_places': haunted_places_list,
    }

    # Render the template with the context
    return render(request, 'haunted_places.html', context)


def haunted_detail(request, place_id):
    """
    Haunted Place Detail View

    This view displays detailed information about a specific haunted place.
    Pulls data from the HauntedPlace model in the database.

    For junior developers:
    ----------------------
    This view receives a parameter (place_id) from the URL.

    URL pattern:  /haunted/<int:place_id>/
    Example URL:  /haunted/42/
    Result:       haunted_detail(request, place_id=42)

    The place_id is captured from the URL and passed as a function parameter.

    Template: templates/haunted_detail.html
    URL: /haunted/<int:place_id>/
    """

    # Get the haunted place from database (or return 404 if not found)
    place = get_object_or_404(HauntedPlace.objects.select_related('location', 'created_by'), id=place_id)

    # Increment view count
    place.view_count += 1
    place.save(update_fields=['view_count'])

    context = {
        'place': place,
    }

    return render(request, 'haunted_detail.html', context)


def events_list(request):
    """
    Events Listing View

    Displays all active Halloween events with filtering options.
    Supports search query parameter.

    Template: templates/events_list.html
    URL: /events/
    """
    from django.db.models import Q

    # Start with all active events
    events = Event.objects.filter(is_active=True).select_related('location', 'created_by')

    # Handle search query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Search across multiple fields
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__city__icontains=search_query) |
            Q(location__state__icontains=search_query) |
            Q(location__name__icontains=search_query)
        )

    # Order by date
    events = events.order_by('event_date')

    # Count featured events
    featured_count = events.filter(is_featured=True).count()

    context = {
        'events': events,
        'featured_count': featured_count,
        'search_query': search_query,
    }

    return render(request, 'events_list.html', context)


def event_detail(request, event_id):
    """
    Event Detail View

    Displays detailed information about a specific event.

    Template: templates/event_detail.html
    URL: /events/<int:event_id>/
    """
    # Get the event from database (or return 404 if not found)
    event = get_object_or_404(Event.objects.select_related('location', 'created_by'), id=event_id, is_active=True)

    # Increment view count
    event.view_count += 1
    event.save(update_fields=['view_count'])

    context = {
        'event': event,
    }

    return render(request, 'event_detail.html', context)


def businesses_list(request):
    """
    Businesses Listing View

    Displays all active Halloween businesses with filtering options.
    Supports search query parameter.

    Template: templates/businesses_list.html
    URL: /businesses/
    """
    from django.db.models import Q

    # Start with all active businesses
    businesses = Business.objects.filter(is_active=True).select_related('location', 'user').prefetch_related('coupons')

    # Handle search query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Search across multiple fields
        businesses = businesses.filter(
            Q(business_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__city__icontains=search_query) |
            Q(location__state__icontains=search_query) |
            Q(business_type__icontains=search_query)
        )

    # Order by name
    businesses = businesses.order_by('business_name')

    # Count verified businesses
    verified_count = businesses.filter(verified=True).count()

    context = {
        'businesses': businesses,
        'verified_count': verified_count,
        'search_query': search_query,
    }

    return render(request, 'businesses_list.html', context)


def business_detail(request, slug):
    """
    Business Detail View

    Displays detailed information about a specific business.

    Template: templates/business_detail.html
    URL: /businesses/<slug:slug>/
    """
    # Get the business from database (or return 404 if not found)
    business = get_object_or_404(
        Business.objects.select_related('location', 'user').prefetch_related('coupons'),
        slug=slug,
        is_active=True
    )

    context = {
        'business': business,
    }

    return render(request, 'business_detail.html', context)


def terms(request):
    """
    Terms and Conditions Page

    Displays the platform's terms and conditions with spooky theming
    but legally compliant content.

    Template: templates/terms.html
    URL: /terms/
    """
    return render(request, 'terms.html')


def privacy(request):
    """
    Privacy Policy Page

    Displays the platform's privacy policy, fully compliant with GDPR
    and UK Data Protection laws, with Halloween-themed presentation.

    Template: templates/privacy.html
    URL: /privacy/
    """
    return render(request, 'privacy.html')


def cookie_settings(request):
    """
    Cookie Settings Page

    Allows users to manage their cookie preferences and consent choices.
    Users can accept or decline different categories of cookies.

    Template: templates/cookie_settings.html
    URL: /cookie-settings/
    """
    return render(request, 'cookie_settings.html')


# Custom 404 error handler
def custom_404(request, exception=None):
    """
    Custom 404 Error Page

    This view is called when a page is not found.
    Configure it in your main urls.py with: handler404 = 'core.views.custom_404'

    Template: templates/404.html
    """
    return render(request, '404.html', status=404)
