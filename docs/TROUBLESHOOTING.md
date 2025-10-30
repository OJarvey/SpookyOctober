# Troubleshooting Guide

## Common Issues and Solutions

### Issue: "UserWarning: No directory at: /Volumes/.../staticfiles/"

**Cause**: The staticfiles directory hasn't been created yet.

**Solution**:
```bash
python manage.py collectstatic --noinput
```

Or use the Makefile:
```bash
make collectstatic
```

---

### Issue: "Bad request version" or "You're accessing the development server over HTTPS"

**Cause**: Browser is trying to access `https://localhost:8000/` but Django dev server only supports HTTP.

**Solution**:
Access the site using HTTP (not HTTPS):
```
http://localhost:8000/
```

**Safari-specific fix**:
Safari may force HTTPS due to HSTS. Clear Safari's HSTS cache:
```bash
# Close Safari completely first
rm -rf ~/Library/Cookies/HSTS.plist
# Restart Safari
```

Or use Chrome/Firefox for local development.

---

### Issue: Safari/Browser can't open localhost:8000

**Causes**:
1. Missing `.env` file (causing DEBUG to default to False)
2. Missing staticfiles directory
3. Server not running properly
4. Trying to access via HTTPS instead of HTTP

**Solution**:
```bash
# Make sure .env file exists
cp .env.example .env

# Run collectstatic
python manage.py collectstatic --noinput

# Start the server
python manage.py runserver
```

Or use the Makefile setup command:
```bash
make setup
make run
```

**Important**: Always use `http://localhost:8000/` (not `https://`)

---

### Issue: "DisallowedHost" error

**Cause**: The hostname you're using isn't in ALLOWED_HOSTS.

**Solution**:
1. For local development, make sure your `.env` file has:
```
ALLOWED_HOSTS=localhost,127.0.0.1
```

2. For production (Heroku), set:
```bash
heroku config:set ALLOWED_HOSTS='your-app.herokuapp.com'
```

---

### Issue: Database connection errors on Heroku

**Solution**:
1. Verify PostgreSQL addon is provisioned:
```bash
heroku addons
```

2. Check DATABASE_URL is set:
```bash
heroku config:get DATABASE_URL
```

3. Run migrations on Heroku:
```bash
heroku run python manage.py migrate
```

---

### Issue: Static files not loading on Heroku

**Solution**:
1. Ensure WhiteNoise is in requirements.txt
2. Run collectstatic:
```bash
heroku run python manage.py collectstatic --noinput
```
3. Verify STATIC_ROOT in settings.py
4. Check that WhiteNoise middleware is enabled

---

### Issue: "Port already in use" error

**Cause**: Another process is running on port 8000.

**Solution**:
```bash
# Kill process on port 8000 (macOS/Linux)
lsof -ti:8000 | xargs kill -9

# Or kill all Django processes
pkill -f "manage.py runserver"
```

---

### Issue: SECRET_KEY warnings

**Cause**: Using the default Django-generated SECRET_KEY.

**Solution**:
```python
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Add it to .env for local development
SECRET_KEY=<generated-key>

# Or set it on Heroku
heroku config:set SECRET_KEY='<generated-key>'
```

---

## First Time Setup Checklist

If you're setting up the project for the first time:

1. ✅ Activate virtual environment
2. ✅ Install dependencies: `pip install -r requirements.txt`
3. ✅ Create .env file: `cp .env.example .env`
4. ✅ Run migrations: `python manage.py migrate`
5. ✅ Collect static files: `python manage.py collectstatic --noinput`
6. ✅ Create admin user: `python manage.py createsuperuser` (optional)
7. ✅ Start server: `python manage.py runserver`

Or simply run:
```bash
make setup
make run
```

---

## Getting Help

- Check Django logs for error messages
- Use `make check` to run system checks
- Use `make deploy-check` before deploying to Heroku
- Review the [Django documentation](https://docs.djangoproject.com/)
- Check [Heroku Django documentation](https://devcenter.heroku.com/articles/django-app-configuration)
