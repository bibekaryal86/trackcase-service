# do not use lru-cache because the result differs per param
# and `request` param will be different
# this should suffice for now
from src.trackcase_service.service import schemas

COMPONENT_STATUSES_CACHE = []


def get_component_statuses_cache():
    return COMPONENT_STATUSES_CACHE


def set_component_statuses_cache(component_statuses: list[schemas.ComponentStatus]):
    COMPONENT_STATUSES_CACHE.clear()
    COMPONENT_STATUSES_CACHE.extend(component_statuses)
