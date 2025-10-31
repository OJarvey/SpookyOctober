# ShriekedIn Development Guide

## Quick Start

For the best development experience with automatic reloading:

```bash
make dev
```

This command will:
- ✅ Run initial Django template checks with djlint
- 🚀 Start the Django development server on http://localhost:8000/
- 👀 Watch for Tailwind CSS changes and auto-rebuild
- 🔄 Show warnings from both djlint and Tailwind CSS

**Press Ctrl+C to stop all services**

## Development Commands

### Core Development

- **`make dev`** - 🚀 **Recommended!** Run full development environment with auto-reload
- **`make run`** - Run Django dev server only (no CSS watching)
- **`make shell`** - Open Django Python shell

### Template Quality

- **`make lint-templates`** - Check Django templates for issues with djlint
- **`make format-templates`** - Auto-format Django templates with djlint

### Styling

- **`make css`** - Build Tailwind CSS once (production build)
- **`make css-watch`** - Watch and auto-rebuild Tailwind CSS on changes

**Important:** After modifying any Tailwind classes in templates, the CSS will auto-rebuild if you're using `make dev` or `make css-watch`. Otherwise, run `make css` manually.

### Database

- **`make migrate`** - Apply database migrations
- **`make makemigrations`** - Create new migrations from model changes

### Testing & Validation

- **`make test`** - Run Django tests
- **`make check`** - Run Django system checks
- **`make deploy-check`** - Verify Heroku deployment readiness

### Project Setup

- **`make setup`** - First-time project setup (dependencies, migrations, static files)
- **`make install`** - Install Python dependencies only
- **`make clean`** - Remove cache files and SQLite database

## djlint Configuration

Template linting is configured in `.djlintrc`:

- **Profile:** Django
- **Indentation:** 4 spaces
- **Max line length:** 120 characters
- **Auto-formats:** CSS and JavaScript within templates
- **Excluded:** node_modules, venv, staticfiles, generated CSS

### Common djlint Issues

djlint helps catch:
- Incorrect template tag usage
- Missing closing tags
- Inconsistent indentation
- Long lines that should be broken up
- Accessibility issues (missing alt text, etc.)

## Tailwind CSS Workflow

### Adding New Styles

1. Add Tailwind utility classes to your HTML templates
2. If using `make dev`: CSS rebuilds automatically
3. If not using `make dev`: Run `make css` to rebuild
4. Refresh your browser to see changes

### Custom CSS

For custom styles beyond Tailwind utilities:
1. Add them to `static/css/tailwind-input.css`
2. Run `make css` or use `make dev` for auto-rebuild

## Recommended Workflow

### For Active Development

```bash
# Terminal 1: Run the full dev environment
make dev
```

This gives you:
- Django server with auto-reload on Python changes
- Tailwind CSS auto-rebuild on template changes
- Initial template quality checks

### For Template Work

```bash
# Check templates before committing
make lint-templates

# Auto-format templates
make format-templates
```

### Pre-Commit Checklist

Before committing code:

1. ✅ Run `make lint-templates` - Ensure templates are properly formatted
2. ✅ Run `make check` - Verify Django configuration
3. ✅ Run `make test` - Ensure tests pass
4. ✅ Run `make css` - Build production CSS (if you modified styles)

## Tips for Junior Developers

### Understanding the Development Flow

1. **Edit a template** (`templates/*.html`)
   - Tailwind CSS auto-rebuilds (if using `make dev`)
   - Django auto-reloads the page
   - Refresh browser to see changes

2. **Edit Python code** (`*.py` files)
   - Django dev server auto-restarts
   - Refresh browser to see changes

3. **Edit Tailwind classes**
   - CSS rebuilds automatically with `make dev`
   - No need to manually rebuild

### Common Issues

**"I changed Tailwind classes but nothing happened"**
- Make sure you're using `make dev` or `make css-watch`
- Or manually run `make css`
- Hard refresh your browser (Cmd+Shift+R or Ctrl+Shift+R)

**"djlint is showing formatting errors"**
- Run `make format-templates` to auto-fix most issues
- Review the changes before committing

**"Background processes won't stop"**
- Press Ctrl+C in the terminal running `make dev`
- If stuck, run: `pkill -f "python manage.py runserver"` and `pkill -f "tailwindcss"`

## Environment Variables

Development environment variables are in `.env`:

```bash
DEBUG=True
SECRET_KEY=your-dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

See `.env.example` for all available options.

## Getting Help

- **Makefile commands:** Run `make help`
- **Django docs:** https://docs.djangoproject.com/
- **Tailwind CSS docs:** https://tailwindcss.com/docs
- **djlint docs:** https://djlint.com/

---

Happy coding! 🎃👻
