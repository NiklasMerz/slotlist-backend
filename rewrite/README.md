# Slotlist Backend - Django Rewrite

This directory contains the Django+Django Ninja rewrite of the slotlist.info backend.

## Overview

The original backend was built with:
- **Framework**: Hapi.js (Node.js/TypeScript)
- **Database**: PostgreSQL with Sequelize ORM
- **Authentication**: JWT with Steam SSO

The new backend is built with:
- **Framework**: Django 4.2 with Django Ninja
- **Database**: PostgreSQL with Django ORM
- **Authentication**: JWT with Steam SSO

## Installation

### Requirements
- Python 3.9 or higher
- PostgreSQL 9.6 or higher
- Virtual environment (venv)

### Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the rewrite directory with the following variables:
```
# Django
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*

# Database
DB_DATABASE=slotlist
DB_USERNAME=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# JWT
CONFIG_JWT_SECRET=your-jwt-secret
CONFIG_JWT_ISSUER=slotlist.info
CONFIG_JWT_AUDIENCE=slotlist.info
CONFIG_JWT_EXPIRESIN=86400

# Steam API
CONFIG_STEAM_API_SECRET=your-steam-api-key

# Google Cloud Storage
CONFIG_STORAGE_BUCKETNAME=your-bucket-name
CONFIG_STORAGE_PROJECTID=your-project-id

# Default Admin User
DEFAULT_ADMIN_STEAMID=your-steam-id
DEFAULT_ADMIN_NICKNAME=your-nickname

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Documentation

Django Ninja provides automatic API documentation:
- **Interactive docs**: `http://localhost:8000/api/docs`
- **OpenAPI schema**: `http://localhost:8000/api/openapi.json`

## API Endpoints

### Authentication
- `GET /api/v1/auth/steam/return` - Steam authentication return handler
- `POST /api/v1/auth/refresh` - Refresh JWT token

### Status
- `GET /api/v1/status` - Get API status and uptime

### Users
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{uid}` - Get user by UID
- `PATCH /api/v1/users/{uid}` - Update user
- `GET /api/v1/users/{uid}/permissions` - List user permissions
- `POST /api/v1/users/{uid}/permissions` - Add user permission
- `DELETE /api/v1/users/{uid}/permissions/{permission_uid}` - Remove user permission

### Missions
- `GET /api/v1/missions/` - List all missions
- `GET /api/v1/missions/{slug}` - Get mission by slug
- `POST /api/v1/missions/` - Create new mission
- `PATCH /api/v1/missions/{slug}` - Update mission
- `DELETE /api/v1/missions/{slug}` - Delete mission

### Communities
- `GET /api/v1/communities/` - List all communities
- `GET /api/v1/communities/{slug}` - Get community by slug
- `POST /api/v1/communities/` - Create new community
- `PATCH /api/v1/communities/{slug}` - Update community
- `DELETE /api/v1/communities/{slug}` - Delete community

### Notifications
- `GET /api/v1/notifications/` - List notifications for authenticated user
- `GET /api/v1/notifications/{uid}` - Get notification by UID
- `PATCH /api/v1/notifications/{uid}/read` - Mark notification as read
- `DELETE /api/v1/notifications/{uid}` - Delete notification

## Models

The Django backend includes the following models:

1. **Community** - Represents organizations/clans
2. **User** - User accounts linked to Steam IDs
3. **Permission** - User permissions
4. **Mission** - Mission/event management
5. **MissionSlotGroup** - Slot groups within missions
6. **MissionSlot** - Individual slots in slot groups
7. **MissionSlotRegistration** - User registrations for slots
8. **MissionSlotTemplate** - Reusable slot templates
9. **MissionAccess** - Access control for missions
10. **CommunityApplication** - Applications to join communities
11. **Notification** - User notifications

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in environment variables
2. Configure `ALLOWED_HOSTS` with your domain
3. Use a production-grade WSGI server like Gunicorn:
```bash
gunicorn slotlist_backend.wsgi:application
```

4. Set up a reverse proxy (nginx/traefik) for SSL termination
5. Configure static files serving
6. Set up database backups
7. Configure Sentry for error tracking

## Migration from Original Backend

The database schema is designed to be compatible with the existing PostgreSQL database. To migrate:

1. Ensure the database connection settings match your existing database
2. Run Django migrations to create any missing tables/columns
3. The existing data should remain intact

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Admin
The Django admin interface is available at `http://localhost:8000/admin/`

## Architecture

The backend follows a clean architecture pattern:

- **Models** (`api/models.py`): Django ORM models
- **Schemas** (`api/schemas.py`): Pydantic schemas for request/response validation
- **Auth** (`api/auth.py`): JWT authentication and permission utilities
- **Routers** (`api/routers/`): API endpoint handlers organized by resource
- **API** (`api/api.py`): Main Django Ninja API configuration

## Key Differences from Original Backend

1. **Framework**: Django Ninja instead of Hapi.js
2. **ORM**: Django ORM instead of Sequelize
3. **Validation**: Pydantic schemas instead of Joi
4. **Documentation**: Automatic OpenAPI/Swagger documentation
5. **Admin Interface**: Built-in Django admin panel

## License

MIT
