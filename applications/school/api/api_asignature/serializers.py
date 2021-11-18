from rest_framework import serializers

from applications.school.models import Asignature, KnowledgeArea


class AsignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignature
        exclude = [
            'created_at',
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
                    'knowledge_area': 'Error, una vez ingresada el Área de Conocimiento no se puede cambiar el mismo.'
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
                'name': instance.knowledge_area.name,
                'coordinator': instance.knowledge_area.get_coordinator()
            },
            'observations': instance.observations,
            # classrooms = instance.classrooms
        }
