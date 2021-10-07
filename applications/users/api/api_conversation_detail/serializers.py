from rest_framework import serializers

from applications.users.models import User, Conversation, Conversation_Detail


class ConversationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation_Detail
        exclude = [
            'created_at',
            'updated_at',
            'auth_state'
        ]

    # Validate State of Conversation
    def validate_state(self, value):
        if value > 1:
            raise serializers.ValidationError(
                detail="Error, no se puede guardar este estado."
            )
        return value

    # Validate Owner
    def validate_owner(self, value):
        if not User.objects.user_exists(value.id):
            raise serializers.ValidationError(
                detail='Error, este Usuario no existe.'
            )
        return value

    # Validate Conversation
    def validate_conversation(self, value):
        if not Conversation.objects.conversation_exists(value.id):
            raise serializers.ValidationError(
                detail='Error, no se puede enviar este mensaje; consulte con el Administrador.'
            )
        return value

    # Validate All data
    def validate(self, attrs):
        if not Conversation_Detail.objects.is_owner_in_conversation(
                attrs['conversation'].id,
                attrs['owner'].id
        ):
            raise serializers.ValidationError(
                detail='Error, este Usuario no puede enviar este mensaje; consulte con el Administrador.'
            )
        if attrs['owner'] != self.context.get('request').user:
            raise serializers.ValidationError(
                detail='Error, por falta de permisos este usuario no puede mandar este mensaje.'
            )
        return attrs

    # Update Conversation Detail
    def update(self, instance, validated_data):
        if instance.conversation != validated_data['conversation']:
            raise serializers.ValidationError('Error, no se puede cambiar de conversación; '
                                              'consulte con el Administrador.')
        if instance.owner != validated_data['owner']:
            raise serializers.ValidationError('Error, no se puede cambiar de remitente; consulte con el Administrador.')
        update_conversation = super().update(instance, validated_data)
        update_conversation.save()
        return update_conversation

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'conversation': instance.conversation.id,
            'owner': {
                'id': instance.owner.id,
                'name': instance.owner.__str__()
            },
            'detail': instance.detail,
            'send_date': instance.send_date,
            'state': instance.state,
            'blocked': instance.blocked
        }
