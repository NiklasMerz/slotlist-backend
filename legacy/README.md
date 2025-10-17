# Slotlist Backend - Legacy (TypeScript/Hapi.js)

This directory contains the original TypeScript/Hapi.js backend for slotlist.info.

**⚠️ Note:** This is the legacy backend maintained for reference. For new deployments, please use the Django backend in the `../rewrite/` directory.

## Overview

- **Framework:** Hapi.js (Node.js)
- **Language:** TypeScript
- **ORM:** Sequelize
- **Database:** PostgreSQL
- **Authentication:** JWT + Steam OpenID

## Quick Start

### Development

```bash
# Install dependencies
yarn install

# Run development server
yarn dev
```

The API will be available at http://localhost:3000

### Production

```bash
# Install dependencies
yarn install

# Build TypeScript
yarn build

# Run production server
yarn start
```

## Docker

```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.legacy.yml up
```

## API Documentation

Swagger documentation is available at:
- http://localhost:3000/documentation

## Configuration

Create a `.env` file based on `dev.env`:

```env
# Database
DB_DATABASE=slotlist
DB_USERNAME=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# JWT
CONFIG_JWT_SECRET=your-jwt-secret
CONFIG_JWT_ISSUER=https://slotlist.info
CONFIG_JWT_AUDIENCE=https://slotlist.info

# Steam API
CONFIG_STEAM_API_SECRET=your-steam-api-key
CONFIG_STEAM_OPENID_CALLBACK_URL=https://slotlist.info/auth/callback
CONFIG_STEAM_OPENID_REALM=https://slotlist.info
```

## Database Migrations

```bash
# Run migrations
yarn migrate

# Revert last migration
yarn migrate:undo
```

## Project Structure

```
legacy/
├── src/
│   ├── api/              # API routes and controllers
│   ├── shared/
│   │   ├── models/      # Sequelize models
│   │   ├── migrations/  # Database migrations
│   │   ├── services/    # Business logic
│   │   └── util/        # Utilities
│   └── server.ts        # Server entry point
├── package.json
├── tsconfig.json
└── ...
```

## Testing

```bash
# Run tests
yarn test

# Run tests with coverage
yarn test:coverage
```

## Migration to Django

If you're migrating from this legacy backend to the Django rewrite:

1. **Database:** Both backends use the same schema - no database migration needed
2. **Authentication:** Steam OpenID flow is compatible
3. **API:** Endpoints are designed to be compatible

See [../rewrite/README.md](../rewrite/README.md) for the Django backend documentation.

## Troubleshooting

### Database Connection Issues

Ensure PostgreSQL is running and credentials in `.env` are correct:
```bash
psql -U postgres -h localhost
```

### TypeScript Build Errors

Clear build cache and rebuild:
```bash
yarn clean
yarn build
```

### Port Already in Use

Check if another process is using port 3000:
```bash
lsof -i :3000
```

## Maintenance Status

This backend is in **maintenance mode**:
- ✅ Bug fixes will be applied
- ✅ Security updates will be applied
- ❌ New features should be added to Django backend
- ❌ Major refactoring is not planned

## Support

For issues with the legacy backend, create an issue with the `[Legacy]` prefix.

For new deployments, we recommend using the Django backend in `../rewrite/`.
