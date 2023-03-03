from django.db import DataError
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


def qs_exists(queryset):
    try:
        return queryset.exists()
    except (TypeError, ValueError, DataError):
        return False

class CustomUniqueValidator(UniqueValidator):
    def __call__(self, value, serializer_field):
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        field_name = serializer_field.source_attrs[-1]
        # Determine the existing instance, if this is an update operation.
        instance = getattr(serializer_field.parent, 'instance', None)

        queryset = self.queryset
        queryset = self.filter_queryset(value, queryset, field_name)
        queryset = self.exclude_current_instance(queryset, instance)
        if instance:
            if qs_exists(queryset) and instance.made_by_user is True:
                raise ValidationError(self.message, code='unique')