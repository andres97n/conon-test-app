from rest_framework import serializers, pagination

from applications.users.models import Person


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


class PersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'identification',
            'name',
            'last_name',
            'gender',
            'age',
            'phone',
        )
