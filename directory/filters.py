from url_filter.filtersets import ModelFilterSet

from .models import Teacher

class TeacherFilterSet(ModelFilterSet):
    """
    Used django-url-filter
    Allows filtering on last_name or subjects field.
    """
    class Meta:
        model = Teacher
        fields = ["last_name", "subjects", ]
