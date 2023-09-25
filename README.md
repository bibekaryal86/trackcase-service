# trackcase-service
backend service for trackcase

* create migrations:
  * `alembic revision --autogenerate -m COMMIT_MESSAGE`
* run migrations:
  * `alembic upgrade head`
* error during run migrations:
  * ibm_db_alembic is really old, so kept encountering this error:
    *       File "<<PROJECT_HOME>>\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1408, in execute
                meth = statement._execute_on_connection
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                AttributeError: 'str' object has no attribute '_execute_on_connection'
    * Added the following lines of code to site-packages\sqlalchemy\engine\base.py to resolve, at least locally 
      *     if isinstance(statement, str):
                import sqlalchemy
                statement = sqlalchemy.text(statement)
    * If needed, the exact location of where to update will be where the error was thrown


* don't allow deleting form, case, anything
  * allow status of deleted
* case status tied with form status and collections
  * case complete when all forms complete
  * case complete when all collections balance zero


* add check to make sure coming from authenv_service
* pydantic says `from_orm` is deprecated



* run as module
  * python -m src.trackcase_service.main