from rest_framework import serializers

from applications.ac.models import TeamAc
from applications.ac_roles.models import SecretaryInformationAc


class SecretaryInformationAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretaryInformationAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Secretary Information AC
    def create(self, validated_data):
        if not TeamAc.objects.exists_team_ac(validated_data['team_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_ac': 'Error, el integrante ingresado no existe o está inactivo; '
                               'consulte con el Administrador.'
                }
            )
        secretary_information_ac = SecretaryInformationAc(**validated_data)
        secretary_information_ac.save()
        return secretary_information_ac


class SecretaryInformationAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretaryInformationAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_ac': {
                'id': instance.team_ac.id,
                'team_state': instance.team_ac.team_state
            },
            'external_path': instance.external_path,
            'active': instance.active,
            'created_at': instance.created_at
        }
