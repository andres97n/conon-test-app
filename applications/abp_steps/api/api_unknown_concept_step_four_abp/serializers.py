
from rest_framework import serializers

from applications.abp_steps.models import UnknownConceptStepFourAbp
from applications.abp.models import TeamAbp


class UnknownConceptStepFourAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnknownConceptStepFourAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Unknown Concept ABP
    def create(self, validated_data):
        if not TeamAbp.objects.team_abp_exists(validated_data['team_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, el estudiante no pertenece a este grupo, '
                                'consulte con el Administrador.'
                }
            )
        unknown_concept_abp = UnknownConceptStepFourAbp(**validated_data)
        unknown_concept_abp.save()
        return unknown_concept_abp

    # Update Unknown Concept ABP
    def update(self, instance, validated_data):
        if instance.team_abp != validated_data['team_abp']:
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, no se puede cambiar de referencia, '
                                'consulte con el administrador.'
                }
            )
        update_unknown_concept_abp = super().update(instance, validated_data)
        update_unknown_concept_abp.save()
        return update_unknown_concept_abp


class UnknownConceptStepFourAbpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnknownConceptStepFourAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team': {
              'id': instance.team_abp.id,
              'step': instance.team_abp.step
            },
            'unknown_concept': instance.unknown_concept,
            'active': instance.active,
            'created_at': instance.created_at
        }


class SmallUnknownConceptStepFourAbpListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'unknown_concept': instance.unknown_concept,
            'active': instance.active,
            'created_at': instance.created_at
        }
