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
* For History and Notes
  * To retrieve history, use the `find_one` endpoint with `is_include_history=True`
  * To retrieve notes, use the `find_one` endpoint, notes are always included

* do not let change status to inactive if dependents are still active
* deleting is not allowed, set status of inactive/closed/retired etc
* case status tied with form status and collections
  * case complete when all forms complete
  * case complete when all collections balance zero
* report of all court cases where all forms and other dependencies are done but still active

testing without from_attributes=True in schema, don't think needed because all converting manually
