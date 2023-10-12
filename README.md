# trackcase-service
backend service for trackcase

* create migrations:
  * `alembic revision --autogenerate -m COMMIT_MESSAGE`
* run migrations:
  * `alembic upgrade head`


* don't allow deleting form, case, anything
  * allow status of deleted
* case status tied with form status and collections
  * case complete when all forms complete
  * case complete when all collections balance zero


* add check to make sure coming from authenv_service
* pydantic says `from_orm` is deprecated



* run as module
  * python -m src.trackcase_service.main