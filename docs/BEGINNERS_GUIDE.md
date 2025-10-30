# Beginner's Guide to Django - ShriekedIn Edition

## Welcome! 👋

This guide is for developers who are new to Django, especially those coming from static HTML/CSS/JS backgrounds.

---

## 📁 Project Structure Explained

```
ShriekedIn/
├── manage.py              # Command-line utility (like package.json scripts)
├── .env                   # Environment variables (SECRET_KEY, DEBUG, etc.)
├── requirements.txt       # Python dependencies (like package.json)
├── package.json          # Node dependencies (for Tailwind CSS)
│
├── spookyoctober/        # PROJECT settings folder
│   ├── settings.py       # Main configuration file
│   ├── urls.py          # ROOT URL routing (main entry point)
│   ├── wsgi.py          # Production server configuration
│   └── asgi.py          # Async server configuration
│
├── core/                 # CORE APP (your main application code)
│   ├── views.py         # Functions that handle requests (like controllers)
│   ├── urls.py          # URL routing for this app
│   ├── models.py        # Database models (tables)
│   ├── admin.py         # Django admin configuration
│   ├── apps.py          # App configuration
│   └── tests.py         # Unit tests
│
├── templates/            # HTML templates (your views)
│   ├── base.html        # Base template (layout)
│   ├── home.html        # Home page
│   ├── login.html       # Login page
│   ├── dashboard.html   # Dashboard page
│   └── 404.html         # Custom 404 error page
│
├── static/               # Static files (CSS, JS, images)
│   └── css/
│       ├── tailwind-input.css   # Source CSS
│       └── tailwind-output.css  # Compiled CSS (use this)
│
└── staticfiles/          # Collected static files for production (auto-generated)
```

---

## 🎯 How Django Works (Coming from Static HTML)

### Static HTML Site:
```
Browser → Web Server → HTML File → Browser
```

### Django Site:
```
Browser → Django → View Function → Template (HTML) → Browser
                       ↓
                   Database Query
```

---

## 🛣️ Request Flow

Let's trace what happens when someone visits `/login/`:

### 1. User visits URL
```
https://spookyoctober.com/login/
```

### 2. Django checks `spookyoctober/urls.py` (ROOT urls)
```python
urlpatterns = [
    path("", include("core.urls")),  # ← Matches! Goes to core/urls.py
]
```

### 3. Django checks `core/urls.py`
```python
urlpatterns = [
    path('login/', views.user_login, name='login'),  # ← Matches!
]
```

### 4. Django calls the view function in `core/views.py`
```python
def user_login(request):
    if request.method == 'POST':
        # Process form submission
        username = request.POST.get('username')
        # ... authenticate user
    return render(request, 'login.html')
```

### 5. Django renders the template `templates/login.html`
```html
{% extends 'base.html' %}
{% block content %}
    <!-- Your login form HTML -->
{% endblock %}
```

### 6. Django sends HTML response back to browser

---

## 📝 Templates vs Static HTML

### Static HTML:
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>
```

### Django Template:
```html
{% extends 'base.html' %}
{% load static %}

{% block content %}
    <h1>Hello {{ user.username }}</h1>
    <img src="{% static 'images/logo.png' %}">
{% endblock %}
```

**Key differences:**
- `{% %}` = Template tags (Python logic)
- `{{ }}` = Variables (output values)
- `{% extends %}` = Inherit from another template
- `{% block %}` = Define sections that can be overridden
- `{% static %}` = Generate URLs for static files

---

## 🎨 Working with Tailwind CSS

### Development Workflow:

1. **Edit templates** in `templates/`
2. **Add Tailwind classes** to your HTML:
   ```html
   <button class="btn-primary">Click me</button>
   ```

3. **Rebuild CSS** (in terminal):
   ```bash
   npm run build:css
   ```

4. **Collect static files** for Django:
   ```bash
   python manage.py collectstatic --noinput
   ```

### Using Custom Styles:

In `static/css/tailwind-input.css`:
```css
@layer components {
  .btn-halloween {
    @apply bg-orange-600 text-white px-4 py-2 rounded hover:bg-orange-700;
  }
}
```

Then rebuild: `npm run build:css`

---

## 🗄️ Database & Models

### In traditional websites:
You write SQL: `SELECT * FROM users WHERE username='john'`

### In Django:
You use the ORM (Object-Relational Mapper):
```python
# models.py
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()

