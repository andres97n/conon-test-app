from rest_framework import serializers

from applications.dua.models import Question, Activity


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = [
            'updated_at',
            'auth_state'
        ]

    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                {
                    'value': 'Error, la siguiente pregunta no puede tener un valor negativo.'
                }
            )
        return value

    # Create A Question
    def create(self, validated_data):
        if not Activity.objects.activity_exists(validated_data['activity'].id):
            raise serializers.ValidationError(
                {
                    'activity': 'Error, no se puede crear esta Pregunta; por favor '
                                'consulte con el Administrador.'
                }
            )
        question = Question(**validated_data)
        question.save()
        return question

    # Update Question
    def update(self, instance, validated_data):
        if instance.activity != validated_data['activity']:
            raise serializers.ValidationError(
                {
                    'activity': 'Error, no se puede editar esta Pregunta; '
                                'por favor consulte con el Administrador.'
                }
            )
        update_question = super().update(instance, validated_data)
        update_question.save()
        return update_question

    # Get A Question List
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'activity': {
                'id': instance.activity.id,
                'description': instance.activity.description
            },
            'title': instance.title,
            'answers': instance.answers,
            'value': instance.value,
            'active': instance.active,
            'created_at': instance.created_at
        }


class QuestionByActivitySerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'answers': instance.answers,
            'value': instance.value,
            'active': instance.active,
            'created_at': instance.created_at
        }
