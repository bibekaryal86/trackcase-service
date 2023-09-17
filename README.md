# trackcase-service
backend service for trackcase

* create migrations:
  * `alembic revision --autogenerate -m COMMIT_MESSAGE`
* run migrations:
  * `alembic upgrade head
* error during run migrations:
  * ibm_db_alembic is really old, so kept encountering this error:
    * `AttributeError: 'str' object has no attribute '_execute_on_connection'`at site-packages\sqlalchemy\engine\base.py, line 1408
    * Added the following lines of code to site-packages\sqlalchemy\engine\base.py to resolve, at least locally
          if isinstance(statement, str):
              import sqlalchemy
              statement = sqlalchemy.text(statement)
    * If needed, the exact location of where to update will be where the error was thrown
