# Project Context: SpookyOctober

## Core Principles
- Use conventional commits taxonomy for commit messages (feat:, fix:, docs:, etc.)
- Don't run the Django app as a background process - user runs it interactively
- Prioritize clarity over brevity - this is a beginner-friendly codebase
- Team is new to Django, coming from static HTML/Bootstrap backgrounds

## Tech Stack
- **Backend**: Django 5.2.7 with PostgreSQL on Heroku
- **Frontend**: Django Templates + Tailwind CSS 3.4
- **Python**: 3.12.7 (managed via pyenv)
- **CSS Build**: Tailwind CLI (npm run build:css)
- **Deployment**: Heroku with Gunicorn + WhiteNoise

## Project Structure
```
SpookyOctober/
├── spookyoctober/      # Django project settings
├── core/               # Main app (auth, home views)
├── templates/          # Global templates (base.html, 404.html)
├── static/css/         # Tailwind source files
│   ├── tailwind-input.css    # EDIT THIS
│   └── tailwind-output.css   # Generated - don't edit
├── docs/               # Comprehensive documentation
│   ├── BEGINNERS_GUIDE.md
│   ├── TAILWIND_CUSTOMIZATION.md
│   └── SPRINT_ROADMAP.md
└── Makefile           # Common tasks
```

## Key Files to Reference

### Documentation
- `docs/BEGINNERS_GUIDE.md` - Django concepts explained for newcomers
- `docs/TAILWIND_CUSTOMIZATION.md` - Complete Tailwind customization guide
- `docs/SPRINT_ROADMAP.md` - 8-sprint development roadmap
- `docs/DATABASE_SCHEMA.md` - Database structure and relationships
- `docs/QUICK_REFERENCE.md` - Common commands and patterns

