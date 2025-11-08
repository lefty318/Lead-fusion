# Database Migrations with Alembic

This project uses Alembic for database migrations instead of `Base.metadata.create_all()`.

## Initial Setup

1. Make sure your database is running and configured in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost/omnilead
   ```

2. Create your first migration:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Initial migration"
   ```

3. Review the generated migration file in `alembic/versions/` to ensure it's correct.

4. Apply the migration:
   ```bash
   alembic upgrade head
   ```

## Common Commands

- **Create a new migration**: `alembic revision --autogenerate -m "Description"`
- **Apply migrations**: `alembic upgrade head`
- **Rollback one migration**: `alembic downgrade -1`
- **Rollback to specific revision**: `alembic downgrade <revision_id>`
- **View current revision**: `alembic current`
- **View migration history**: `alembic history`

## Migration Workflow

1. Make changes to your models in `app/models/`
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Review the generated migration file
4. Apply: `alembic upgrade head`

## Important Notes

- Always review auto-generated migrations before applying them
- Never edit existing migration files that have been applied to production
- Test migrations on a development database first
- Keep migrations small and focused on specific changes

