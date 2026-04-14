# Database Migrations

Migrations are managed with [Alembic](https://alembic.sqlalchemy.org/). The DB must be running before any `alembic` command.

## Standard workflow

### Adding a new model or changing an existing one

1. Edit or create the model in `app/models/`
2. Generate the migration:
   ```bash
   uv run alembic revision --autogenerate -m "describe the change"
   ```
3. Apply it:
   ```bash
   uv run alembic upgrade head
   ```

---

## Regenerating migrations from scratch

Use this when you need a clean slate (e.g. during early development).

1. Tear down the DB and delete all migration files:
   ```bash
   docker compose down -v
   rm app/database/alembic/versions/*.py
   ```

2. Start a fresh DB and wait for it to be healthy:
   ```bash
   docker compose up -d
   ```

3. Stamp Alembic as base (clears any recorded revision):
   ```bash
   uv run alembic stamp base
   ```

4. Autogenerate a new initial migration:
   ```bash
   uv run alembic revision --autogenerate -m "initial schema"
   ```

5. Apply it and run seeders:
   ```bash
   uv run alembic upgrade head
   uv run python -m app.database.bootstrap.seed
   ```

Or just run `./vhsaas reset`, which handles steps 2–5 automatically on a fresh volume.

---

## Useful commands

| Command | Description |
|---|---|
| `uv run alembic upgrade head` | Apply all pending migrations |
| `uv run alembic downgrade base` | Roll back all migrations |
| `uv run alembic current` | Show the current applied revision |
| `uv run alembic history` | List all migrations |
| `uv run alembic stamp base` | Mark DB as having no migrations applied |
