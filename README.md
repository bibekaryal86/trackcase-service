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

# create a gateway within this app
# add a raw sql execution
# only superusers can edit user stuffs
# superusers, provide option to view soft deleted
# remove get_statuses() from constants
# ui, separate popup for password update

# docs, login to have basic security
# others to have Token
