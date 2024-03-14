import math
from datetime import datetime
from typing import Dict, List, NamedTuple, Type, TypeVar, Union

from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Query, Session

from src.trackcase_service.db.models import Base
from src.trackcase_service.service.schemas import (
    FilterConfig,
    FilterOperation,
    ResponseMetadata,
    SortConfig,
    SortDirection,
)

ModelBase = TypeVar("ModelBase", bound=Base)
DataKeys = NamedTuple("DataKeys", [("data", str), ("metadata", str)])


class CrudService:
    def __init__(self, db_session: Session, db_model: Type[ModelBase]):
        self.db_model = db_model
        self.db_session = db_session

    def create(self, model_data: ModelBase) -> ModelBase:
        setattr(model_data, "created", func.now())
        setattr(model_data, "modified", func.now())
        setattr(model_data, "is_deleted", False)
        self.db_session.add(model_data)
        self.db_session.commit()
        self.db_session.refresh(model_data)
        return model_data

    def read(
        self,
        model_id: int = None,
        model_ids: list[int] = None,
        sort_config: SortConfig = None,
        filter_config: List[FilterConfig] = None,
        page_number: int = 1,
        per_page: int = 100,
        is_include_soft_deleted: bool = False,
    ) -> Dict[str, Union[List[ModelBase], ResponseMetadata]]:
        if model_id and model_id > 0:
            query = self.db_session.query(self.db_model).filter(
                self.db_model.id == model_id
            )
            if not is_include_soft_deleted:
                query = query.filter(
                    self.db_model.is_deleted == False  # noqa: E501, E712
                )
            data = query.first()
            return {
                DataKeys.data: [data] if data else [],
                DataKeys.metadata: None,
            }
        elif model_ids and len(model_ids) > 0:
            query = self.db_session.query(self.db_model).filter(
                self.db_model.id.in_(model_ids)
            )
            if not is_include_soft_deleted:
                query = query.filter(
                    self.db_model.is_deleted == False  # noqa: E501, E712
                )
            data = query.all()
            return {
                DataKeys.data: data,
                DataKeys.metadata: None,
            }

        if per_page > 1000:
            per_page = 1000  # Cap per_page at 1000

        query: Query = self.db_session.query(self.db_model)

        if not is_include_soft_deleted:
            # Add filter to exclude deleted rows
            query = query.filter(
                getattr(self.db_model, "is_deleted") == False  # noqa: E501, E712
            )

        if filter_config:
            query = _apply_filters(self.db_model, query, filter_config)

        if sort_config:
            query = _apply_sort(self.db_model, query, sort_config)

        total_items = query.count()
        total_pages = math.ceil(total_items / per_page)
        paginated_query = query.offset((page_number - 1) * per_page).limit(per_page)

        data = paginated_query.all()
        metadata = ResponseMetadata(
            total_items=total_items,
            total_pages=total_pages,
            page_number=page_number,
            per_page=per_page,
        )

        return {
            DataKeys.data: data,
            DataKeys.metadata: metadata,
        }

    def update(self, model_id: int, model_data: ModelBase) -> ModelBase:
        db_record = self.db_session.query(self.db_model).get(model_id)
        # exists check done in controller/api for better messaging, so no need again
        db_record = _copy_key_values(model_data, db_record)
        setattr(db_record, "modified", func.now())
        self.db_session.commit()
        self.db_session.refresh(db_record)
        return db_record

    def delete(self, model_id: int, is_hard_delete: bool = False):
        db_record = self.db_session.query(self.db_model).get(model_id)
        # exists check done in controller/api for better messaging, so no need again
        if is_hard_delete:
            self.db_session.delete(db_record)
        else:
            setattr(db_record, "modified", func.now())
            setattr(db_record, "deleted_date", func.now())
            setattr(db_record, "is_deleted", True)
        self.db_session.commit()
        return True


def _copy_key_values(model_data, db_record):
    # Get a list of attributes for the db_record object
    db_attributes_and_types = {
        attr: type(getattr(db_record, attr))
        for attr in dir(db_record)
        if not callable(getattr(db_record, attr)) and not attr.startswith("_")
    }

    for attr_name, attr_type in db_attributes_and_types.items():
        attr_value = getattr(model_data, attr_name)
        if _is_should_set_attr_value(model_data, attr_name, attr_value, attr_type):
            setattr(db_record, attr_name, attr_value)
    return db_record


def _is_should_set_attr_value(model_data, attr_name, attr_value, attr_type) -> bool:
    auto_generated_attributes = [
        "id",
        "created",
        "modified",
        "is_deleted",
        "deleted_date",
        "metadata",
        "registry",
    ]
    if hasattr(model_data, attr_name):
        if attr_name not in auto_generated_attributes:
            if not isinstance(attr_value, list):
                if attr_value is None:
                    return attr_type == str or attr_type == int or attr_type == bool
                else:
                    return True
    return False


def _apply_filters(
    db_model: ModelBase, query: Query, filter_config: List[FilterConfig] = None
) -> Query:
    for filter_item in filter_config:
        column = filter_item.column
        value = filter_item.value
        operation = filter_item.operation
        query = _apply_filter(
            db_model, query, column, value, FilterOperation(operation)
        )
    return query


def _apply_filter(
    db_model: ModelBase,
    query: Query,
    column: str,
    value: Union[str, int, float, datetime],
    operation: FilterOperation,
) -> Query:
    column_attr = getattr(db_model, column)
    if operation == FilterOperation.EQUAL_TO:
        query = query.filter(column_attr == value)
    elif operation == FilterOperation.GREATER_THAN:
        query = query.filter(column_attr > value)
    elif operation == FilterOperation.LESS_THAN:
        query = query.filter(column_attr < value)
    elif operation == FilterOperation.GREATER_THAN_OR_EQUAL_TO:
        query = query.filter(column_attr >= value)
    elif operation == FilterOperation.LESS_THAN_OR_EQUAL_TO:
        query = query.filter(column_attr <= value)
    else:
        raise ValueError("Unsupported operation for filter")
    return query


def _apply_sort(db_model: ModelBase, query: Query, sort_config: SortConfig) -> Query:
    order_by_conditions = []
    if sort_config.direction == SortDirection.ASC:
        order_by_conditions.append(asc(getattr(db_model, sort_config.column)))
    elif sort_config.direction == SortDirection.DESC:
        order_by_conditions.append(desc(getattr(db_model, sort_config.column)))
    else:
        raise ValueError("Unsupported operation for sort")
    return query.order_by(*order_by_conditions)
