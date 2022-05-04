
from rest_framework import serializers

from applications.ac_roles.models import MemberPerformanceCoordinatorAc
from applications.ac.models import TeamDetailAc


class MemberPerformanceCoordinatorAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberPerformanceCoordinatorAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Member Performance Coordinator AC
    def create(self, validated_data):
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado sobre no existe o está inactivo; '
                                      'consulte con el Administrador.'
                }
            )
        member_performance_coordinator_ac = MemberPerformanceCoordinatorAc(**validated_data)
        member_performance_coordinator_ac.save()
        return member_performance_coordinator_ac


class MemberPerformanceCoordinatorAcSerializerList(serializers.ModelSerializer):
    class Meta:
        model = MemberPerformanceCoordinatorAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_detail_ac': {
                'id': instance.team_detail_ac.id,
                'role_type': instance.team_detail_ac.role_type
            },
            'member_assessment': instance.member_assessment,
            'active': instance.active,
            'created_at': instance.created_at
        }
