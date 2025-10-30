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


# Custom 404 error handler
def custom_404(request, exception=None):
    """
    Custom 404 Error Page

    This view is called when a page is not found.
    Configure it in your main urls.py with: handler404 = 'core.views.custom_404'

    Template: templates/404.html
    """
    return render(request, '404.html', status=404)
