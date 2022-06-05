from rest_framework import serializers

from applications.users.models import User, Person


# Serializer for Create and Update a normal User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'updated_at',
            'created_at'
        ]

    def validate_person(self, value):
        person = Person.objects.is_deleted(value.id)
        if person is None:
            raise serializers.ValidationError(
                'Error, esta Persona no existe.'
            )
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                'Error, la contraseña debe contener por lo menos 6 caracteres.'
            )
        return value

    # Type field validation
    def validate_type(self, value):
        if value > 2:
            raise serializers.ValidationError(
                detail='Error, no existe este Tipo.'
            )
        return value

    def validate(self, attrs):
        if not User.objects.validate_user_type(attrs['person'].id):
            raise serializers.ValidationError(
                {
                    'type': 'Error, este Usuario no puede ser de este tipo.'
                }
            )
        return attrs

    # Create a normal User
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        if instance.person is None:
            return {
                'id': instance.id,
                'person': {
                  'id': None,
                  'name': instance.__str__(),
                },
                'username': instance.username,
                'email': instance.email,
                'type': instance.type,
                'is_active': instance.is_active,
                'is_superuser': instance.is_superuser,
                'created_at': instance.created_at
            }

        return {
            'id': instance.id,
            'person': {
              'id': instance.person.id,
              'identification': instance.person.identification,
              'name': instance.__str__(),
            },
            'username': instance.username,
            'email': instance.email,
            'type': instance.type,
            'is_active': instance.is_active,
            'is_superuser': instance.is_superuser,
            'created_at': instance.created_at
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email'
        ]


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
