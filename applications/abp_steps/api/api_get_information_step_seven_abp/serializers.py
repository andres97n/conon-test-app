
from rest_framework import serializers

from applications.abp_steps.models import GetInformationStepSevenAbp
from applications.abp.models import TeamAbp


class GetInformationStepSevenAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetInformationStepSevenAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Get Information ABP
    def create(self, validated_data):
        if not TeamAbp.objects.team_abp_exists(validated_data['team_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, el estudiante no pertenece a este grupo, '
                                'consulte con el Administrador.'
                }
            )
        get_information_abp = GetInformationStepSevenAbp(**validated_data)
        get_information_abp.save()
        return get_information_abp

    # Update Get Information ABP
    def update(self, instance, validated_data):
        if instance.team_abp != validated_data['team_abp']:
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, no se puede cambiar de referencia, '
                                'consulte con el administrador.'
                }
            )
        update_get_information_abp = super().update(instance, validated_data)
        update_get_information_abp.save()
        return update_get_information_abp


class GetInformationStepSevenAbpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetInformationStepSevenAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_abp': {
                'id': instance.team_abp.id,
                'step': instance.team_abp.step
            },
            'get_information': instance.get_information,
            'observations': instance.observations,
            'active': instance.active,
            'created_at': instance.created_at
        }

