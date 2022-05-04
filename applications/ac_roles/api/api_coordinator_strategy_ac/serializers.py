
from rest_framework import serializers

from applications.ac_roles.models import CoordinatorStrategyAc
from applications.ac.models import TeamDetailAc


class CoordinatorStrategyAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordinatorStrategyAc
        exclude = [
            'updated_at',
            'created_at'
        ]

    # Create Coordinator Strategy AC
    def create(self, validated_data):
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado sobre no existe o está inactivo; '
                                      'consulte con el Administrador.'
                }
            )
        coordinator_strategy_ac = CoordinatorStrategyAc(**validated_data)
        coordinator_strategy_ac.save()
        return coordinator_strategy_ac


class CoordinatorStrategyListAcSerializer(serializers.ModelSerializer):
    model = CoordinatorStrategyAc
    exclude = [
        'update_at',
        'created_at'
    ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'team_detail_ac': {
                'id': instance.team_detail_ac.id,
                'role_type': instance.team_detail_ac.role_type
            },
            'strategy': instance.strategy,
            'active': instance.active,
            'created_at': instance.created_at
        }
