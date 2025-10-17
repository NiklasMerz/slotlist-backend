# Slotlist Backend - Monorepo

This repository contains both the legacy TypeScript/Hapi.js backend and the new Django/Django Ninja backend for slotlist.info.

## Repository Structure

```
slotlist-backend/
├── legacy/              # Original TypeScript/Hapi.js backend (Node.js)
│   ├── src/            # TypeScript source code
│   ├── package.json    # Node.js dependencies
│   └── ...             # Legacy configuration files
│
├── rewrite/            # New Django/Django Ninja backend (Python)
│   ├── api/            # Django application
│   ├── manage.py       # Django management script
│   ├── requirements.txt # Python dependencies
│   ├── docker-compose.yml # Docker setup for Django + PostgreSQL
│   └── ...             # Django configuration files
│
└── README.md           # This file
```

## Quick Start

### Django Backend (Recommended)

The new Django backend is located in the `rewrite/` directory.

```bash
cd rewrite
docker-compose up
```

The API will be available at http://localhost:8000/api/

**Documentation:**
- Full setup guide: [rewrite/README.md](rewrite/README.md)
- Steam OAuth guide: [rewrite/STEAM_OAUTH.md](rewrite/STEAM_OAUTH.md)
- Database schema: [rewrite/DATABASE_SCHEMA.md](rewrite/DATABASE_SCHEMA.md)

### Legacy Backend (TypeScript/Hapi.js)

The original TypeScript backend is in the `legacy/` directory for reference.

```bash
cd legacy
yarn install
yarn dev
```

**Note:** The legacy backend is maintained for reference but the Django backend is recommended for new deployments.

## Features Comparison

| Feature | Legacy (TypeScript) | Django Rewrite |
|---------|-------------------|----------------|
| Framework | Hapi.js | Django + Django Ninja |
| Language | TypeScript | Python 3.9+ |
| ORM | Sequelize | Django ORM |
| API Docs | Swagger (hapi-swagger) | OpenAPI (Django Ninja) |
| Authentication | JWT + Steam OpenID | JWT + Steam OpenID |
| Database | PostgreSQL | PostgreSQL |
| Database Schema | Original | 100% Compatible |
| Docker Support | ✅ | ✅ |
| Version | 1.2.x | 1.0.0 (rewrite) |

## Migration Guide

The Django backend is designed as a **drop-in replacement** for the TypeScript backend:

1. Both backends use the **same database schema**
2. Both backends use the **same authentication flow**
3. Both backends expose **compatible API endpoints**

To migrate:
1. Point the Django backend to your existing PostgreSQL database
2. Configure Steam API key
3. Test endpoints with your frontend
4. Switch traffic to Django backend

See [rewrite/DATABASE_SCHEMA.md](rewrite/DATABASE_SCHEMA.md) for detailed compatibility information.

## Development

### Django Backend

```bash
cd rewrite

# Using Docker (Recommended)
docker-compose up

# Or manually
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Legacy Backend

```bash
cd legacy

# Install dependencies
yarn install

# Development
yarn dev

# Production
yarn build
yarn start
```

## API Documentation

### Django Backend
- Interactive API docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI schema: http://localhost:8000/api/openapi.json

### Legacy Backend
- Swagger UI: http://localhost:3000/documentation

## Configuration

### Django Backend
Configuration via environment variables (`.env` file):
- Database credentials
- JWT secrets
- Steam API key
- Debug settings

See [rewrite/.env.example](rewrite/.env.example) for all options.

### Legacy Backend
Configuration via environment variables:
- `DB_*` - Database settings
- `CONFIG_JWT_*` - JWT configuration
- `CONFIG_STEAM_*` - Steam API settings

See [legacy/dev.env](legacy/dev.env) for all options.

## Testing

### Django Backend
```bash
cd rewrite
python manage.py test
```

### Legacy Backend
```bash
cd legacy
yarn test
```

## Deployment

### Django Backend with Docker

```bash
cd rewrite
docker-compose up -d
```

For production deployment, see [rewrite/README.md](rewrite/README.md).

### Legacy Backend

See legacy backend documentation for deployment instructions.

## Contributing

New features should be added to the Django backend in the `rewrite/` directory. The legacy backend is in maintenance mode.

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Django backend: Create an issue with `[Django]` prefix
- Legacy backend: Create an issue with `[Legacy]` prefix
