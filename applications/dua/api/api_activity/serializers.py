from rest_framework import serializers

from applications.dua.models import Activity
from applications.topic.models import Topic


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Activity
    def create(self, validated_data):
        if not Topic.objects.topic_exists(validated_data['topic'].id):
            raise serializers.ValidationError(
                detail='Error, no se puede crear esta Actividad; consulte con el Administrador.'
            )
        activity = Dua(**validated_data)
        activity.save()
        return activity

    # Update Activity
    def update(self, instance, validated_data):
        if instance.topic != validated_data['topic']:
            raise serializers.ValidationError('Error, no es posible editar esta Actividad; '
                                              'por favor consulte con el Administrador.')
        update_activity = super().update(instance, validated_data)
        update_activity.save()
        return update_activity

    # Return Activity Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'topic': {
                'id': instance.topic.id,
                'title': instance.topic.title
            },
            'description': instance.description,
            'objective': instance.objective,
            'created_at': instance.created_at
        }
