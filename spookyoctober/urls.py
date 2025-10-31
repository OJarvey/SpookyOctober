"""
Main URL Configuration for SpookyOctober Project

This is the ROOT URL configuration file. All URL patterns start here.

For developers new to Django:
---------------------------------
This file is like the "main entrance" to your application's URLs.
It includes URL patterns from different apps and directs traffic accordingly.

Structure:
    path('prefix/', include('app_name.urls'))

    This includes all URLs from that app and adds a prefix.
    For example: path('blog/', include('blog.urls')) means all blog URLs
    will start with /blog/ (e.g., /blog/post/1/)

In our case, we're using:
    path('', include('core.urls')) - This means core app URLs have no prefix
    So core URLs like /login/ are directly accessible at /login/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #################################################################
    # DJANGO ADMIN
    #################################################################
    # URL: /admin/
    # Purpose: Django's built-in admin interface
    # Access: Only for superusers (created with: python manage.py createsuperuser)
    # This is where you can manage users, view database records, etc.
    path("admin/", admin.site.urls),

    #################################################################
    # CORE APP URLs
    #################################################################
    # Include all URLs from the core app (see core/urls.py)
    # These URLs have no prefix, so they're accessible at the root
    # Example: core's '/login/' URL is accessible at /login/
    path("", include("core.urls")),

    #################################################################
    # COOKIE CONSENT (GDPR Compliance)
    #################################################################
    # URLs for cookie consent management
    # Provides: /cookies/accept/, /cookies/decline/, etc.
    path("cookies/", include("cookie_consent.urls")),

    #################################################################
    # GAMES APP (Mad Libs and Halloween Games)
    #################################################################
    # Halloween-themed educational games
    # Provides: /games/, /games/madlibs/, etc.
    path("games/", include("games.urls")),

    #################################################################
    # FUTURE APP URLs (to be added in later sprints)
    #################################################################
    # As we build more features, we'll add more apps here:

    # Sprint 3 - Events app:
    # path('events/', include('events.urls')),

    # Sprint 4 - Haunted places app:
    # path('haunted/', include('haunted.urls')),

    # Sprint 5 - Business app:
    # path('business/', include('business.urls')),
]

#################################################################
# STATIC AND MEDIA FILES (Development only)
#################################################################
# In development, Django serves static files (CSS, JS) and media files (uploads)
# In production (Heroku), WhiteNoise handles static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Media files will be added when we implement image uploads:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Auto-reload browser on file changes (development only)
    urlpatterns = [
        path("__reload__/", include("django_browser_reload.urls")),
    ] + urlpatterns

#################################################################
# CUSTOM ERROR HANDLERS
#################################################################
# These handle HTTP error pages (404, 500, etc.)
# Uncomment to use custom error pages:

# 404 - Page Not Found
handler404 = 'core.views.custom_404'

# You can also add handlers for other errors:
# handler500 = 'core.views.custom_500'  # Server Error
# handler403 = 'core.views.custom_403'  # Forbidden
# handler400 = 'core.views.custom_400'  # Bad Request

"""
HOW URL ROUTING WORKS:
----------------------
1. User visits a URL (e.g., https://spookyoctober.com/login/)
2. Django strips the domain, leaving /login/
3. Django checks urlpatterns in THIS FILE from top to bottom
4. Django finds: path("", include("core.urls"))
5. Django then looks in core/urls.py for a match
6. Finds: path('login/', views.user_login, name='login')
7. Django calls: views.user_login(request)
8. The view returns a response (HTML, redirect, JSON, etc.)
9. Django sends the response back to the user's browser

URL NAMESPACING:
----------------
We use app_name = 'core' in core/urls.py
This creates a namespace, so we reference URLs as 'core:login'

In templates: {% url 'core:login' %}
In views: redirect('core:login')
In Python: reverse('core:login')

This prevents conflicts if multiple apps have a 'login' URL.
"""
