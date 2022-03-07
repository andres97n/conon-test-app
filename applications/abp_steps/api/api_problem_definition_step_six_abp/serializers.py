
from rest_framework import serializers

from applications.abp_steps.models import ProblemDefinitionStepSixAbp
from applications.abp.models import TeamAbp


class ProblemDefinitionStepSixAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemDefinitionStepSixAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Problem Definition ABP
    def create(self, validated_data):
        if not TeamAbp.objects.team_abp_exists(validated_data['team_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, el estudiante no pertenece a este grupo, '
                                'consulte con el Administrador.'
                }
            )
        problem_definition_abp = ProblemDefinitionStepSixAbp(**validated_data)
        problem_definition_abp.save()
        return problem_definition_abp

    # Update Problem Definition ABP
    def update(self, instance, validated_data):
        if instance.team_abp != validated_data['team_abp']:
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, no se puede cambiar de referencia, '
                                'consulte con el administrador.'
                }
            )
        update_problem_definition_abp = super().update(instance, validated_data)
        update_problem_definition_abp.save()
        return update_problem_definition_abp


class ProblemDefinitionStepSixAbpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemDefinitionStepSixAbp
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
            'problem_definition': instance.problem_definition,
            'observations': instance.observations,
            'active': instance.active,
            'created_at': instance.created_at
        }
