
from rest_framework import serializers

from applications.ac.models import TeamDetailAc
from applications.ac_roles.models import AssignActivityOrganizerAc


class AssignActivityOrganizerAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignActivityOrganizerAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Assign Activity Organizer AC
    def create(self, validated_data):
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado sobre no existe o está inactivo; '
                                      'consulte con el Administrador.'
                }
            )
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['member_ac'].id):
            raise serializers.ValidationError(
                {
                    'member_ac': 'Error, el integrante ingresado sobre no existe o está inactivo; '
                                 'consulte con el Administrador.'
                }
            )
        assign_activity_organizer_ac = AssignActivityOrganizerAc(**validated_data)
        assign_activity_organizer_ac.save()
        return assign_activity_organizer_ac


class AssignActivityOrganizerAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignActivityOrganizerAc
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
            'member_ac': {
                'id': instance.member_ac.id,
                'role_type': instance.member_ac.role_type
            },
            'member_activity': instance.member_activity,
            'active': instance.active,
            'created_at': instance.created_at
        }
