from django.db.models import Model
from django.core.cache import cache


def get_cached_count(instance: Model, field_name: str, queryset):
    """
    Retrieve the count for a specific field from the cache or the database if not cached.

    Args:
        instance (Model): The instance of the model for which the count is retrieved.
        field_name (str): The name of the field for which the count is retrieved.
        queryset (QuerySet): The queryset used to retrieve the count from the database.

    Returns:
        int: The count value.
    """

    cache_key = f"{instance._meta.model_name}_{instance.pk}_{field_name}"

    # Retrieve count from cache
    count = cache.get(cache_key)

    if count is None:
        count = queryset.count()
        cache.set(cache_key, count, timeout=360)

    return count
