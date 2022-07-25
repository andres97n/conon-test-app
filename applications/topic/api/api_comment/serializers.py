from rest_framework import serializers

from applications.topic.models import Comment, Topic
from applications.users.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = [
            'auth_state',
        ]

    # Create Comment
    def create(self, validated_data):
        if not User.objects.user_exists(validated_data['owner'].id):
            raise serializers.ValidationError(
                {
                    'owner': 'Error, el siguiente Usuario no existe.'
                }
            )
        if Comment.objects.title_exists(validated_data['topic'].id, validated_data['title']):
            raise serializers.ValidationError(
                {
                    'title': 'Error, el siguiente Título ya existe, por favor ingrese otro.'
                }
            )
        comment = Comment(**validated_data)
        comment.save()
        return comment

    # Update Comment
    def update(self, instance, validated_data):
        if instance.topic != validated_data['topic']:
            raise serializers.ValidationError(
                {
                    'topic': 'Error, no se puede cambiar el Tema de Estudio.'
                }
            )
        if instance.owner != validated_data['owner']:
            raise serializers.ValidationError(
                {
                    'owner': 'Error, no se puede cambiar el Usuario.'
                }
            )
        if instance.title != validated_data['title']:
            if Comment.objects.title_exists(instance.id, validated_data['title']):
                raise serializers.ValidationError(
                    {
                        'title': 'Error, el siguiente Título ya existe, por favor ingrese otro.'
                    }
                )
        update_comment = super().update(instance, validated_data)
        update_comment.save()
        return update_comment

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'topic': {
                'id': instance.topic.id,
                'title': instance.topic.__str__()
            },
            'owner': {
                'id': instance.owner.id,
                'name': instance.owner.__str__()
            },
            'title': instance.title,
            'created_at': instance.created_at,
            'wrong_use': instance.wrong_use,
            'state': instance.state
        }
