# Deployment Guide - Heroku

## Prerequisites
- Heroku CLI installed
- Heroku account
- Git repository

## Initial Heroku Setup

### 1. Create Heroku App
```bash
heroku create spooky-october-[your-name]
```

### 2. Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:essential-0
```

### 3. Set Environment Variables
```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='shriekedin.uk,www.shriekedin.uk,spookyoctober-2f7f54251dfc.herokuapp.com'
```

**Note:** ALLOWED_HOSTS should include:
- Your custom domain (shriekedin.uk)
- The www subdomain (www.shriekedin.uk)
- Your Heroku app domain (*.herokuapp.com)

### 4. Configure Custom Domain (Optional)
```bash
# Add custom domains to Heroku
heroku domains:add shriekedin.uk
heroku domains:add www.shriekedin.uk

# View DNS configuration instructions
heroku domains
```

**DNS Configuration:**
- Create an ALIAS/ANAME record for `shriekedin.uk` pointing to your Heroku app
- Create a CNAME record for `www.shriekedin.uk` pointing to your Heroku app
- Heroku will provide the specific DNS target when you run `heroku domains`

## Required Files

### Procfile
```
web: gunicorn [project_name].wsgi --log-file -
```

### runtime.txt
```
python-3.12.x
```

### requirements.txt
Generated from:
```bash
pip freeze > requirements.txt
```

## Django Configuration for Heroku

### Settings Updates Needed
```python
# settings.py

import os
import dj_database_url

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## Deployment Commands

### First Deployment
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Subsequent Deployments
```bash
git push heroku main
# If there are migrations:
heroku run python manage.py migrate
```

## Useful Heroku Commands

### View Logs
```bash
heroku logs --tail
```

### Run Django Shell
```bash
heroku run python manage.py shell
```

### Database Backup
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

### Open App
```bash
heroku open
```

## Troubleshooting

### Check Dyno Status
```bash
heroku ps
```

### Restart Dynos
```bash
heroku restart
```

### Database Connection Issues
```bash
heroku pg:info
heroku config:get DATABASE_URL
```

## Production Checklist
- [ ] DEBUG=False
- [ ] SECRET_KEY set via environment variable
- [ ] ALLOWED_HOSTS configured
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Admin user created
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate active
- [ ] Monitoring set up (Heroku dashboard)

## Cost Considerations
- Hobby dyno: $7/month
- Essential Postgres: $5/month
- Total: ~$12/month

For hackathon: Can use free tier with limitations.
