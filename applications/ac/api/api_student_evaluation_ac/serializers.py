
from rest_framework import serializers

from applications.ac.models import StudentEvaluationAc, RubricAc, TeamDetailAc


class StudentEvaluationAcSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvaluationAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Validate State
    def validate_state(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError(
                {
                    'state': 'Error, el estado envíado no puede tener ese valor; '
                             'consulte con el Administrador.'
                }
            )
        return value

    # Create Student Activity AC
    def create(self, validated_data):
        if not RubricAc.objects.exists_rubric_ac(validated_data['rubric_ac'].id):
            raise serializers.ValidationError(
                {
                    'rubric_ac': 'Error, la rúbrica ingresada no es válida; '
                                 'consulte con el Administrador.'
                }
            )
        if not TeamDetailAc.objects.exists_team_detail_ac(validated_data['team_detail_ac'].id):
            raise serializers.ValidationError(
                {
                    'team_detail_ac': 'Error, el integrante ingresado no es válido; '
                                      'consulte con el Administrador.'
                }
            )
        student_activity_ac = StudentEvaluationAc(**validated_data)
        student_activity_ac.save()
        return student_activity_ac


class StudentEvaluationAcListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvaluationAc
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'rubric_ac': {
                'id':  instance.rubric_ac.id,
                'description_rubric': instance.rubric_ac.description_rubric
            },
            'team_detail_ac': {
                'id': instance.team_detail_ac.id,
                'role_type': instance.team_detail_ac.role_type
            },
            'description': instance.description,
            'evaluation_type': instance.evaluation_type,
            'final_value': instance.final_value,
            'observations': instance.observations,
            'state': instance.state,
            'created_at': instance.created_at
        }


class StudentEvaluationAcShortListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'description': instance.description,
            'evaluation_type': instance.evaluation_type,
            'final_value': instance.final_value,
            'observations': instance.observations,
            'state': instance.state,
            'created_at': instance.created_at
        }
