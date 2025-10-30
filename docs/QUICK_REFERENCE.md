# Quick Reference

## Project Structure (Planned)
```
SpookyOctober/
├── docs/                    # Project documentation
├── [project_name]/         # Django project directory
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── [app_name]/             # Django apps
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
├── static/                 # Static files (CSS, JS, images)
├── staticfiles/           # Collected static files for production
├── templates/             # Global templates
├── .env                   # Environment variables (not in git)
├── .env.example          # Example environment variables
├── .gitignore
├── manage.py
├── Procfile              # Heroku process configuration
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version for Heroku
└── README.md
```

## Makefile Commands

Quick access to common tasks:
```bash
make help              # Show all available commands
make run               # Run development server
make install           # Install dependencies
make migrate           # Run migrations
make makemigrations    # Create new migrations
make createsuperuser   # Create admin user
make shell             # Open Django shell
make test              # Run tests
make check             # Run system checks
make collectstatic     # Collect static files
make clean             # Clean up cache files
make deploy-check      # Verify Heroku readiness
```

## Common Django Commands

### Project Setup
```bash
django-admin startproject [project_name] .
python manage.py startapp [app_name]
```

### Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py dbshell
```

### User Management
```bash
python manage.py createsuperuser
python manage.py changepassword [username]
```

### Development
```bash
python manage.py runserver
python manage.py shell
python manage.py check
```

### Static Files
```bash
python manage.py collectstatic
python manage.py findstatic [filename]
```

## Git Workflow
```bash
git status
git add .
git commit -m "descriptive message"
git push origin main
```

## Heroku Workflow
```bash
# Deploy
git push heroku main

# Run commands
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

# Monitor
heroku logs --tail
heroku ps

# Database
heroku pg:info
heroku pg:psql  # Connect to database
```

## Environment Variables
See `.env.example` for required variables.

### Local Development
Copy `.env.example` to `.env` and update values.

### Production (Heroku)
Set via Heroku CLI:
```bash
heroku config:set KEY=value
heroku config:get KEY
heroku config
```

## Halloween Theme Ideas
- Color palette: #FF6600 (orange), #1a1a1a (black), #6B2D6B (purple)
- Fonts: Creepster, Nosifer, Eater (Google Fonts)
- Icons: Font Awesome Halloween icons
- Effects: CSS animations, particles.js for spooky effects

## Resources
- Django Docs: https://docs.djangoproject.com/
- Heroku Django: https://devcenter.heroku.com/articles/django-app-configuration
- PostgreSQL: https://www.postgresql.org/docs/
