from rest_framework import serializers, pagination

from applications.users.models import Person


# Create or Update Person Serializer
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'identification',
            'identification_type',
            'name',
            'last_name',
            'gender',
            'age',
            'phone',
            'created_at'
        )

    # Validate Identification
    def validate_identification(self, value):
        if not value.isdecimal():
            raise serializers.ValidationError(
                detail='Error, la Identificación debe contener solo números.'
            )
        return value

    # Validate Identification Type
    def validate_identification_type(self, value):
        if value > 1:
            raise serializers.ValidationError(
                detail='Error, no existe este tipo de identificación.'
            )
        return value

    # Validate Gender
    def validate_gender(self, value):
        if value > 2:
            raise serializers.ValidationError(
                detail='Error, no existe este Género.'
            )
        return value

    # Validate Age
    def validate_age(self, value):
        if value >= 80:
            raise serializers.ValidationError(
                detail='Error, esta persona no debe tener 80 años o más.'
            )
        return value

    def validate(self, attrs):
        # Validate the length of the identification
        if attrs['identification_type'] == 0:
            if len(attrs['identification']) != 10:
                raise serializers.ValidationError(
                    detail={
                        'ok': False,
                        'detail': 'Error, la Identificación debe contener 10 números.'
                    }
                )
        return attrs

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'identification': instance.identification,
            'name': instance.name,
            'last_name': instance.last_name,
            'gender': instance.gender,
            'age': instance.age,
            'phone': instance.phone,
            'created_at': instance.created_at
        }
