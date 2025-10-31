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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import connection
from django.conf import settings
import sys


def home(request):
    """
    Home Page View

    This is the landing page that visitors see when they first arrive.
    It displays platform statistics and introduces the main features.

    Template: templates/home.html
    URL: / (root URL)
    """
    # Get some basic statistics for the home page
    stats = {
        'total_users': User.objects.count(),
        'total_events': 0,  # Will be implemented in Sprint 3
        'total_locations': 0,  # Will be implemented in Sprint 2
        'total_businesses': 0,  # Will be implemented in Sprint 5
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

    Displays technical statistics and system information.
    This is a demonstration of how to gather and display system metrics.
    Only accessible to logged-in users.

    Template: templates/dashboard.html
    URL: /dashboard/
    """

    # Gather technical statistics
    tech_stats = get_technical_stats()

    return render(request, 'dashboard.html', {
        'tech_stats': tech_stats
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
    Currently shows sample data - in Sprint 4, this will pull from the database.

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

    # Sample data for demonstration
    # TODO: In Sprint 4, replace this with: HauntedPlace.objects.all()
    sample_haunted_places = [
        {
            'id': 1,
            'name': 'The Winchester Mystery House',
            'location': 'San Jose, California',
            'description': 'A sprawling mansion with staircases to nowhere, doors that open to walls, and countless architectural oddities. Built by Sarah Winchester who believed she was haunted by the spirits of those killed by Winchester rifles.',
            'place_type': 'Historic Mansion',
            'scary_rating': 4,
            'image': None,
        },
        {
            'id': 2,
            'name': 'Eastern State Penitentiary',
            'location': 'Philadelphia, Pennsylvania',
            'description': 'Once the most famous and expensive prison in the world, this Gothic fortress now stands in ruins. Visitors report shadow figures, cackling laughter, and ghostly faces appearing in cell doorways.',
            'place_type': 'Historic Prison',
            'scary_rating': 5,
            'image': None,
        },
        {
            'id': 3,
            'name': 'The Stanley Hotel',
            'location': 'Estes Park, Colorado',
            'description': 'The hotel that inspired Stephen King to write "The Shining." Guests report hearing children playing in empty hallways, piano music from the music room, and ghost sightings throughout the building.',
            'place_type': 'Historic Hotel',
            'scary_rating': 3,
            'image': None,
        },
        {
            'id': 4,
            'name': 'Bachelor\'s Grove Cemetery',
            'location': 'Midlothian, Illinois',
            'description': 'One of the most haunted cemeteries in America. Paranormal investigators have documented over 100 different phenomena including ghost lights, apparitions, and mysterious glowing orbs.',
            'place_type': 'Cemetery',
            'scary_rating': 5,
            'image': None,
        },
        {
            'id': 5,
            'name': 'The Myrtles Plantation',
            'location': 'St. Francisville, Louisiana',
            'description': 'Built in 1796, this plantation is reportedly home to at least 12 ghosts. The most famous is Chloe, a former slave whose spirit is said to roam the grounds. Visitors report handprints on mirrors and furniture that moves on its own.',
            'place_type': 'Historic Plantation',
            'scary_rating': 4,
            'image': None,
        },
        {
            'id': 6,
            'name': 'Waverly Hills Sanatorium',
            'location': 'Louisville, Kentucky',
            'description': 'A former tuberculosis hospital where thousands died. The building features a "body chute" used to remove corpses. Paranormal activity is rampant, with reports of shadow people, full-bodied apparitions, and disembodied voices.',
            'place_type': 'Abandoned Hospital',
            'scary_rating': 5,
            'image': None,
        },
    ]

    # Context dictionary - data passed to the template
    context = {
        'haunted_places': sample_haunted_places,
    }

    # Render the template with the context
    return render(request, 'haunted_places.html', context)


def haunted_detail(request, place_id):
    """
    Haunted Place Detail View

    This view displays detailed information about a specific haunted place.
    Currently shows sample data - in Sprint 4, this will pull from the database.

    For junior developers:
    ----------------------
    This view receives a parameter (place_id) from the URL.

    URL pattern:  /haunted/<int:place_id>/
    Example URL:  /haunted/42/
    Result:       haunted_detail(request, place_id=42)

    The place_id is captured from the URL and passed as a function parameter.

    Template: templates/haunted_detail.html (to be created)
    URL: /haunted/<int:place_id>/
    """

    # Sample data lookup (simulating database query)
    # TODO: In Sprint 4, replace with: HauntedPlace.objects.get(id=place_id)
    sample_places = {
        1: {
            'id': 1,
            'name': 'The Winchester Mystery House',
            'location': 'San Jose, California',
            'full_description': '''
                The Winchester Mystery House is a sprawling 160-room Victorian mansion that defies all
                architectural logic. Built by Sarah Winchester, widow of gun magnate William Wirt Winchester,
                construction continued 24 hours a day for 38 years.

                Sarah believed she was haunted by the ghosts of those killed by Winchester rifles. A medium
                told her that continuous construction would appease the spirits. The result is a bizarre
                maze of staircases leading to ceilings, doors opening to walls, and windows overlooking
                other rooms.

                Reported paranormal activity includes:
                - Footsteps in empty hallways
                - Doorknobs turning on their own
                - Mysterious whispers and cold spots
                - Apparitions of Sarah Winchester herself
                - The ghostly sounds of construction continuing at night

                The house spans 6 acres with 10,000 windows, 2,000 doors, 47 stairways and fireplaces,
                and 17 chimneys. Some staircases have steps only 2 inches high. Secret passages and
                hidden rooms are found throughout.
            ''',
            'place_type': 'Historic Mansion',
            'scary_rating': 4,
            'image': None,
            'year_built': 1884,
            'visits_count': 1337,
        }
    }

    # Get the place (or return 404 if not found)
    place = sample_places.get(place_id)

    if place is None:
        # If place doesn't exist, show 404 error
        return render(request, '404.html', status=404)

    context = {
        'place': place,
    }

    return render(request, 'haunted_detail.html', context)


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
