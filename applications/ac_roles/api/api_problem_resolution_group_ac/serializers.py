
from rest_framework import serializers

from applications.ac_roles.models import ProblemResolutionGroupAc
from applications.ac.models import TeamAc


class ProblemResolutionGroupAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemResolutionGroupAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Problem Resolution Group AC
    def create(self, validated_data):
        if not TeamAc.objects.exists_team_ac(validated_data['team_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_ac': 'Error, el equipo ingresado sobre no existe o está inactivo; '
                               'consulte con el Administrador.'
                }
            )
        problem_resolution_group_ac = ProblemResolutionGroupAc(**validated_data)
        problem_resolution_group_ac.save()
        return problem_resolution_group_ac


class ProblemResolutionGroupAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemResolutionGroupAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_ac': {
                'id': instance.team_ac.id,
                'role_type': instance.team_ac.role_type
            },
            'problem_resolution': instance.problem_resolution,
            'references_images': instance.references_images,
            'observations': instance.observations,
            'active': instance.active,
            'created_at': instance.created_at
        }




