from rest_framework import serializers, pagination

from applications.users.models import User, Person


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
        )

    def validate_person(self, value):
        person = Person.objects.is_deleted(value.id)
        if person is None:
            raise serializers.ValidationError('Error, esta Persona no existe.')
        return value

    # Type field validation
    def validate_type(self, value):
        if value == 0:
            raise serializers.ValidationError('Error, el Usuario que se intenta crear no pueder ser de este tipo.')
        if value > 2:
            raise serializers.ValidationError('Error, no existe este Tipo.')
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

    def to_representation(self, instance):
        print(instance.id)
        return dict(
            id=instance.id,
            username=instance.username,
            name=instance.person.name,
            last_name=instance.person.last_name,
            email=instance.email,
            type=instance.type,
            is_superuser=instance.is_superuser
        )


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
