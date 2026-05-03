# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack SaaS starter template with:

- **Backend**: Python Flask API (`/api`)
- **Frontend**: SvelteKit + Tailwind CSS (`/frontend`)
- **Mobile**: Capacitor for iOS/Android (configured in frontend)
- **Database**: MongoDB (primary) with optional PostgreSQL via SQLAlchemy
- **Payments**: Stripe integration
- **Auth**: Email/password + Google OAuth

## Commands

### Frontend (`/frontend`)

```bash
npm run dev              # Vite dev server on port 5173
npm run dev-lan          # LAN-accessible dev server
npm run build            # Production build
npm run build-staging    # Staging build
npm run build-capacitor  # Build and sync mobile
npm run run-android      # Run on Android
npm run run-ios          # Run on iOS
```

### Backend (`/api`)

```bash
python api.py            # Flask dev server on port 5005
```

### Docker (project root)

```bash
docker-compose up        # Start API + Frontend + MongoDB
```

### Database Migrations (Flask-Migrate/Alembic)

```bash
flask db migrate -m "description"
flask db upgrade
```

## Architecture

### Backend Blueprint Structure

Flask uses a blueprint-per-feature pattern registered in `api/app/__init__.py`:

- `mongo/api_token_auth` — signup, signin, signout, password reset, Google OAuth
- `mongo/admin` — admin dashboard
- `api` — core API endpoints (`blueprints/api/routes.py`)
- `payments_stripe` — Stripe webhook handlers
- `email` — transactional email
- `ai` — OpenAI integration
- `settings` — user account settings
- `subscription` — subscription plan management

**Database**: Dual support — MongoEngine (MongoDB) for primary auth/user data; SQLAlchemy for optional SQL models. Dev uses SQLite; production uses PostgreSQL/MongoDB.

**Auth**: Token-based API auth stored in MongoDB. Tokens are blacklisted on logout. `api/config.py` maps environments (`development`, `docker-development`, `staging`, `production`).

**Notable**: A `time.sleep(0.25)` exists before request handling middleware — intentional delay.

### Frontend Structure

SvelteKit with `@sveltejs/adapter-static` (fully prerendered SSG — no SSR):

- `src/routes/` — file-based routing; `+layout.svelte` handles auth guards and nav
- `src/components/slg/` — internal reusable component library
- `src/stores/` — Svelte stores: `auth.js` (user state), `settings.js`, `localStorage.js`
- `src/config/` — frontend configuration constants

**Tailwind** is configured with dark mode and custom `primary`/`secondary`/`tertiary` color scales.

### Multi-Environment Config

`api/config.py` contains all environment configs. Template variables like `schedulr.ai`, `life-organizer`, `schedulr`, `127.0.0.1` are replaced by `scripts/initialization/find-and-replace` during project setup.

If you see `|UPDATE_ME|` strings in code, those require manual updates specific to the deployment.

### CI/CD

- **Staging**: Auto-deploys on GitHub release publish (`.github/workflows/push-to-staging.yml`)
- **Production**: Manual dispatch only (`.github/workflows/deploy_to_production.yml`)
- Deploys via SSH + Docker Hub for frontend, SSH + pip/systemd for backend

### Ports

- API dev: `5005`
- Frontend dev: `5173`
- API production: `5002`
- Frontend production: `%%PROD_FRONTEND_PORT%%` (template variable)

## Context Directory (`/context`)

The `/context` directory is the source of truth for existing functions, routes, and components:

- `context/frontend_lib.js` — all function signatures from `frontend/src/lib/`
- `context/frontend_routes.js` — all frontend SvelteKit routes and their inline function signatures
- `context/api_routes.py` — all Flask blueprint routes and function signatures
- `context/slg_components.js` — all component signatures from `frontend/src/components/slg/`
- `context/slg_lib.js` — all utility function signatures from `frontend/src/components/slg/lib/`
- `context/components.js` — all component signatures from `frontend/src/components/` (excluding slg)
- `context/stores.js` — all Svelte store exports from `frontend/src/stores/`
- `context/api_helpers.py` — all helper, service, and model signatures from `api/app/blueprints/`

Each context file begins with a `// location:` (or `# location:`) comment indicating where to import from or add new code.

**Workflow:**

1. Check the relevant context file to see if what you need already exists.
2. If not found, assume it does not exist — do NOT search the project for it.
3. Implement the needed functionality.
4. Append the new signature(s) to the relevant context file.

When creating a new context file, always include a location header as the first line.

## Adding a New API Blueprint

1. Use `api/app/blueprints/example` as the template.
2. Register it in `api/app/__init__.py`:

```python
from app.blueprints.example import bp as example_bp
app.register_blueprint(example_bp)
```

3. Append new route signatures to `context/api_routes.py`.

## Adding a New Frontend Route

1. Use `frontend/src/routes/example` as the template.
2. Use slug-based nested paths where appropriate (e.g. `items/[id]`).
3. Decompose into focused components — prefer many small components over few large ones.
4. Generic/reusable components must come from `frontend/src/components/slg/`. If one doesn't exist there yet, add it there. Only route-specific custom components belong in the route directory.
5. Append new route/function signatures to `context/frontend_routes.js`.
6. Append any new component signatures to `context/components.js` (custom) or `context/slg_components.js` (generic).
