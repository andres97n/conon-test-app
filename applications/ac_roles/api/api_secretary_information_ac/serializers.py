

from rest_framework import serializers

from applications.ac.models import TeamDetailAc
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
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado no existe o está inactivo; '
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
            'team_detail_ac': {
                'id': instance.team_detail_ac.id,
                'role_type': instance.team_detail_ac.role_type
            },
            'external_path': instance.external_path,
            'active': instance.active,
            'created_at': instance.created_at
        }

