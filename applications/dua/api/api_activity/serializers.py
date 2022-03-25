from rest_framework import serializers

from applications.dua.models import Dua, Activity


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Validate State
    def validate_state(self, value):
        if value > 1:
            raise serializers.ValidationError(
                {
                    'state': 'Error, no se puede asignar este Estado a este metodología.'
                }
            )
        return value

    # Create Activity
    def create(self, validated_data):
        if not Dua.objects.exists_dua(validated_data['dua'].id):
            raise serializers.ValidationError(
                {
                    'dua': 'Error, no se puede crear esta Actividad; consulte con el Administrador.'
                }
            )
        activity = Activity(**validated_data)
        activity.save()
        return activity

    # Update Activity
    def update(self, instance, validated_data):
        if instance.dua != validated_data['dua']:
            raise serializers.ValidationError(
                {
                    'dua': 'Error, no es posible editar esta Actividad; por favor '
                           'consulte con el Administrador.'
                }
            )
        update_activity = super().update(instance, validated_data)
        update_activity.save()
        return update_activity

    # Return Activity Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'dua': {
                'id': instance.dua.id,
                'topic': {
                    'id': instance.dua.topic.id,
                    'title': instance.dua.topic.title
                }
            },
            'description': instance.description,
            'objective': instance.objective,
            'final_grade': instance.final_grade,
            'state': instance.state,
            'created_at': instance.created_at
        }


class ActivityDetailSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['question'],
            'title': instance['question__title'],
            'answers': instance['question__answers'],
            'value': instance['question__value']
        }


class ActivityByDuaSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'description': instance.description,
            'objective': instance.objective,
            'final_grade': instance.final_grade,
            'state': instance.state,
            'created_at': instance.created_at
        }
