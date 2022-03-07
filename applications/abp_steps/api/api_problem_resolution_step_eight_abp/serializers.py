
from rest_framework import serializers

from applications.abp_steps.models import ProblemResolutionStepEightAbp
from applications.abp.models import TeamAbp


class ProblemResolutionStepEightAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemResolutionStepEightAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Problem Resolution ABP
    def create(self, validated_data):
        if not TeamAbp.objects.team_abp_exists(validated_data['team_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, el estudiante no pertenece a este grupo, '
                                'consulte con el Administrador.'
                }
            )
        problem_resolution_abp = ProblemResolutionStepEightAbp(**validated_data)
        problem_resolution_abp.save()
        return problem_resolution_abp

    # Update Problem Resolution ABP
    def update(self, instance, validated_data):
        if instance.team_abp != validated_data['team_abp']:
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, no se puede cambiar de referencia, '
                                'consulte con el administrador.'
                }
            )
        update_problem_resolution_abp = super().update(instance, validated_data)
        update_problem_resolution_abp.save()
        return update_problem_resolution_abp


class ProblemResolutionStepEightAbpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemResolutionStepEightAbp
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
            'problem_resolution': instance.problem_resolution,
            'video_url': instance.video_url,
            'image_references': instance.image_references,
            'observations': instance.observations,
            'active': instance.active,
            'created_at': instance.created_at
        }
