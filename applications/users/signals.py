from django.db.models.signals import post_save

from .models import AuditUser, User

# def save_current_user(sender, environ, *args, **kwargs):

'''
def save_audit_user(sender, instance, created, update_fields, **kwargs):
    if created:
        audit_user = AuditUser()
        audit_user.table = sender.__name__
        audit_user.fields_changed = serializers.serialize('json', instance)
        audit_user.record_id = instance.id
        if update_fields is not None:
            audit_user.old_values = {}
            audit_user.new_values = serializers.serialize('json', update_fields)
        audit_user.add_by = 1
        audit_user.save()


post_save.connect(save_audit_user, sender=User)
'''