
from rest_framework import serializers

from applications.abp_steps.models import InformationReferenceStepSevenAbp
from applications.abp.models import TeamAbp, TeamDetailAbp
from applications.users.models import User


class InformationReferenceStepSevenSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationReferenceStepSevenAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def validate(self, attrs):
        if not TeamDetailAbp.objects.exists_user_in_team_abp(
                attrs['team_abp'].id, attrs['user'].id
        ):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el usuario envíado no pertenece al equipo envíado, consulte con '
                            'el Administrador.'
                }
            )
        return attrs

    # Create Information Reference ABP
    def create(self, validated_data):
        if not TeamAbp.objects.team_abp_exists(validated_data['team_abp'].id):
            raise serializers.ValidationError(
                {
                    'team_abp': 'Error, el estudiante no pertenece a este grupo, '
                                'consulte con el Administrador.'
                }
            )
        if not User.objects.user_exists(validated_data['user'].id):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el usuario no existe o está inactivo, consulte con el '
                            'Administrador.'
                }
            )
        information_reference_abp = InformationReferenceStepSevenAbp(**validated_data)
        information_reference_abp.save()
        return information_reference_abp


class InformationReferenceStepSevenAbpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationReferenceStepSevenAbp
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_abp': {
                'id': instance.team_abp.id,
                'step': instance.team_abp.step
            },
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'information_reference': instance.information_reference,
            'active': instance.active,
            'created_at': instance.created_at
        }


class InformationReferenceStepSevenAbpByTeamSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'information_reference': instance.information_reference,
            'active': instance.active,
            'created_at': instance.created_at
        }


