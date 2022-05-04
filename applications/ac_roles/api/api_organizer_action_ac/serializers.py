
from rest_framework import serializers

from applications.ac.models import TeamDetailAc
from applications.ac_roles.models import OrganizerActionAc


class OrganizerActionAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerActionAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Organizer Action AC
    def create(self, validated_data):
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado sobre no existe o está inactivo; '
                                      'consulte con el Administrador.'
                }
            )
        organizer_action_ac = OrganizerActionAc(**validated_data)
        organizer_action_ac.save()
        return organizer_action_ac


class OrganizerActionAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerActionAc
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
            'action': instance.action,
            'active': instance.active,
            'created_at': instance.created_at
        }
