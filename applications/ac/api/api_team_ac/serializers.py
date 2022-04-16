
from rest_framework import serializers

from applications.ac.models import TeamAc, Ac


class TeamAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Team AC
    def create(self, validated_data):
        if not Ac.objects.exists_ac_methodology(validated_data['ac'].id):
            raise serializers.ValidationError(
                {
                    'ac': 'Error, la metodología Ac ingresada no es válida; '
                          'consulte con el Administrador.'
                }
            )
        team_ac = TeamAc(**validated_data)
        team_ac.save()
        return team_ac


class TeamAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Return Team AC
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'ac': {
                'id': instance.ac.id,
                'real_problem': instance.ac.real_problem,
                'topic': {
                    'id': instance.ac.topic.id,
                    'title': instance.ac.topic.title
                },
            },
            'observations': instance.observations,
            'active': instance.active,
            'created_at': instance.created_at
        }


class TeamAcShortListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'observations': instance.observations,
            'active': instance.active,
            'created_at': instance.created_at
        }
