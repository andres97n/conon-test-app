from django.core import serializers
from django.db import models
from django.forms.models import model_to_dict

from applications.users.models import AuditUser


def get_changed_fields(old_instance=None, new_instance=None):
    changed_fields = {}
    for key, value in new_instance.items():
        for old_field in old_instance._meta.fields:
            if old_field.name == key:
                print(old_field.name, '-', key)
                print(old_field.value_from_object(old_instance), '-', value)
                if old_field.value_from_object(old_instance) != value:
                    changed_fields[old_field.name] = old_field.value_to_string(old_instance)
        '''
        if old_instance.new_field.name != new_field.name:
            changed_fields[new_field.name] = new_field.value_to_string(new_instance)
        '''
    return changed_fields


def get_data_dict(instance=None):
    data = {}
    for field in instance._meta.fields:
        print(type(field.value_from_object(instance)))
        if type(field.value_from_object(instance)) == models.fields.related.ForeignKey:
            pass
        else:
            data[field.name] = field.value_to_string(instance)
    return data


def save_auth_user(
        table=None, instance=None, user=None,
        update=False, old_instance=None, serializer_class=None,
        audit_type=None
):
    '''
    AuditUser.objects.create(
        table=table,
        new_values={},
        record_id=instance.id,
        audit_type=audit_type,
        add_by=user
    )
    '''
    audit_user = AuditUser()
    audit_user.table = table
    audit_user.audit_type = audit_type
    if update:
        audit_user.new_values = instance
        audit_user.record_id = old_instance.id
        audit_user.old_values = serializer_class(old_instance).data
    else:
        audit_user.new_values = {}
        audit_user.record_id = instance.id
        audit_user.old_values = {}
        audit_user.fields_changed = {}
    audit_user.add_by = user
    audit_user.save()
