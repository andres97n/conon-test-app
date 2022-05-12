
from rest_framework import serializers

from applications.ac.models import TeamDetailAc
from applications.ac_roles.models import PerformanceDescriptionSpokesmanAc


class PerformanceDescriptionSpokesmanAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceDescriptionSpokesmanAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Performance Description Spokesman AC
    def create(self, validated_data):
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado no existe o está inactivo; '
                                      'consulte con el Administrador.'
                }
            )
        performance_description_spokesman_ac = PerformanceDescriptionSpokesmanAc(**validated_data)
        performance_description_spokesman_ac.save()
        return performance_description_spokesman_ac

    # Update Performance Description Spokesman AC
    def update(self, instance, validated_data):
        if instance.team_detail_ac != validated_data['team_detail_ac']:
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, una vez ingresado el Integrante no se lo puede cambiar.'
                }
            )
        update_performance_description_spokesman_ac = super().update(instance, validated_data)
        update_performance_description_spokesman_ac.save()
        return update_performance_description_spokesman_ac


class PerformanceDescriptionSpokesmanAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceDescriptionSpokesmanAc
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
            'performance_description': instance.performance_description,
            'oral_description': instance.oral_description,
            'active': instance.active,
            'created_at': instance.created_at
        }

