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

* don't allow deleting form, case, anything
  * allow status of deleted
* case status tied with form status and collections
  * case complete when all forms complete
  * case complete when all collections balance zero

* TODO
  * History API one for all, just read history, no put/post/delete
  * Add Notes API one for all
    * for notes api and history api, create an ENUM of table names and then use switch/case

testing without from_attributes=True in schema, don't think needed because all converting manually
