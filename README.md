# PLUTO

[![codecov](https://codecov.io/gh/jotaherrera/pluto/graph/badge.svg?token=SVQQKD8WRP)](https://codecov.io/gh/jotaherrera/pluto)

Managing personal finances through a REST API. Backend built with FastAPI and PostgreSQL: JWT auth, RBAC, Alembic migrations, and separate DB roles (owner vs runtime), orchestrated with Docker.

## Features

- REST API with FastAPI
- JWT authentication and authorization
- Role-based access control
- Schema migrations with Alembic
- Separate Postgres roles (owner for DDL, app_user for DML)
- Docker Compose for local Postgres

## Prerequisites

- **Python 3.13**
- **[uv](https://docs.astral.sh/uv/)** – Python package and project manager
- **Docker** and **Docker Compose** – for running Postgres
- **envsubst** – for generating bootstrap SQL (often from the `gettext` package; on macOS: `brew install gettext` and ensure it’s on your `PATH`)

## Environment variables

Create a `.env` file in the project root. Required (and optional) variables:

| Variable                       | Description                                          |
| ------------------------------ | ---------------------------------------------------- |
| `DATABASE__PASSWORD`           | Postgres superuser password (used by Docker Compose) |
| `DATABASE__PORT`               | Port exposed for Postgres (e.g. `5432`)              |
| `DATABASE__APP_OWNER_PASSWORD` | Password for DB role `app_owner` (migrations)        |
| `DATABASE__APP_USER_PASSWORD`  | Password for DB role `app_user` (API runtime)        |
| `DATABASE__USER`               | User the API uses to connect (e.g. `app_user`)       |
| `APP__JWT_SECRET`              | Secret for signing JWT tokens                        |

## Running the app

Use the project script to bring up the database (bootstrap and migrations run on first start) and start the API:

```bash
./pluto up
```

Development mode (with reload):

```bash
./pluto up --dev
```

Other commands:

- `./pluto down` – stop and remove the DB container
- `./pluto reset [--dev]` – down then up (fresh start)

API docs (Swagger UI): **[/docs](http://localhost:8000/docs)** once the server is running.

## Users and roles

- **Application roles**: `admin` and `user`.
- **Admin** (the superuser from the seeders): for managing users and seeing all of them. You define it via env: `SUPER_USER_EMAIL`, `SUPER_USER_PASSWORD`, `SUPER_USER_NAME`, `SUPER_USER_LAST_NAME`.
- **User**: for normal use; each user only sees and works with their own data.

## Database users (Postgres)

These are DB roles, not app roles:

- **postgres** – Used by Docker Compose; superuser of the cluster.
- **app_owner** – Used for migrations (DDL: create tables, etc.). Set `DATABASE__USER=app_owner` when running `alembic upgrade head`.
- **app_user** – Used by the API at runtime (DML only). The app connects with this user in production so it cannot alter schema.
