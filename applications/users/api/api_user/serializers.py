from rest_framework import serializers, pagination

from applications.users.models import User, Person
from applications.base.functions import save_auth_user


# TODO: Realizar un serializer para el cambio de contraseña


# Serializer for Create and Update a normal User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'person',
            'email',
            'password',
            'type',
            'created_at'
        )

    def validate_person(self, value):
        person = Person.objects.is_deleted(value.id)
        if person is None:
            raise serializers.ValidationError(
                detail='Error, esta Persona no existe.'
            )
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                detail='Error, la contraseña debe contener por lo menos 6 caracteres.'
            )
        return value

    # Type field validation
    def validate_type(self, value):
        if value == 0:
            raise serializers.ValidationError(
                detail='Error, el Usuario que se intenta crear no pueder ser de este tipo.'
            )
        if value > 2:
            raise serializers.ValidationError(
                detail='Error, no existe este Tipo.'
            )
        return value

    def validate(self, attrs):
        if not User.objects.validate_user_type(attrs['person'].id, attrs['type']):
            raise serializers.ValidationError(
                detail='Error, este Usuario no puede ser de este tipo.'
            )
        return attrs

    # Create a normal User
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # Update a normal User
    def update(self, instance, validated_data):
        if instance.person != validated_data['person']:
            raise serializers.ValidationError(
                detail='Error, no se puede cambiar de Persona.'
            )
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'person': {
                'id': instance.person.id,
                'name': instance.person.name,
                'last_name': instance.person.last_name,
            },
            'email': instance.email,
            'type': instance.type,
            'created_at': instance.created_at
        }


'''
class UserTokenSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'person',
        )

    def get_person(self, obj):
        person = User.objects.filter(username=obj['username']).values(
            'person__name',
            'person__last_name'
        )
        return person
'''
