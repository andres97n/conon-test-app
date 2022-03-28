from rest_framework import serializers

from applications.users.models import User, Conversation, Conversation_Detail


class ConversationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation_Detail
        exclude = [
            'auth_state'
        ]

    # Validate State of Conversation
    def validate_state(self, value):
        if value > 2:
            raise serializers.ValidationError(
                {
                    'state': "Error, no se puede guardar este estado."
                }
            )
        return value

    # Validate Owner
    def validate_owner(self, value):
        if not User.objects.user_exists(value.id):
            raise serializers.ValidationError(
                {
                    'owner': 'Error, este Usuario no existe.'
                }
            )
        elif not Conversation.objects.is_owner_in_conversation(value.id):
            raise serializers.ValidationError(
                {
                    'owner': 'Error, este Usuario no pertenece a esta Conversación; consulte '
                            'con el Administrador.'
                }
            )
        elif value != self.context.get('request').user:
            raise serializers.ValidationError(
                {
                    'owner': 'Error, por falta de permisos este usuario no puede mandar este mensaje.'
                }
            )
        return value

    # Validate Conversation
    def validate_conversation(self, value):
        if not Conversation.objects.conversation_exists(value.id):
            raise serializers.ValidationError(
                {
                    'conversation': 'Error, no se puede enviar este mensaje; '
                                    'consulte con el Administrador.'
                }
            )
        return value

'''
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
'''


class ConversationDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation_Detail
        exclude = [
            'auth_state'
        ]

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'conversation': instance.conversation.id,
            'owner': {
                'id': instance.owner.id,
                'name': instance.owner.__str__()
            },
            'detail': instance.detail,
            'state': instance.state,
            'blocked': instance.blocked,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
