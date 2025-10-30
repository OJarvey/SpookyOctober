# Heroku Deployment Quick Start

Since you already have a PostgreSQL database provisioned on Heroku, follow these steps to deploy:

## 1. Prerequisites Checklist
- [x] Django project created
- [x] requirements.txt generated
- [x] Procfile created
- [x] runtime.txt created
- [x] Settings configured for Heroku
- [x] PostgreSQL database provisioned on Heroku

## 2. Set Environment Variables on Heroku

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set the environment variables
heroku config:set SECRET_KEY='<generated-secret-key>'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='<your-app-name>.herokuapp.com'

# Verify DATABASE_URL is already set (from your provisioned PostgreSQL)
heroku config:get DATABASE_URL
```

## 3. Deploy to Heroku

```bash
# If not already initialized as Heroku app:
# heroku git:remote -a <your-heroku-app-name>

# Push to Heroku
git push heroku main
```

## 4. Run Post-Deployment Commands

```bash
# Run migrations on Heroku PostgreSQL
heroku run python manage.py migrate

# Collect static files
heroku run python manage.py collectstatic --noinput

# Create admin superuser
heroku run python manage.py createsuperuser
```

## 5. Verify Deployment

```bash
# Open your app
heroku open

# Monitor logs
heroku logs --tail
```

## 6. Quick Checks

Visit these URLs:
- `https://<your-app-name>.herokuapp.com/` - Home page
- `https://<your-app-name>.herokuapp.com/admin/` - Django admin

## Troubleshooting

### If you get errors:

```bash
# Check logs
heroku logs --tail

# Check dyno status
heroku ps

# Restart dynos
heroku restart

# Check database connection
heroku pg:info
```

### Common Issues:

1. **ALLOWED_HOSTS error**: Make sure you set ALLOWED_HOSTS with your Heroku app URL
2. **Static files not loading**: Run `heroku run python manage.py collectstatic --noinput`
3. **Database errors**: Verify `heroku config:get DATABASE_URL` returns a valid PostgreSQL URL
4. **Application error**: Check `heroku logs --tail` for detailed error messages

## Environment Variables Summary

Required on Heroku:
- `SECRET_KEY` - Django secret key (required)
- `DEBUG` - Set to False (required)
- `ALLOWED_HOSTS` - Your Heroku domain (required)
- `DATABASE_URL` - Already set by Heroku PostgreSQL addon (auto-configured)

## Next Steps After Deployment

1. Test all functionality on production
2. Set up your app-specific features
3. Configure custom domain (optional)
4. Set up monitoring/alerts
5. Regular database backups: `heroku pg:backups:schedule`
