"""
Core URL Configuration for SpookyOctober

This file defines all the URL patterns (routes) for the core app.

For developers new to Django:
---------------------------------
URLs in Django work like a map - they connect web addresses (URLs) to view functions.

Basic structure:
    path('url-pattern/', view_function, name='url-name')

Where:
    - 'url-pattern/' = The URL users will visit (e.g., /login/)
    - view_function = The Python function that handles this URL (defined in views.py)
    - name='url-name' = A name you can use to reference this URL in templates

Example:
    path('login/', views.user_login, name='login')

    This means:
    - When someone visits /login/, Django calls the user_login() function
    - In templates, you can use {% url 'core:login' %} to get this URL
"""

from django.urls import path
from . import views

# App name for namespacing URLs
# This allows us to use 'core:home', 'core:login', etc. in templates
# Namespacing prevents conflicts if multiple apps have URLs with the same name
app_name = 'core'

urlpatterns = [
    #################################################################
    # HOME PAGE
    #################################################################
    # URL: /
    # View: views.home
    # Template: templates/home.html
    # Purpose: Landing page showing platform overview and statistics
    path('', views.home, name='home'),

    #################################################################
    # AUTHENTICATION URLS
    #################################################################

    # LOGIN
    # URL: /login/
    # View: views.user_login
    # Template: templates/login.html
    # Purpose: Display login form and process user authentication
    # Handles both GET (show form) and POST (process login)
    path('login/', views.user_login, name='login'),

    # LOGOUT
    # URL: /logout/
    # View: views.user_logout
    # Purpose: Log out the current user and redirect to home
    # Requires user to be logged in (@login_required decorator)
    path('logout/', views.user_logout, name='logout'),

    #################################################################
    # USER DASHBOARD
    #################################################################
    # URL: /dashboard/
    # View: views.dashboard
    # Template: templates/dashboard.html
    # Purpose: Show technical statistics and user information
    # Requires login - will redirect to login page if not authenticated
    path('dashboard/', views.dashboard, name='dashboard'),

    #################################################################
    # LEGAL PAGES
    #################################################################
    # URL: /terms/
    # View: views.terms
    # Template: templates/terms.html
    # Purpose: Display Terms and Conditions (spooky but legally binding)
    path('terms/', views.terms, name='terms'),

    # URL: /privacy/
    # View: views.privacy
    # Template: templates/privacy.html
    # Purpose: Display Privacy Policy (GDPR compliant with Halloween theme)
    path('privacy/', views.privacy, name='privacy'),

    # COOKIE SETTINGS
    # URL: /cookie-settings/
    # View: views.cookie_settings
    # Template: templates/cookie_settings.html
    # Purpose: Allow users to manage cookie preferences
    path('cookie-settings/', views.cookie_settings, name='cookie_settings'),

    #################################################################
    # INFORMATIONAL PAGES
    #################################################################
    # URL: /about/
    # View: views.about
    # Template: templates/about.html
    # Purpose: Display information about ShriekedIn platform and team
    path('about/', views.about, name='about'),

    # URL: /contact/
    # View: views.contact
    # Template: templates/contact.html
    # Purpose: Display contact form with security protections and handle submissions
    path('contact/', views.contact, name='contact'),

    #################################################################
    # HAUNTED PLACES
    #################################################################
    # URL: /haunted/
    # View: views.haunted_places
    # Template: templates/haunted_places.html
    # Purpose: Display a list of all haunted locations with ghost stories
    #
    # For junior developers:
    # This is a simple URL pattern that maps /haunted/ to a view function
    # The name='haunted_places' allows you to reference this URL in templates:
    # Example: <a href="{% url 'core:haunted_places' %}">Haunted Places</a>
    path('haunted/', views.haunted_places, name='haunted_places'),

    # HAUNTED PLACE DETAIL
    # URL: /haunted/<int:place_id>/
    # View: views.haunted_detail
    # Template: templates/haunted_detail.html (to be created)
    # Purpose: Display detailed information about a specific haunted place
    #
    # For junior developers:
    # This URL pattern captures an integer from the URL as 'place_id'
    #
    # How it works:
    #   - User visits: /haunted/42/
    #   - Django captures: place_id = 42
    #   - Django calls: views.haunted_detail(request, place_id=42)
    #   - View can use place_id to look up the specific haunted place
    #
    # The <int:place_id> syntax means:
    #   - <...> = capture this part of the URL
    #   - int: = convert to an integer (rejects non-numeric values)
    #   - place_id = the parameter name passed to the view
    #
    # Example template usage:
    #   <a href="{% url 'core:haunted_detail' place.id %}">View Details</a>
    path('haunted/<int:place_id>/', views.haunted_detail, name='haunted_detail'),

    #################################################################
    # EVENTS
    #################################################################
    # URL: /events/
    # View: views.events_list
    # Template: templates/events_list.html
    # Purpose: Display a list of all active Halloween events
    path('events/', views.events_list, name='events_list'),

    # EVENT DETAIL
    # URL: /events/<int:event_id>/
    # View: views.event_detail
    # Template: templates/event_detail.html
    # Purpose: Display detailed information about a specific event
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),

    #################################################################
    # BUSINESSES
    #################################################################
    # URL: /businesses/
    # View: views.businesses_list
    # Template: templates/businesses_list.html
    # Purpose: Display a list of all active Halloween businesses
    path('businesses/', views.businesses_list, name='businesses_list'),

    # BUSINESS DETAIL
    # URL: /businesses/<slug:slug>/
    # View: views.business_detail
    # Template: templates/business_detail.html
    # Purpose: Display detailed information about a specific business
    path('businesses/<slug:slug>/', views.business_detail, name='business_detail'),

    #################################################################
    # FUTURE URLs (Coming in later sprints)
    #################################################################
    # These will be added as we develop more features:

    # Sprint 2 (Location & Map):
    # path('map/', views.map_view, name='map'),
    # path('locations/', views.location_list, name='location_list'),
    # path('locations/<int:location_id>/', views.location_detail, name='location_detail'),

    # Sprint 3 (Events):
    # path('events/', views.event_list, name='event_list'),
    # path('events/create/', views.event_create, name='event_create'),
    # path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    # path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),

    # Sprint 5 (Business & Coupons):
    # path('businesses/', views.business_list, name='business_list'),
    # path('coupons/', views.coupon_list, name='coupon_list'),

    # Sprint 6 (Social Features):
    # path('feed/', views.feed, name='feed'),
    # path('profile/<int:user_id>/', views.profile, name='profile'),
]

"""
HOW TO ADD NEW URLs:
--------------------
1. Create a new view function in views.py
2. Import it if needed (or use views.function_name)
3. Add a new path() to this urlpatterns list
4. Give it a descriptive name parameter
5. Create the corresponding template in templates/

Example of adding a new "about" page:

In views.py:
    def about(request):
        return render(request, 'about.html')

In this file:
    path('about/', views.about, name='about'),

In templates:
    Create templates/about.html

In other templates, link to it:
    <a href="{% url 'core:about' %}">About Us</a>

URL PATTERNS WITH PARAMETERS:
-----------------------------
You can capture parts of the URL as parameters:

    path('event/<int:event_id>/', views.event_detail, name='event_detail')

    - <int:event_id> captures an integer from the URL
    - It gets passed to the view as: event_detail(request, event_id)
    - Example URL: /event/123/ would pass event_id=123 to the view

Common pattern types:
    - <int:name> = captures an integer
    - <str:name> = captures a string (default)
    - <slug:name> = captures a slug (letters, numbers, hyphens, underscores)
    - <uuid:name> = captures a UUID

"""
