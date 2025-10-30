# Technical Stack

## Backend
- **Framework**: Django 5.x
- **Language**: Python 3.12
- **ORM**: Django ORM

## Database
- **Development**: PostgreSQL (local)
- **Production**: Heroku Postgres
- **Migrations**: Django migrations

## Hosting & Infrastructure
- **Platform**: Heroku
- **Web Server**: Gunicorn
- **Static Files**: WhiteNoise or Heroku-compatible static file serving

## Required Heroku Buildpacks
- heroku/python

## Environment Variables (to configure)
- `SECRET_KEY`
- `DATABASE_URL` (auto-configured by Heroku Postgres)
- `DEBUG` (False in production)
- `ALLOWED_HOSTS`

## Development Dependencies
TBD - to be defined in requirements.txt

## Production Dependencies
- Django
- psycopg2-binary (PostgreSQL adapter)
- gunicorn
- whitenoise (static files)
- django-environ (environment variable management)

## Files Needed for Heroku Deployment
- `Procfile` - Process types (web, worker)
- `runtime.txt` - Python version
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment variables
