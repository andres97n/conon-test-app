
from rest_framework import serializers

from applications.ac.models import TeamDetailAc
from applications.ac_roles.models import FeaturedInformationSecretaryAc


class FeaturedInformationSecretaryAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedInformationSecretaryAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Featured Information Secretary AC
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
        featured_information_secretary_ac = FeaturedInformationSecretaryAc(**validated_data)
        featured_information_secretary_ac.save()
        return featured_information_secretary_ac

    # Update Featured Information Secretary AC
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
        update_featured_information_secretary_ac = super().update(instance, validated_data)
        update_featured_information_secretary_ac.save()
        return update_featured_information_secretary_ac


class FeaturedInformationSecretaryAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedInformationSecretaryAc
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
                'name': instance.member_ac.owner.__str__(),
                'role_type': instance.member_ac.role_type
            },
            'external_path': instance.external_path,
            'description_path': instance.description_path,
            'active': instance.active,
            'created_at': instance.created_at
        }
