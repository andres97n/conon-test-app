from rest_framework import serializers

from applications.abp.models import TeamDetailAbp, TeamAbp
from applications.users.models import User


class TeamDetailAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamDetailAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Team Detail ABP
    def create(self, validated_data):
        if not TeamAbp.objects.team_abp_exists(validated_data['team_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, el grupo ingresado no es válido; consulte con el Administrador.'
                }
            )
        if not User.objects.user_exists(validated_data['user'].id):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el estudiante ingresado no es válido; consulte con el Administrador.'
                }
            )
        team_detail_abp = TeamDetailAbp(**validated_data)
        team_detail_abp.save()
        return team_detail_abp

    # Update Team Detail ABP
    def update(self, instance, validated_data):
        if instance.team_abp != validated_data['team_abp']:
            if not TeamAbp.objects.team_abp_exists(validated_data['team_abp'].id):
                raise serializers.ValidationError(
                    {
                        'team_abp': 'Error, el grupo ingresado no es válido; consulte con el Administrador.'
                    }
                )
        if instance.user != validated_data['user']:
            if not User.objects.user_exists(validated_data['user'].id):
                raise serializers.ValidationError(
                    {
                        'user': 'Error, el estudiante ingresado no es válido; consulte con el Administrador.'
                    }
                )
        update_team_detail_abp = super().update(instance, validated_data)
        update_team_detail_abp.save()
        return update_team_detail_abp

    # Return Team Detail ABP
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_abp': {
                'id': instance.team_abp.id,
                'observation': instance.team_abp.observation,
                'abp': {
                    'id': instance.team_abp.abp.id,
                    'title': instance.team_abp.abp.problem
                },
            },
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'active': instance.active,
            'created_at': instance.created_at
        }
