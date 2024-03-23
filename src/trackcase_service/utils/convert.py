from datetime import datetime
from decimal import Decimal

from pydantic.fields import FieldInfo


def _get_default_value(field: FieldInfo):
    field_type_name = field.annotation.__name__
    if field.is_required():
        if field_type_name == "str":
            return ""
        elif field_type_name == "int":
            return 0
        elif field_type_name == "datetime":
            return datetime.now()
        elif field_type_name == "Decimal":
            return Decimal("0.00")
        elif field_type_name == "list":
            return []
        elif field_type_name == "bool":
            return False
    return field.default


# this is required because Pydantic doesn't allow creating empty instance
# so create an instance with default empty values according to type
def create_default_schema_instance(destination_class):
    fields = destination_class.__fields__
    required_fields = {
        name: _get_default_value(field) for name, field in fields.items()
    }
    destination_object = destination_class(**required_fields)
    return destination_object


def _copy_objects(
    source_object,
    destination_class,
    destination_object=None,
    is_copy_all=False,
    exclusions=None,
):
    if exclusions is None:
        exclusions = []
    if source_object is None:
        return None
    if destination_object is None:
        destination_object = create_default_schema_instance(destination_class)
    common_attributes = set(dir(source_object)) & set(dir(destination_object))
    for attr in common_attributes:
        if (
            not callable(getattr(source_object, attr))
            and not attr.startswith("_")
            and attr not in exclusions
            and (is_copy_all or not getattr(destination_object, attr))
        ):
            value = getattr(source_object, attr)
            if value and isinstance(value, str):
                setattr(destination_object, attr, value.strip().upper())
            elif isinstance(value, bool) and value is not None:
                setattr(destination_object, attr, value)
            elif value:
                setattr(destination_object, attr, value)
            else:
                setattr(destination_object, attr, None)
    return destination_object


def convert_schema_to_model(
    request_schema,
    model_class,
    app_user_id=None,
    history_object_id_key=None,
    history_object_id_value=None,
):
    data_model = _copy_objects(request_schema, model_class, model_class())
    if history_object_id_key and history_object_id_value:
        setattr(data_model, "app_user_id", app_user_id)
        setattr(data_model, history_object_id_key, history_object_id_value)
    return data_model


def convert_model_to_schema(
    data_model,
    schema_class,
    is_include_extra: bool = False,
    is_include_history: bool = False,
    exclusions=None,
    extra_to_include=None,
    history_to_include=None,
):
    if extra_to_include is None:
        extra_to_include = []
    if history_to_include is None:
        history_to_include = []
    data_schema = _copy_objects(
        data_model, schema_class, is_copy_all=True, exclusions=exclusions
    )
    if is_include_extra and extra_to_include:
        for extra in extra_to_include:
            setattr(data_schema, extra, getattr(data_model, extra))
    if is_include_history and history_to_include:
        for history in history_to_include:
            setattr(data_schema, history, getattr(data_model, history))
    return data_schema


def convert_data_model_to_schema(data_model, schema_class, exclusions=None):
    return _copy_objects(
        data_model, schema_class, is_copy_all=True, exclusions=exclusions
    )
