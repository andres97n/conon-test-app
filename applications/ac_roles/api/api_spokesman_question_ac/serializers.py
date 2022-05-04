
from rest_framework import serializers

from applications.ac.models import TeamDetailAc
from applications.ac_roles.models import SpokesmanQuestionAc


class SpokesmanQuestionAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokesmanQuestionAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Spokesman Question AC
    def create(self, validated_data):
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado sobre no existe o está inactivo; '
                                      'consulte con el Administrador.'
                }
            )
        spokesman_question_ac = SpokesmanQuestionAc(**validated_data)
        spokesman_question_ac.save()
        return spokesman_question_ac


class SpokesmanQuestionAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokesmanQuestionAc
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
            'spokesman_question': instance.spokesman_question,
            'active': instance.active,
            'created_at': instance.created_at
        }
