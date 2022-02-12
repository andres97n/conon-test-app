from rest_framework import serializers

from applications.abp_steps.models import OpinionStepOneAbp
from applications.abp.models import TeamDetailAbp


class OpinionStepOneAbpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpinionStepOneAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Opinion ABP
    def create(self, validated_data):
        if not TeamDetailAbp.objects.exists_team_detail_abp(validated_data['team_detail_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_abp': 'Error, el grupo enviado no existe.'
                }
            )
        opinion_abp = OpinionStepOneAbp(**validated_data)
        opinion_abp.save()
        return opinion_abp

    # Update Opinion ABP
    def update(self, instance, validated_data):
        if instance.team_detail_abp != validated_data['team_detail_abp']:
            raise serializers.ValidationError(
                {
                    'team_detail_abp': 'Error, no se puede cambiar de grupo.'
                }
            )
        update_opinion_abp = super().update(instance, validated_data)
        update_opinion_abp.save()
        return update_opinion_abp

    # Opinion ABP List
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_detail_abp': {
                'id': instance.team_detail_abp.id,
                'user': instance.team_detail_abp.user.__str__(),
                'is_moderator': instance.team_detail_abp.is_moderator
            },
            'opinion': instance.opinion,
            'active': instance.active,
            'created_at': instance.created_at
        }


class OpinionAbpByTeamAbpSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['opinionsteponeabp'],
            'opinion': instance['opinionsteponeabp__opinion'],
            'active': instance['opinionsteponeabp__active'],
            'created_at': instance['opinionsteponeabp__created_at']
        }
