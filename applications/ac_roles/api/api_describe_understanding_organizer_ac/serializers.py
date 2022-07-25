
from rest_framework import serializers

from applications.ac.models import TeamDetailAc
from applications.ac_roles.models import DescribeUnderstandingOrganizerAc


class DescribeUnderstandingOrganizerAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescribeUnderstandingOrganizerAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Organizer Action AC
    def create(self, validated_data):
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado no existe o está inactivo; '
                                      'consulte con el Administrador.'
                }
            )
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['member_ac'].id):
            raise serializers.ValidationError(
                {
                    'member_ac': 'Error, el integrante ingresado no existe o está inactivo; '
                                 'consulte con el Administrador.'
                }
            )
        describe_understanding_organizer_ac = DescribeUnderstandingOrganizerAc(**validated_data)
        describe_understanding_organizer_ac.save()
        return describe_understanding_organizer_ac


class DescribeUnderstandingOrganizerListAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescribeUnderstandingOrganizerAc
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
                'name': instance.member_ac.__str__(),
                'role_type': instance.member_ac.role_type
            },
            'member_assessment': instance.member_assessment,
            'understanding': instance.understanding,
            'active': instance.active,
            'created_at': instance.created_at
        }
