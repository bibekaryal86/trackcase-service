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

* advanced:
  * DELETING
    * deleting is not allowed in general, but set status of inactive/closed
      * instead of delete, the button should show CLOSE
      * do not let something to be marked as closed/finished until all the dependents are closed/finished
  * REPORTING
    * show all court cases that are pending
    * show all forms that are in progress
    * show all pending payments to be received
    * show all hearing/task calendars that are past due
      * but with active dependents
