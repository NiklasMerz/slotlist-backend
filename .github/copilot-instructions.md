# Copilot Instructions for slotlist-backend

## Project Overview
This is the backend for slotlist.info, an ArmA 3 mission planning and slotlist management tool. The project is written in TypeScript and uses Node.js with a Hapi.js web framework, PostgreSQL database, and Sequelize ORM.

**Note:** This project has been discontinued and is no longer actively maintained. It remains as an archive for historical and reference purposes.

## Technology Stack
- **Runtime:** Node.js 8.1.4 (legacy version)
- **Language:** TypeScript 2.3.3 with strict compiler options
- **Web Framework:** Hapi.js v16
- **Database:** PostgreSQL 9.6+
- **ORM:** Sequelize v4 with decorators
- **Authentication:** JWT (hapi-auth-jwt2) and OpenID (Steam integration)
- **Logging:** Bunyan with Google Cloud Logging integration
- **Storage:** Google Cloud Storage
- **Deployment:** Docker, Kubernetes (Google Cloud Platform)

## Code Style & Standards

### TypeScript Configuration
- Strict mode is enabled with all strict checks
- Experimental decorators are enabled for Sequelize models
- Target is ES6 with CommonJS modules
- All code must have explicit type annotations (see `typedef` rule in tslint.json)
- No implicit any, this, or returns allowed

### Linting
- Uses TSLint with Microsoft contrib rules
- Max line length: 180 characters
- Max function body length: 125 lines
- Arrow parameters, call signatures, and property declarations must have type annotations

### Code Organization
- **`src/api/`** - API routes and controllers
- **`src/shared/`** - Shared utilities and models
- **`src/test/`** - Test files
- **`dist/src/`** - Transpiled JavaScript output

## Development Workflow

### Building
```bash
yarn build      # Transpile TypeScript to JavaScript
```

### Running
```bash
yarn start           # Start with formatted logs (bunyan)
yarn start:docker    # Start with raw JSON logs
docker-compose up    # Run with Docker (includes PostgreSQL)
```

### Database Migrations
```bash
yarn migrate    # Run database migrations using Umzug
```

### Testing
```bash
yarn test       # Run Mocha tests (limited test coverage exists)
```

## Key Architecture Patterns

### Authentication
- Uses JWT tokens for API authentication
- Steam OpenID integration for user login
- Token validation via hapi-auth-jwt2 plugin

### Database Models
- Uses Sequelize with decorators (`sequelize-decorators`)
- Models should use TypeScript decorators for columns and relationships
- Transaction support via continuation-local-storage

### API Design
- RESTful API endpoints
- Joi for request validation
- Boom for error responses
- Hapi-swagger for API documentation

### Logging
- Structured logging with Bunyan
- Google Cloud Logging integration for production
- Request/response logging via good-bunyan plugin

### Cloud Integration
- Google Cloud Storage for file uploads
- Environment-based configuration (see `dev.env`)

## Important Conventions

### Configuration
- Environment variables are the primary configuration method
- Required variables are documented in `dev.env`
- Create a `.env` file (gitignored) for local overrides
- Key required variables:
  - `CONFIG_STEAM_API_SECRET`
  - `CONFIG_STORAGE_BUCKETNAME`
  - `CONFIG_STORAGE_PROJECTID`
  - `CONFIG_JWT_SECRET`
  - `DEFAULT_ADMIN_STEAMID`
  - `DEFAULT_ADMIN_NICKNAME`

### Error Handling
- Use Boom for HTTP errors
- Integrate with Sentry (Raven) for error tracking
- Proper error logging with Bunyan context

### Security
- CSP/HPKP headers are configured (review before deploying elsewhere)
- JWT secret must be properly configured
- Run behind reverse proxy for SSL termination

## Common Pitfalls

1. **Node Version:** This project requires Node 8.1.4 - newer versions may have compatibility issues
2. **TypeScript Strict Mode:** All code must satisfy strict type checking requirements
3. **Decorators:** Ensure decorators are properly imported from sequelize-decorators
4. **Environment Variables:** Missing required env vars will cause runtime failures
5. **Database Connection:** PostgreSQL must be running and properly configured
6. **Build Before Run:** Always transpile TypeScript before running (`yarn build`)

## Testing Guidelines

- Unit tests use Mocha
- Test coverage is limited (as of 2018-01-09)
- Test file location: `src/test/`
- Run tests after building: `yarn build && yarn test`

## Documentation

- Configuration details: `docs/Configuration.md`
- Contributors: `docs/Contributors.md`
- Additional docs in `docs/` folder

## Deployment Notes

- Designed for Kubernetes on Google Cloud Platform
- Kubernetes configs in `k8s/` directory
- Docker build config in `cloudbuild.yaml`
- Requires reverse proxy for SSL (nginx or traefik recommended)
- Review CSP/HPKP headers before deploying to custom domains

## Git Workflow

- Pull requests should target the `dev` branch
- Features are merged to `master` after testing
- Uses Semantic Versioning for releases
- Release tags follow `v*.*.*` format

## Additional Resources

- Frontend repository: [slotlist-frontend](https://github.com/MorpheusXAUT/slotlist-frontend)
- Translations: Managed via OneSky platform
- License: MIT
