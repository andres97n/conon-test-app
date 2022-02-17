from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    auth_state = models.CharField(max_length=3, default='A')

    class Meta:
        abstract = True


class BaseModelActive(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    auth_state = models.CharField(max_length=3, default='A')
    active = models.BooleanField(
        default=True,
        null=False,
        blank=True
    )

    class Meta:
        abstract = True
