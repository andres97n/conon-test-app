from rest_framework import serializers

from applications.topic.models import Comment, Topic
from applications.users.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = [
            'auth_state',
        ]

    error = {
        'ok': False,
        'detail': ''
    }

    # Create Comment
    def create(self, validated_data):
        if not Topic.objects.topic_exists(validated_data['topic'].id):
            self.error['detail']: 'Error, el siguiente Tema no existe.'
            raise serializers.ValidationError(
                detail=self.error
            )
        if not User.objects.user_exists(validated_data['owner'].id):
            self.error['detail'] = 'Error, el siguiente Usuario no existe.'
            raise serializers.ValidationError(
                detail=self.error
            )
        if Comment.objects.title_exists(validated_data['topic'].id, validated_data['title']):
            self.error['detail'] = 'Error, el siguiente Título ya existe, por favor ingrese otro.'
            raise serializers.ValidationError(
                detail=self.error
            )
        comment = Comment(**validated_data)
        comment.save()
        return comment

    # Update Comment
    def update(self, instance, validated_data):
        if instance.topic != validated_data['topic']:
            self.error['detail'] = 'Error, no se puede cambiar el Tema de Estudio.'
            raise serializers.ValidationError(
                detail=self.error
            )
        if instance.owner != validated_data['owner']:
            self.error['detail'] = 'Error, no se puede cambiar el Usuario.'
            raise serializers.ValidationError(
                detail=self.error
            )
        if instance.title != validated_data['title']:
            self.error['detail'] = 'Error, el siguiente Título ya existe, por favor ingrese otro.'
            if Comment.objects.title_exists(instance.id, validated_data['title']):
                raise serializers.ValidationError(
                    detail=self.error
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
            'detail': instance.detail,
            'created_at': instance.created_at,
            'end_at': instance.end_at,
            'wrong_use': instance.wrong_use,
            'state': instance.state
        }
