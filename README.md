# trackcase-service
backend service for trackcase

* make changes to models, then run pip install (because it uses python module imports)
  * `pip install .`
* create migrations:
  * `alembic revision --autogenerate -m COMMIT_MESSAGE`
* run migrations:
  * `alembic upgrade head`
* run as module
  * python -m src.trackcase_service.main
* For History and Notes
  * To retrieve history, use the `find_one` endpoint with `is_include_history=True`
  * To retrieve notes, use the `find_one` endpoint, notes are always included

* deleting is not allowed, set status of inactive/closed/retired etc
* case status tied with form status and collections
  * case complete when all forms complete
  * case complete when all collections balance zero
  * case can't be closed/inactive etc if forms pending, give option to close it all
    * still need to put blocker to reconcile cash/case collection

* TODO
  * Add Notes API one for all
    * this will add notes only

testing without from_attributes=True in schema, don't think needed because all converting manually
