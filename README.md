# trackcase-service
backend service for trackcase

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
* For History
  * To retrieve history, use the `find_one` endpoint with `is_include_history=True`

# add user email validation (use python magic link???)
