from rest_framework import serializers

from applications.topic.models import Reply, Comment
from applications.users.models import User


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create Reply
    def create(self, validated_data):
        if not Comment.objects.comment_exists(validated_data['comment'].id):
            raise serializers.ValidationError(
                {
                    'comment': 'Error, el siguiente Comentario no existe.'
                }
            )
        if not User.objects.user_exists(validated_data['owner'].id):
            raise serializers.ValidationError(
                {
                    'owner': 'Error, el siguiente Usuario no existe.'
                }
            )
        reply = Reply(**validated_data)
        reply.save()
        return reply

    # Update Reply
    def update(self, instance, validated_data):
        if instance.comment != validated_data['comment']:
            raise serializers.ValidationError(
                {
                    'comment': 'Error, no se puede cambiar de Comentario.'
                }
            )
        if instance.owner != validated_data['owner']:
            raise serializers.ValidationError(
                {
                    'owner': 'Error, no se puede cambiar el Usuario.'
                }
            )
        update_reply = super().update(instance, validated_data)
        update_reply.save()
        return update_reply

    # Return Reply Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'comment': {
              'id': instance.comment.id,
              'title': instance.comment.title
            },
            'owner': {
                'id': instance.owner.id,
                'name': instance.owner.__str__()
            },
            'detail': instance.detail,
            'wrong_use': instance.wrong_use,
            'state': instance.state,
            'created_at': instance.created_at
        }
