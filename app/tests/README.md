# Test Suite for AMR Control & Monitoring Web Application

This directory contains automated tests for the backend and business logic of the AMR Control & Monitoring Web Application. The tests use `pytest` and Flask's test client for fast, reliable testing.

## How to Run All Tests

From the project root, run:

```bash
PYTHONPATH=. pytest app/tests
```

## Test File Overview

- **test_db.py**: Tests database initialization, user creation, and basic queries.
- **test_login.py**: Tests login success and failure scenarios.
- **test_logout.py**: Tests logout and session clearing.
- **test_publish.py**: Tests the `/publish` endpoint for MQTT message publishing (requires admin session).
- **test_routes.py**: Tests that protected routes redirect or allow access based on login/session state.
- **test_simple_rbac.py**: Tests role-based access control (RBAC) for different user roles and endpoints.
- **test_complete_rbac.py**: Comprehensive RBAC and feature access tests for all user roles.
- **test_numeric_levels.py**: Tests numeric level conversion logic for package delivery and MQTT payloads.

## Notes

- All tests are self-contained and do not require a running server; they use Flask's test client.
- The `__pycache__/` directory contains Python bytecode and can be ignored.
- For integration or end-to-end tests, see the main README for additional instructions.

---

For more details on the backend and app structure, see the main [README.md](../../README.md).
