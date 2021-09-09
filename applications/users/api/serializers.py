from rest_framework import serializers, pagination

from applications.users.models import Person, User


# TODO: add more functionally
#   for a persons in a platform

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'id',
            'identification',
            'name',
            'last_name',
            'gender',
            'age',
            'phone',
            'auth_state'
        )


class UserSerializer(serializers.ModelSerializer):
    persona = PersonSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'persona',
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
