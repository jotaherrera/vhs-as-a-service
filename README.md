# vhs-as-a-service

[![codecov](https://codecov.io/gh/jotaherrera/vhs-as-a-service/graph/badge.svg?token=SVQQKD8WRP)](https://codecov.io/gh/jotaherrera/vhs-as-a-service)

A 90s video rental store REST API. Built with FastAPI + PostgreSQL.

> I've never held a VHS tape in my life — so obviously I built an API to rent them out.

## Context

Imagine a chain of physical video rental stores where staff use a **mobile app** (Apple Store-style) to manage rentals, inventory, and customers right from the shop floor. Customers also have access to a **web app** where they can browse the catalog, check their rental history, and **reserve movies** for in-store pickup.

Both apps consume this same REST API.

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

All the following variables are required. Use `.env.test` as a reference.

| Variable | Description |
|----------|-------------|
| `APP__DEBUG` | Enable debug mode |
| `APP__JWT_SECRET` | Secret key for JWT tokens |
| `DATABASE__USER` | Database user |
| `DATABASE__PASSWORD` | Database password |
| `DATABASE__HOST` | Database host |
| `DATABASE__PORT` | Database port |

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

- **Admin** (store staff): Full access — manage rentals, inventory, and customers via the mobile app
- **User** (customer): Browse catalog, view own rental history, and reserve movies via the web app
