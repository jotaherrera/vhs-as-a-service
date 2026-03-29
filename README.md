# vhs-as-a-service

[![codecov](https://codecov.io/gh/jotaherrera/vhs-as-a-service/graph/badge.svg?token=SVQQKD8WRP)](https://codecov.io/gh/jotaherrera/vhs-as-a-service)

A 90s video rental store REST API. Built with FastAPI + PostgreSQL.

## Features

- REST API with FastAPI
- JWT authentication and authorization
- Role-based access control
- Database migrations with Alembic
- Docker Compose for local development

## Prerequisites

- **Python 3.13**
- **[uv](https://docs.astral.sh/uv/)** – Python package and project manager
- **Docker** and **Docker Compose**

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
| `DATABASE__PASSWORD` | Postgres password | Yes |
| `DATABASE__PORT` | Postgres port (e.g. `5432`) | Yes |
| `DATABASE__USER` | Database user | Yes |
| `APP__JWT_SECRET` | Secret key for JWT tokens | Yes |

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
