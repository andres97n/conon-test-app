from rest_framework import serializers

from applications.school.models import SchoolPeriod


class SchoolPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPeriod
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # State Validation
    def validate_state(self, value):
        if value > 1:
            raise serializers.ValidationError(
                {
                    'state': 'Error, no se puede asignar este Estado a un Período Lectivo.'
                }
            )
        return value

    def validate(self, attrs):
        if attrs['init_date'] >= attrs['end_date']:
            raise serializers.ValidationError(
                'Error: la Fecha de Inicio no puede ser la misma o mayor que la Fecha '
                'Final de Período.'
            )
        return attrs

    # Create a School Period
    def create(self, validated_data):
        if SchoolPeriod.objects.is_name_exists(validated_data['name']):
            raise serializers.ValidationError(
                {
                    'name': 'Error, este Período Lectivo ya existe.'
                }
            )
        school_period = SchoolPeriod(**validated_data)
        school_period.save()
        return school_period

    # Update School Period
    def update(self, instance, validated_data):
        if instance.name != validated_data['name']:
            if SchoolPeriod.objects.is_name_exists(validated_data['name']):
                raise serializers.ValidationError(
                    {
                        'name': 'Error, no se puede cambiar el nombre del Período Lectivo.'
                    }
                )
        update_school_period = super().update(instance, validated_data)
        update_school_period.save()
        return update_school_period

    # Get School Period Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'init_date': instance.init_date,
            'end_date': instance.end_date,
            'school_end_date': instance.school_end_date,
            'state': instance.get_state_display(),
            'observations': instance.observations,
            'created_at': instance.created_at
        }


class SchoolPeriodForAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPeriod
        include = [
            'id',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
        }

