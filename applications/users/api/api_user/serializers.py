from rest_framework import serializers, pagination

from applications.users.models import User
from applications.users.api.api_person.serializers import PersonSerializer


# TODO: add more functionally
#   for a persons in a platform


class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'person',
            'email',
            'type',
            'is_superuser',
            'is_staff',
            'is_active',
        )


class UserCreateSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = User
        fields = (
            'username',
            'person',
            'email',
            'type',
            'is_superuser',
            'is_staff',
            'is_active',
        )


class UserTokenSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'person',
        )
