# Running Tests

This project uses pytest for testing.

## Setup

1. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Run tests with coverage:
   ```bash
   pytest --cov=app --cov-report=html
   ```

## Test Structure

- `tests/conftest.py` - Pytest fixtures and configuration
- `tests/test_auth.py` - Authentication endpoint tests
- Add more test files as needed following the same pattern

## Writing Tests

Tests use an in-memory SQLite database for speed and isolation. Each test gets a fresh database.

Example:
```python
def test_my_endpoint(client, test_user, auth_token):
    response = client.get(
        "/api/my-endpoint",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
```

## Fixtures Available

- `db` - Database session
- `client` - FastAPI test client
- `auth_service` - AuthService instance
- `test_user` - Pre-created test user
- `auth_token` - JWT token for test user

