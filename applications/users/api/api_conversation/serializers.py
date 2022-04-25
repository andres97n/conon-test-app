from rest_framework import serializers

from applications.users.models import Conversation, User


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Validate State of Conversation
    def validate_state(self, value):
        if value > 1:
            raise serializers.ValidationError(
                {
                    'state': "Error, no se puede guardar este estado."
                }
            )
        return value

    # Validate First User
    def validate_first_user(self, value):
        if not User.objects.user_exists(value.id):
            raise serializers.ValidationError(
                detail='Error, este Usuario no existe.'
            )
        return value

    # Validate Second User
    def validate_second_user(self, value):
        if not User.objects.user_exists(pk=value.id):
            raise serializers.ValidationError(
                detail='Error, este Usuario no existe.'
            )
        return value

    # Validate All Conversation data
    def validate(self, attrs):
        if attrs['first_user'].id == attrs['second_user'].id:
            raise serializers.ValidationError(
                detail='Error, no se pueden envíar mensajes al mismo Usuario.'
            )

        return attrs

    # Create Conversation
    def create(self, validated_data):
        if not Conversation.objects.are_users_in_conversation(
                pk_1=validated_data['first_user'].id,
                pk_2=validated_data['second_user'].id
        ):
            raise serializers.ValidationError(
                detail='Error, ya existe esta Conversación.'
            )
        conversation = Conversation(**validated_data)
        conversation.save()
        return conversation
'''
    # Update Conversation
    def update(self, instance, validated_data):
        if instance.first_user != validated_data['first_user']:
            raise serializers.ValidationError(
                detail='Error, no se puede cambiar el Usuario de esta conversación; '
                       'consulte con el Administrador.'
            )
        if instance.second_user != validated_data['second_user']:
            raise serializers.ValidationError(
                detail='Error, no se puede cambiar el Usuario de esta conversación; '
                       'consulte con el Administrador.'
            )
        update_conversation = super().update(instance, validated_data)
        update_conversation.save()
        return update_conversation
'''


class ConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        exclude = [
            'auth_state'
        ]

    # Get Conversation
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'first_user': {
                'id': instance.first_user.id,
                'name': instance.first_user.__str__()
            },
            'second_user': {
                'id': instance.second_user.id,
                'name': instance.second_user.__str__()
            },
            'state': instance.state,
            'blocked': instance.blocked,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }


class ConversationFirstUserShortListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': instance.second_user.id,
            'state': instance.state,
            'blocked': instance.blocked,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }


class ConversationSecondUserShortListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': instance.first_user.id,
            'state': instance.state,
            'blocked': instance.blocked,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
