
from rest_framework import serializers

from applications.ac.models import TeamDetailAc
from applications.ac_roles.models import ActivityDescriptionSpokesmanAc


class ActivityDescriptionSpokesmanAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityDescriptionSpokesmanAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Activity Description Spokesman AC
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
                    'member_ac': 'Error, el integrante ingresado no existe o está inactivo; '
                                 'consulte con el Administrador.'
                }
            )
        activity_description_spokesman_ac = ActivityDescriptionSpokesmanAc(**validated_data)
        activity_description_spokesman_ac.save()
        return activity_description_spokesman_ac

    # Update Activity Description Spokesman AC
    def update(self, instance, validated_data):
        if instance.team_detail_ac != validated_data['team_detail_ac']:
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, una vez ingresado el Integrante no se lo puede cambiar.'
                }
            )
        if instance.member_ac != validated_data['member_ac']:
            raise serializers.ValidationError(
                {
                    'member_ac': 'Error, una vez ingresado el Integrante no se lo puede cambiar.'
                }
            )
        update_activity_description_spokesman_ac = super().update(instance, validated_data)
        update_activity_description_spokesman_ac.save()
        return update_activity_description_spokesman_ac


class ActivityDescriptionSpokesmanAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityDescriptionSpokesmanAc
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
            'activity_description': instance.activity_description,
            'active': instance.active,
            'created_at': instance.created_at
        }
