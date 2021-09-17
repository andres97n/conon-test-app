from rest_framework import serializers, pagination

from applications.users.models import Person


# Create or Update Person Serializer
class PersonSerializer(serializers.ModelSerializer):
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

    # Validate Identification
    def validate_identification(self, value):
        if not value.isdecimal():
            raise serializers.ValidationError('Error, la Identificación debe contener solo números.')
        return value

    # Validate Gender
    def validate_gender(self, value):
        if value > 2:
            raise serializers.ValidationError('Error, no existe este Género.')
        return value

    # Validate Age
    def validate_age(self, value):
        if value >= 80:
            raise serializers.ValidationError('Error, esta persona no debe tener 80 años o más.')
        return value

    def to_representation(self, instance):
        return dict(
            id=instance.id,
            identification=instance.identification,
            name=instance.name,
            last_name=instance.last_name,
            gender=instance.gender,
            age=instance.age,
            phone=instance.phone
        )


# Person List or Person Detail Serializer
class PersonListSerializer(serializers.ModelSerializer):
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
        )