# views.py
events = Event.objects.filter(date__gte=today)
```

**No SQL needed!** Django generates it for you.

---

## 🔐 User Authentication

Django has built-in authentication:

### Check if user is logged in (in templates):
```html
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <a href="{% url 'core:login' %}">Login</a>
{% endif %}
```

### Require login (in views):
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='core:login')
def dashboard(request):
    return render(request, 'dashboard.html')
```

---

## 📍 URL Patterns & Naming

### Define URLs in `urls.py`:
```python
urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
]
```

### Use URLs in templates:
```html
<!-- Static URL -->
<a href="/events/">Events</a>

<!-- Dynamic URL (BETTER - uses name) -->
<a href="{% url 'core:event_list' %}">Events</a>

<!-- URL with parameter -->
<a href="{% url 'core:event_detail' event_id=123 %}">Event #123</a>
```

**Why use {% url %}?**
- If you change the URL pattern, templates update automatically
- No broken links!

---

## 🎯 Common Django Patterns

### 1. List View (show all items)
```python
def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})
```

### 2. Detail View (show one item)
```python
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'event_detail.html', {'event': event})
```

### 3. Create View (add new item)
```python
def event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        # ... save to database
        return redirect('core:event_list')
    return render(request, 'event_form.html')
```

### 4. Update View (edit item)
```python
def event_edit(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.save()
        return redirect('core:event_detail', event_id=event.id)
    return render(request, 'event_form.html', {'event': event})
```

---

## 🧪 Development Workflow

### 1. Start development server:
```bash
make run
# or
python manage.py runserver
```

### 2. Visit in browser:
```
http://localhost:8000/
```

### 3. Make changes to code
- Templates update immediately (just refresh browser)
- Python code changes require server restart (Ctrl+C, then `make run` again)
- CSS changes require: `npm run build:css` + `collectstatic` + refresh

### 4. Check for errors:
- Terminal shows Python errors
- Browser console shows JavaScript errors
- Django debug page shows detailed error info (only in development)

---

## 🚀 Common Commands

```bash
# Start development server
make run

# Create database tables
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Open Python shell
python manage.py shell

# Run tests
python manage.py test

# Check for issues
python manage.py check

# Build Tailwind CSS
npm run build:css

# Collect static files
python manage.py collectstatic --noinput
```

---

## 🐛 Debugging Tips

### 1. Use Django Debug Toolbar (future sprint)
Shows queries, templates used, context variables

### 2. Print debugging:
```python
def my_view(request):
    events = Event.objects.all()
    print(f"Found {events.count()} events")  # Shows in terminal
    return render(request, 'template.html', {'events': events})
```

### 3. Template debugging:
```html
<!-- See what variables are available -->
{{ request.user }}
{{ request.path }}
{{ debug }}
```

### 4. Check the logs:
```bash
# Local development: terminal output

# Heroku:
heroku logs --tail --app spookyoctober
```

---

## 📚 Learning Resources

- **Official Django Tutorial**: https://docs.djangoproject.com/en/5.2/intro/tutorial01/
- **Django Girls Tutorial**: https://tutorial.djangogirls.org/
- **Django for Everybody** (free course): https://www.dj4e.com/
- **Tailwind CSS Docs**: https://tailwindcss.com/docs

---

## 🆘 Common Errors & Solutions

### "TemplateDoesNotExist"
- Check template name in `render()` matches filename
- Make sure template is in `templates/` folder

### "NoReverseMatch"
- Check URL name in `{% url 'core:name' %}` exists in urls.py
- Make sure app_name is defined in urls.py

### "relation does not exist"
- Run migrations: `python manage.py migrate`

### "CSRF verification failed"
- Add `{% csrf_token %}` to all forms
- Make sure `django.middleware.csrf.CsrfViewMiddleware` is in MIDDLEWARE

### Static files not loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings.py
- Make sure `{% load static %}` is at top of template

---

## 💡 Pro Tips

1. **Always use `{% url %}` instead of hardcoded URLs**
2. **Use `@login_required` decorator for protected views**
3. **Use `get_object_or_404()` instead of `.get()` to handle missing objects gracefully**
4. **Keep views simple - move logic to models or separate services**
5. **Use `{% block %}` tags to make templates reusable**
6. **Commit migrations to git**
7. **Never commit `.env` file (keep secrets secret!)**

---

## 🎓 Next Steps

Once you're comfortable with basics, explore:
- Django Forms (automatic form generation)
- Class-Based Views (more structured views)
- Django REST Framework (build APIs)
- Celery (background tasks)
- Django Channels (websockets/real-time features)

---

**Happy Coding! 🎃**

If you get stuck, check:
1. The verbose comments in `urls.py` and `views.py`
2. This guide
3. Django documentation
4. Project documentation in `/docs/`
