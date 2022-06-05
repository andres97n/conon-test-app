from rest_framework import serializers

from applications.school.models import Asignature, KnowledgeArea


class AsignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignature
        exclude = [
            'updated_at',
            'auth_state'
        ]

    # Create a Asignature
    def create(self, validated_data):
        if not KnowledgeArea.objects.is_active(validated_data['knowledge_area'].id):
            raise serializers.ValidationError(
                {
                    'knowledge_area': 'Error, esta Área de Conocimiento no existe.'
                }
            )
        asignature = Asignature(**validated_data)
        asignature.save()
        return asignature

    # Update Asignature
    def update(self, instance, validated_data):
        if instance.knowledge_area != validated_data['knowledge_area']:
            raise serializers.ValidationError(
                {
                    'knowledge_area': 'Error, una vez ingresada el Área de Conocimiento no se '
                                      'puede cambiar el mismo.'
                }
            )
        update_asignature = super().update(instance, validated_data)
        update_asignature.save()
        return update_asignature

    # Return Asignature Data
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'objective': instance.objective,
            'knowledge_area': {
                'id': instance.knowledge_area.id,
                'name': instance.knowledge_area.name,
                'coordinator': instance.knowledge_area.get_coordinator()
            },
            'state': instance.state,
            'observations': instance.observations,
            'created_at': instance.created_at
        }


class AsignatureDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        read_only=True
    )
    classroom = serializers.IntegerField(
        read_only=True
    )
    teacher = serializers.IntegerField(
        read_only=True
    )

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'classroom': instance['classroom_id'],
            'teacher': instance['teacher_id']
        }
