# vhs-as-a-service

[![codecov](https://codecov.io/gh/jotaherrera/vhs-as-a-service/graph/badge.svg?token=SVQQKD8WRP)](https://codecov.io/gh/jotaherrera/vhs-as-a-service)

A REST API for managing personal finances, built with FastAPI and secure database architecture.

## Features

- REST API with FastAPI
- JWT authentication and authorization
- Role-based access control
- Database migrations with Alembic
- Separate Postgres roles for DDL and DML operations
- Docker Compose for local development

## Prerequisites

- **Python 3.13**
- **[uv](https://docs.astral.sh/uv/)** – Python package and project manager
- **Docker** and **Docker Compose**
- **envsubst** – for SQL templating (macOS: `brew install gettext`)

## Quick Start

1. Create a `.env` file (see Environment Variables below)
2. Start the application:
```bash
./vhsaas up
```

Development mode with hot reload:
```bash
./vhsaas up --dev
```

API documentation: **http://localhost:8000/docs**

## Environment Variables

Create a `.env` file in the project root:

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE__PASSWORD` | Postgres superuser password | Yes |
| `DATABASE__PORT` | Postgres port (e.g. `5432`) | Yes |
| `DATABASE__APP_OWNER_PASSWORD` | Password for `app_owner` role | Yes |
| `DATABASE__APP_USER_PASSWORD` | Password for `app_user` role | Yes |
| `DATABASE__USER` | Runtime database user | Yes |
| `DATABASE__MIGRATION_USER` | User for migrations (e.g. `app_owner`) | No |
| `DATABASE__MIGRATION_PASSWORD` | Password for migration user | No |
| `APP__JWT_SECRET` | Secret key for JWT tokens | Yes |
| `SUPER_USER_EMAIL` | Admin email (default: `admin@email.com`) | No |
| `SUPER_USER_PASSWORD` | Admin password (default: `012345678`) | No |
| `SUPER_USER_NAME` | Admin first name (default: `Admin`) | No |
| `SUPER_USER_LAST_NAME` | Admin last name (default: `User`) | No |

## Available Commands

### App
- `./vhsaas up` – Start database and API
- `./vhsaas up --dev` – Start with hot reload
- `./vhsaas down` – Stop and remove containers
- `./vhsaas reset [--dev]` – Clean restart

### Dev
- `uv run pytest` – Run tests
- `uv run ruff format --check && uv run ruff check` – Lint
- `uv run ty check .` – Type check

## Architecture

### Application Roles

- **Admin**: Full access including user management
- **User**: Access limited to own data

### Database Users

- **app_owner** – Used for schema migrations (DDL)
- **app_user** – Used by API at runtime (DML)