### Configuration
- `tailwind.config.js` - Theme colors: pumpkin (#FF6600), midnight (#1a1a1a), spooky-purple (#6B2D6B)
- `core/urls.py` - URL patterns with extensive beginner-friendly comments
- `spookyoctober/settings.py` - Django settings with Heroku configuration

### Templates
- `templates/base.html` - Base template with navbar, footer, flash messages
- `templates/home.html` - Landing page
- `templates/login.html` - Authentication
- `templates/dashboard.html` - User dashboard with technical stats

## Development Workflow

### Daily Development
```bash
make run           # Start Django dev server (http://localhost:8000)
make css-watch     # Watch Tailwind CSS for changes (run in separate terminal)
```

### Common Tasks
```bash
make setup         # First-time setup (one command does everything)
make css           # Build Tailwind CSS once
make migrate       # Run database migrations
make makemigrations # Create new migrations
make test          # Run test suite
make createsuperuser # Create admin user
```

### Deployment
```bash
git push origin main       # Push to GitHub
git push heroku main       # Deploy to Heroku
heroku logs --tail         # View production logs
```

## Code Conventions

### Python/Django
- Follow PEP 8 (use 88-120 char line length, not strict 79)
- All views must have docstrings explaining purpose
- Use Django's built-in features (forms, ORM, auth) when possible
- Use `@login_required` decorator for protected views
- Add CSRF tokens to all forms (`{% csrf_token %}`)
- Follow existing naming patterns in codebase

### Templates
- All templates extend `base.html`
- Use Django template tags: `{% url 'core:home' %}`, not hardcoded URLs
- Mobile-first responsive design
- Use Halloween theme colors and emoji (🎃, 👻)

### Tailwind CSS
- Edit `static/css/tailwind-input.css` (NOT tailwind-output.css)
- Use custom components for repeated patterns (btn-primary, btn-secondary, card)
- Use theme colors: `bg-pumpkin`, `text-midnight`, `text-spooky-purple`
- Create new components with `@apply` in `@layer components`
- Run `make css` after config changes

### Testing
- Use Django's `TestCase` class
- Test both authenticated and unauthenticated flows
- Aim for >80% code coverage
- Test files go in app's `tests.py` or `tests/` directory

## Halloween Theme

### Colors
- **Primary**: #FF6600 (pumpkin orange) - Use `bg-pumpkin`, `text-pumpkin`
- **Dark**: #1a1a1a (midnight black) - Use `bg-midnight`, `text-midnight`
- **Accent**: #6B2D6B (spooky purple) - Use `bg-spooky-purple`, `text-spooky-purple`

### Branding
- Use 🎃 emoji for main branding and positive messages
- Use 👻 emoji for errors, 404 pages, and playful messages
- User-facing text should be friendly and Halloween-themed
- Example: "Welcome back, username! 👻" instead of just "Welcome back"

## Current Development Status

### Completed (Sprint 0)
- ✅ Django project initialized
- ✅ PostgreSQL database configured
- ✅ Heroku deployment pipeline
- ✅ Tailwind CSS integration
- ✅ Basic authentication (login/logout)
- ✅ Responsive base template with navbar
- ✅ Home page with features
- ✅ Dashboard with technical stats
- ✅ Custom 404 page
- ✅ Comprehensive beginner documentation

### Current Sprint (Sprint 1)
**Focus**: Core Authentication & User Management

**GitHub Issues**: See issues tagged with `sprint-1` label
- User registration with email validation
- Password reset flow
- User profile pages with photo upload
- User types (visitor, business_owner, city_official)
- Role-based permissions
- Authentication tests

### Next Sprints
- Sprint 2: Location System & Interactive Map
- Sprint 3: Event Management
- Sprint 4: Haunted Places & Stories
- Sprint 5: Business Promotions & Coupons

See `docs/SPRINT_ROADMAP.md` for complete roadmap.

## Important Reminders

### For Code Suggestions
1. **Add verbose comments** - Team is new to Django, explain what code does
2. **Reference docs** - Check `docs/` folder before suggesting solutions
3. **Use existing patterns** - Match coding style in `core/views.py` and `core/urls.py`
4. **Mobile-responsive** - All UI must work on mobile (mobile-first Tailwind)
5. **Security** - Always include CSRF tokens, use `@login_required`, validate input

### For Templates
1. **Always extend base.html** - `{% extends 'base.html' %}`
2. **Use named URLs** - `{% url 'core:home' %}` not `/`
3. **Use theme colors** - Don't hardcode colors, use Tailwind theme classes
4. **Flash messages** - Already handled in base.html, use Django messages framework
5. **Static files** - `{% load static %}` and `{% static 'css/tailwind-output.css' %}`

### For Tailwind CSS
1. **Never edit tailwind-output.css** - It's generated, changes will be overwritten
2. **Edit tailwind-input.css** - Add custom CSS here
3. **Use @apply in components** - For repeated patterns, create component classes
4. **Rebuild CSS** - Run `make css` or `make css-watch` after changes
5. **Check config** - Custom colors defined in `tailwind.config.js`

### For Database Changes
1. **Always create migrations** - `make makemigrations` after model changes
2. **Test migrations locally** - `make migrate` before pushing
3. **Check for conflicts** - Review migration files before committing
4. **Document schema** - Update `docs/DATABASE_SCHEMA.md` for new models

## Useful Commands Reference

### Django Management
```bash
python manage.py shell                    # Interactive Python shell with Django
python manage.py dbshell                  # Direct PostgreSQL shell
python manage.py check                    # Run system checks
python manage.py check --deploy           # Deployment checks
python manage.py collectstatic --noinput  # Collect static files
```

### Git (Conventional Commits)
```bash
git commit -m "feat: add user registration form"
git commit -m "fix: correct password reset email template"
git commit -m "docs: update BEGINNERS_GUIDE with ORM examples"
git commit -m "style: apply consistent indentation"
git commit -m "refactor: simplify login view logic"
git commit -m "test: add user registration tests"
git commit -m "chore: update dependencies"
```

### Heroku
```bash
heroku logs --tail --app spookyoctober    # View logs
heroku run python manage.py migrate       # Run migrations on production
heroku run python manage.py shell         # Production shell
heroku config                             # View environment variables
heroku config:set KEY=value               # Set environment variable
```

## Common Patterns

### View Example
```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def my_view(request):
    """
    Brief description of what this view does.

    Accessible at: /my-url/
    Template: my_template.html
    """
    if request.method == 'POST':
        # Handle form submission
        messages.success(request, 'Action completed! 🎃')
        return redirect('core:home')

    context = {
        'data': 'value',
    }
    return render(request, 'my_template.html', context)
```

### Template Example
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Page Title - SpookyOctober{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold text-pumpkin mb-6">🎃 Heading</h1>

    <div class="card">
        <p class="text-gray-700">Content here</p>
        <a href="{% url 'core:home' %}" class="btn-primary">Go Home</a>
    </div>
</div>
{% endblock %}
```

### Form Example
```python
from django import forms
from django.contrib.auth.models import User

class MyForm(forms.ModelForm):
    """Brief description of form purpose."""

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use.')
        return email
```

## Production Environment

### Deployed Application
- **URL**: https://spookyoctober-2f7f54251dfc.herokuapp.com
- **Admin**: https://spookyoctober-2f7f54251dfc.herokuapp.com/admin/
- **GitHub**: https://github.com/Hackathon-Team13/SpookyOctober
- **Project Board**: https://github.com/orgs/Hackathon-Team13/projects/1

### Environment Variables (Heroku)
- `SECRET_KEY` - Django secret key
- `DEBUG` - Should be False in production
- `ALLOWED_HOSTS` - spookyoctober-2f7f54251dfc.herokuapp.com
- `DATABASE_URL` - Auto-set by Heroku PostgreSQL addon

## When In Doubt
1. Check `docs/BEGINNERS_GUIDE.md` for Django explanations
2. Check `docs/TAILWIND_CUSTOMIZATION.md` for CSS questions
3. Check `docs/SPRINT_ROADMAP.md` for feature roadmap
4. Look at existing code in `core/views.py` for patterns
5. Review `core/urls.py` for URL naming conventions
6. Check GitHub issues for current sprint tasks

**Remember**: This is a learning project. Prioritize clear, well-commented code over clever solutions.
