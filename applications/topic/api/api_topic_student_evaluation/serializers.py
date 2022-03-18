from rest_framework import serializers

from applications.topic.models import TopicStudentEvaluation, Topic
from applications.users.models import User


class TopicStudentEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicStudentEvaluation
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # State Validation
    def validate_final_grade(self, value):
        if value < 0:
            raise serializers.ValidationError(
                {
                    'final_grade': 'Error, la nota final no puede ser menor que 0.'
                }
            )
        return value

    # Create Topic Student Evaluation
    def create(self, validated_data):
        if not User.objects.user_exists(validated_data['user'].id):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el usuario no existe o está inactivo no es válida; consulte '
                            'con el Administrador.'
                }
            )
        elif not User.objects.type_user_exists(validated_data['user'].id, 2):
            raise serializers.ValidationError(
                {
                    'user': 'Error, el usuario no es un Estudiante o está inactivo; consulte '
                            'con el Administrador.'
                }
            )
        if not Topic.objects.topic_exists(validated_data['topic'].id):
            raise serializers.ValidationError(
                {
                    'topic': 'Error, el tema enviado no existe o está inactivo, consulte con '
                             'el Administrador.'
                }
            )
        topic_student_evaluation = TopicStudentEvaluation(**validated_data)
        topic_student_evaluation.save()
        return topic_student_evaluation


class TopicStudentEvaluationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicStudentEvaluation
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': {
                'id': instance.user.id,
                'name': instance.user.__str__()
            },
            'type': instance.type,
            'evaluation_body': instance.evaluation_body,
            'final_grade': instance.final_grade,
            'observations': instance.observations,
            'active': instance.active,
            'created_at': instance.created_at
        }
