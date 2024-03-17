# do not use lru-cache because the result differs per param
# and `request` param will be different
# this should suffice for now
from src.trackcase_service.service import schemas

COMPONENT_STATUSES_CACHE = []
COLLECTION_METHODS_CACHE = []
CASE_TYPES_CACHE = []
FILING_TYPES_CACHE = []
HEARING_TYPES_CACHE = []
TASK_TYPES_CACHE = []
APP_ROLES_CACHE = []
APP_PERMISSIONS_CACHE = []


def get_ref_types_cache(ref_type: schemas.RefTypesServiceRegistry):
    match ref_type:
        case schemas.RefTypesServiceRegistry.COMPONENT_STATUS:
            return COMPONENT_STATUSES_CACHE
        case schemas.RefTypesServiceRegistry.COLLECTION_METHOD:
            return COLLECTION_METHODS_CACHE
        case schemas.RefTypesServiceRegistry.CASE_TYPE:
            return CASE_TYPES_CACHE
        case schemas.RefTypesServiceRegistry.FILING_TYPE:
            return FILING_TYPES_CACHE
        case schemas.RefTypesServiceRegistry.HEARING_TYPE:
            return HEARING_TYPES_CACHE
        case schemas.RefTypesServiceRegistry.TASK_TYPE:
            return TASK_TYPES_CACHE
        case _:
            return []


def set_ref_types_cache(
    ref_type: schemas.RefTypesServiceRegistry,
    ref_types: (
        list[schemas.ComponentStatus]
        | list[schemas.CollectionMethod]
        | list[schemas.CaseType]
        | list[schemas.FilingType]
        | list[schemas.HearingType]
        | list[schemas.TaskType]
    ),
):
    match ref_type:
        case schemas.RefTypesServiceRegistry.COMPONENT_STATUS:
            COMPONENT_STATUSES_CACHE.clear()
            COMPONENT_STATUSES_CACHE.extend(ref_types)
        case schemas.RefTypesServiceRegistry.COLLECTION_METHOD:
            COLLECTION_METHODS_CACHE.clear()
            COLLECTION_METHODS_CACHE.extend(ref_types)
        case schemas.RefTypesServiceRegistry.CASE_TYPE:
            CASE_TYPES_CACHE.clear()
            CASE_TYPES_CACHE.extend(ref_types)
        case schemas.RefTypesServiceRegistry.FILING_TYPE:
            FILING_TYPES_CACHE.clear()
            FILING_TYPES_CACHE.extend(ref_types)
        case schemas.RefTypesServiceRegistry.HEARING_TYPE:
            HEARING_TYPES_CACHE.clear()
            HEARING_TYPES_CACHE.extend(ref_types)
        case schemas.RefTypesServiceRegistry.TASK_TYPE:
            TASK_TYPES_CACHE.clear()
            TASK_TYPES_CACHE.extend(ref_types)
        case _:
            return []


def get_app_roles_cache():
    return APP_ROLES_CACHE


def set_app_roles_cache(app_roles: list[schemas.AppRole]):
    APP_ROLES_CACHE.clear()
    APP_ROLES_CACHE.extend(app_roles)


def get_app_permissions_cache():
    return APP_PERMISSIONS_CACHE


def set_app_permissions_cache(app_permissions: list[schemas.AppPermission]):
    APP_PERMISSIONS_CACHE.clear()
    APP_PERMISSIONS_CACHE.extend(app_permissions)
