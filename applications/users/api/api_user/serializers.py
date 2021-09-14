from rest_framework import serializers, pagination

from applications.users.models import User
from applications.users.api.api_person.serializers import PersonSerializer, PersonCreateSerializer


# TODO: add more functionally
#   for a persons in a platform


# Serializer for Create and Update a normal User
class UserSerializer(serializers.ModelSerializer):
    # person = PersonCreateSerializer()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'type',
        )

    # Return a full detail User data
    def to_representation(self, instance):
        return dict(
            id=instance['id'],
            username=instance['username'],
            name=instance['person__name'],
            last_name=instance['person__last_name'],
            email=instance['email'],
            type=instance['type'],
            is_superuser=instance['is_superuser']
        )

    # Validation of type field
    def validate_type(self, value):
        if value == 0:
            raise serializers.ValidationError('Error, no se puede crear a un Usuario Administrador.')
        return value

    # Create a normal User
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # Update a normal User
    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


class UserTokenSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'person',
        )
