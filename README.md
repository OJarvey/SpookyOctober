# ShriekedIn
Professional Halloween networking platform built with Django and PostgreSQL.

**Live Site:** [https://shriekedin.uk](https://shriekedin.uk) | [https://www.shriekedin.uk](https://www.shriekedin.uk)

## Tech Stack
- Django 5.2.7
- PostgreSQL
- Heroku hosting
- Python 3.12.7
- Tailwind CSS 3.4

## Prerequisites

### Python Version
This project requires **Python 3.12.7**. We recommend using [pyenv](https://github.com/pyenv/pyenv) to manage Python versions.

#### Installing Python with pyenv (Recommended)

**macOS/Linux:**
```bash
# Install pyenv (if not already installed)
curl https://pyenv.run | bash

# Install Python 3.12.7
pyenv install 3.12.7

# Set Python version for this project
pyenv local 3.12.7

# Verify version
python --version  # Should show: Python 3.12.7
```

**Windows:**
Use [pyenv-win](https://github.com/pyenv-win/pyenv-win) or download Python 3.12.7 from [python.org](https://www.python.org/downloads/)

**Why pyenv?**
- Easily switch between Python versions
- Avoid conflicts with system Python
- Match production environment exactly
- Project-specific Python versions (`.python-version` file)

#### Without pyenv
If you prefer not to use pyenv, ensure you have Python 3.12.7 installed:
```bash
python --version  # Should be 3.12.7 (or at least 3.12.x)
```

### Node.js (for Tailwind CSS)
Required for building Tailwind CSS styles:
```bash
node --version   # Should be v16+ or higher
npm --version    # Should be 8+ or higher
```

## Documentation
All project documentation is in the `/docs` directory:

**🚀 Start Here**:
- [Sprint Roadmap](./docs/SPRINT_ROADMAP.md) - Development plan with prioritized sprints
- [Requirements Document](./docs/halloween-urs-doc.md) - Complete URS specifications

**Project Info**:
- [Project Overview](./docs/PROJECT_OVERVIEW.md) - High-level project info
- [Features](./docs/FEATURES.md) - Feature specifications by sprint
- [Database Schema](./docs/DATABASE_SCHEMA.md) - Data models

**Development**:
- [Beginner's Guide](./docs/BEGINNERS_GUIDE.md) - 🌟 **New to Django? Start here!**
- [Tech Stack](./docs/TECH_STACK.md) - Technical details and dependencies
- [Development Log](./docs/DEVELOPMENT_LOG.md) - Progress tracking and decisions
- [Quick Reference](./docs/QUICK_REFERENCE.md) - Common commands and tips
- [Troubleshooting](./docs/TROUBLESHOOTING.md) - Common issues and solutions

**Deployment**:
- [Deployment Guide](./docs/DEPLOYMENT.md) - Heroku deployment guide
- [Deployment Quickstart](./DEPLOYMENT_QUICKSTART.md) - Quick deployment steps

## Quick Start

### Local Development

**Step 1: Ensure Python 3.12.7 is installed**
```bash
python --version  # Should show Python 3.12.7
```

**Step 2: Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**Step 3: Setup and run (Using Make - Recommended)**
```bash
# First time setup (installs deps, builds CSS, runs migrations)
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
