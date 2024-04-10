# trackcase-service
Provides backend services for track-case
Create and manage app users
Create and manage clients, cases, maintain calendars, track collections, etc
Uses python, fastapi, sqlalchemy, alembic, postgresql
Frontend app is provided by: https://github.com/bibekaryal86/trackcase-spa

* make changes to models, then run pip install (because it uses python module imports)
  * `pip install .`
* create migrations:
  * `alembic revision --autogenerate -m COMMIT_MESSAGE`
* run migrations:
  * `alembic upgrade head`
* revert one migration:
  * `alembic downgrade -1`
* run as module
  * python -m src.trackcase_service.main
