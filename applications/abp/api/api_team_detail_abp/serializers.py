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

    # General Validate
    def validate(self, attrs):
        if attrs['is_moderator'] is True:
            if TeamAbp.objects.exists_moderator_in_team_abp(attrs['team_abp'].id):
                raise serializers.ValidationError(
                    {
                        'is_moderator': 'Error, ya existe un Moderador en el grupo.'
                    }
                )
        if not TeamAbp.objects.team_abp_exists(attrs['team_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, el grupo ingresado no es válido; consulte con el Administrador.'
                }
            )
        if not User.objects.type_user_exists(attrs['user'].id, 2):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el estudiante ingresado no es válido; consulte con el Administrador.'
                }
            )
        elif TeamAbp.objects.exists_user_in_team_abp(attrs['team_abp'].id, attrs['user'].id):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el Estudiante enviado ya ha sido agregado a este grupo.'
                }
            )

        return attrs

    # Create Team Detail ABP
    def create(self, validated_data):
        if TeamAbp.objects.get_count_of_users_in_team_abp(validated_data['team_abp'].id) == 4:
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, según la aplicación de ABP por CONON se requiere un '
                                'máximo de 4 estudiantes por grupo.'
                }
            )
        team_detail_abp = TeamDetailAbp(**validated_data)
        team_detail_abp.save()
        return team_detail_abp

    # Update Team Detail ABP
    def update(self, instance, validated_data):
        update_team_detail_abp = super().update(instance, validated_data)
        update_team_detail_abp.save()
        return update_team_detail_abp

    # Return Team Detail ABP
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_abp': {
                'id': instance.team_abp.id,
                'observations': instance.team_abp.observations,
                'abp': {
                    'id': instance.team_abp.abp.id,
                    'title': instance.team_abp.abp.problem
                },
            },
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'is_moderator': instance.is_moderator,
            'active': instance.active,
            'created_at': instance.created_at
        }
