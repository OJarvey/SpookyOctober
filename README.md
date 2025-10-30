# SpookyOctober
Halloween-themed hackathon project built with Django and PostgreSQL

## Tech Stack
- Django 5.x
- PostgreSQL
- Heroku hosting
- Python 3.12

## Documentation
All project documentation is in the `/docs` directory:
- [Project Overview](./docs/PROJECT_OVERVIEW.md) - High-level project info
- [Tech Stack](./docs/TECH_STACK.md) - Technical details and dependencies
- [Features](./docs/FEATURES.md) - Feature specifications
- [Database Schema](./docs/DATABASE_SCHEMA.md) - Data models
- [Development Log](./docs/DEVELOPMENT_LOG.md) - Progress tracking and decisions
- [Deployment](./docs/DEPLOYMENT.md) - Heroku deployment guide

## Quick Start

### Local Development

**Using Make (Recommended):**
```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# First time setup (creates .env, runs migrations, collects static files)
make setup

# Run the development server
make run

# See all available commands
make help

# Other useful commands
make migrate              # Run migrations
make createsuperuser      # Create admin user
make check                # Run system checks
make deploy-check         # Check Heroku deployment readiness
```

**Manual Commands:**
```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env if you want custom settings

# Run migrations
python manage.py migrate

# Collect static files (fixes staticfiles warning)
python manage.py collectstatic --noinput

# Create admin user (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit **http://localhost:8000/** to see the Halloween home page!

**Important**: Use `http://` (not `https://`) - the development server doesn't support HTTPS.

### Deploy to Heroku
See [DEPLOYMENT_QUICKSTART.md](./DEPLOYMENT_QUICKSTART.md) for step-by-step deployment instructions.

Since PostgreSQL is already provisioned on your Heroku app, you just need to:
1. Set environment variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
2. Push to Heroku
3. Run migrations
4. Create superuser

## Project Status
✅ Django 5.2.7 project initialized
✅ Heroku deployment files created
✅ PostgreSQL configuration ready
✅ Basic Halloween-themed home page
✅ Ready for feature development and deployment!
