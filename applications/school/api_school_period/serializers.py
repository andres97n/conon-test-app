from rest_framework import serializers

from applications.school.models import SchoolPeriod


class SchoolPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPeriod
        exclude = [
            'created_at',
            'updated_at',
            'auth_state'
        ]

    # State Validation
    def validate_state(self, value):
        if value > 1:
            raise serializers.ValidationError('Error, no se puede asignar este Estado a un Período Lectivo.')
        return value

    def validate(self, attrs):
        if attrs['init_date'] >= attrs['end_date']:
            raise serializers.ValidationError('Error: la Fecha de Inicio no puede ser la misma o mayor que la Fecha ' 
                                              'de Final de Período.')
        return attrs

    def to_representation(self, instance):
        return dict(
            name=instance.name,
            init_date=instance.init_date,
            end_date=instance.end_date,
            school_end_date=instance.school_end_date,
            state=instance.state.__str__(),
            observations=instance.observations
        )
