from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.forms import ChoiceField, CharField
from inface.uc.models import *
from inface.uc.models import SyUser

class DeptChoiceField(ChoiceField):
    def clean(self, value):
        return Dept.objects.get(pk=value)


def get_parent_choices(root_dept):
    def get_flat_tuples(item):
        choices = [(item.pk, mark_safe(item.name_with_spacer()))]
        if item.has_children():
            for child in item.children():
                choices += get_flat_tuples(child)
        return choices
    return get_flat_tuples(root_dept)

