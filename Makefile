.PHONY: help setup run install migrate makemigrations createsuperuser shell test clean collectstatic check deploy-check css css-watch

help:
	@echo "SpookyOctober - Django Project Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup            - Initial project setup (first time only)"
	@echo "  make run              - Run the Django development server"
	@echo "  make install          - Install project dependencies"
	@echo "  make migrate          - Run database migrations"
	@echo "  make makemigrations   - Create new database migrations"
	@echo "  make createsuperuser  - Create a Django admin superuser"
	@echo "  make shell            - Open Django shell"
	@echo "  make test             - Run tests"
	@echo "  make check            - Run Django system checks"
	@echo "  make collectstatic    - Collect static files"
	@echo "  make css              - Build Tailwind CSS"
	@echo "  make css-watch        - Watch and rebuild Tailwind CSS on changes"
	@echo "  make clean            - Remove Python cache files and SQLite db"
	@echo "  make deploy-check     - Verify Heroku deployment readiness"
	@echo ""

setup:
	@echo "🎃 Setting up SpookyOctober for the first time..."
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file..."; \
		cp .env.example .env; \
		echo "✅ .env file created"; \
	else \
		echo "✅ .env file already exists"; \
	fi
	@echo "📦 Installing Python dependencies..."
	@pip install -r requirements.txt
	@echo "📦 Installing Node dependencies..."
	@npm install
	@echo "🎨 Building Tailwind CSS..."
	@npm run build:css
	@echo "🗄️  Running migrations..."
	@python manage.py migrate
	@echo "📦 Collecting static files..."
	@python manage.py collectstatic --noinput
	@echo ""
	@echo "✨ Setup complete! Run 'make run' to start the development server."
	@echo "💡 Visit http://localhost:8000/ to see your app!"
	@echo ""

run:
	@if [ ! -f .env ]; then \
		echo "⚠️  .env file not found! Run 'make setup' first."; \
		exit 1; \
	fi
	@echo "🎃 Starting SpookyOctober development server..."
	@echo ""
	@echo "💡 Visit: http://localhost:8000/"
	@echo "⚠️  Important: Use HTTP (not HTTPS)"
	@echo ""
	@python manage.py runserver

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

migrate:
	@echo "🗄️  Running database migrations..."
	python manage.py migrate

makemigrations:
	@echo "📝 Creating new migrations..."
	python manage.py makemigrations

createsuperuser:
	@echo "👤 Creating admin superuser..."
	python manage.py createsuperuser

shell:
	@echo "🐚 Opening Django shell..."
	python manage.py shell

test:
	@echo "🧪 Running tests..."
	python manage.py test

check:
	@echo "✅ Running Django system checks..."
	python manage.py check

collectstatic:
	@echo "📦 Collecting static files..."
	python manage.py collectstatic --noinput

css:
	@echo "🎨 Building Tailwind CSS..."
	npm run build:css

css-watch:
	@echo "👀 Watching Tailwind CSS for changes..."
	npm run watch:css

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.db" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -f db.sqlite3
	@echo "✨ Cleanup complete!"

deploy-check:
	@echo "🚀 Checking Heroku deployment readiness..."
	@echo ""
	@echo "Required files:"
	@test -f Procfile && echo "  ✅ Procfile exists" || echo "  ❌ Procfile missing"
	@test -f runtime.txt && echo "  ✅ runtime.txt exists" || echo "  ❌ runtime.txt missing"
	@test -f requirements.txt && echo "  ✅ requirements.txt exists" || echo "  ❌ requirements.txt missing"
	@echo ""
	@echo "Django checks:"
	@python manage.py check --deploy 2>/dev/null && echo "  ✅ Django deployment checks passed" || echo "  ⚠️  Django deployment checks have warnings (review them)"
	@echo ""
	@echo "Environment variables needed on Heroku:"
	@echo "  - SECRET_KEY"
	@echo "  - DEBUG=False"
	@echo "  - ALLOWED_HOSTS=<your-app>.herokuapp.com"
	@echo "  - DATABASE_URL (auto-set by Heroku PostgreSQL)"
	@echo ""
	@echo "Ready to deploy! Run: git push heroku main"
