
from rest_framework import serializers

from applications.abp.models import TeamDetailAbp
from applications.abp_steps.models import PerformActionStepFiveAbp


class PerformActionStepFiveAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformActionStepFiveAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Perform Action ABP
    def create(self, validated_data):
        if not TeamDetailAbp.objects.exists_team_detail_abp(
                validated_data['team_detail_abp'].id
        ):
            raise serializers.ValidationError(
                {
                    'team_detail_abp': 'Error, el estudiante no pertenece a este grupo, '
                                       'consulte con el Administrador.'
                }
            )
        perform_action_abp = PerformActionStepFiveAbp(**validated_data)
        perform_action_abp.save()
        return perform_action_abp

    # Update Perform Action ABP
    def update(self, instance, validated_data):
        if instance.team_detail_abp != validated_data['team_detail_abp']:
            raise serializers.ValidationError(
                {
                    'team_detail_abp': 'Error, no se puede cambiar de referencia, '
                                       'consulte con el administrador.'
                }
            )
        update_perform_action_abp = super().update(instance, validated_data)
        update_perform_action_abp.save()
        return update_perform_action_abp


class PerformActionStepFiveAbpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformActionStepFiveAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_detail_abp': {
                'id': instance.team_detail_abp.id,
                'user': {
                    'id': instance.team_detail_abp.user.id,
                    'name': instance.team_detail_abp.user.__str__()
                },
                'is_moderator': instance.team_detail_abp.is_moderator
            },
            'action': instance.action,
            'active': instance.active,
            'created_at': instance.created_at
        }


class PerformActionStepFiveAbpListByTeamDetailSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'action': instance.action,
            'active': instance.active,
            'created_at': instance.created_at
        }
