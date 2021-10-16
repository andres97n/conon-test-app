from rest_framework import serializers

from applications.dua.models import Answer, ActivityStudent, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError(
                detail='Error, el valor de la respuesta no puede ser un número negativo.'
            )

        return value

    # Create Answer
    def create(self, validated_data):
        if not ActivityStudent.objects. \
                activity_student_exists(validated_data['activity_student'].id):
            raise serializers.ValidationError(
                detail='Error, no se pudo guardar su respuesta; '
                       'por favor consulte con el Administrador.'
            )
        if not Question.objects. \
                question_exists(validated_data['question'].id):
            raise serializers.ValidationError(
                detail='Error, no se puede encontrar a la Pregunta asociada; por favor '
                       'contacte con el Administrador.'
            )
        answer = Answer(**validated_data)
        answer.save()
        return answer

    # Update Question
    def update(self, instance, validated_data):
        if instance.activity_student != validated_data['activity_student']:
            raise serializers.ValidationError(
                detail='Error, no se puede editar esta Respuesta; '
                       'por favor consulte con el Administrador '
            )
        if instance.question != validated_data['question']:
            raise serializers.ValidationError(
                detail='Error, no se puede cambiar la pregunta asociada con esta respuesta '
                       'por favor consulte con el Administrador '
            )
        update_answer = super().update(instance, validated_data)
        update_answer.save()
        return update_answer

    # Get Answer List
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'activity_student': {
                'id': instance.activity_student.id,
                'name': instance.activity_student.__str__()
            },
            'question': {
                'id': instance.question.id,
                'title': instance.question.title
            },
            'detail': instance.detail,
            'value': instance.value,
            'created_at': instance.created_at
        }
