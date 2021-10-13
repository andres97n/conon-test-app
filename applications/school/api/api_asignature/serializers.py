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
        if not KnowledgeArea.objects.is_active(value.id):
            raise serializers.ValidationError('Error, esta Área de Conocimiento no existe.')
        classroom = Classroom(**validated_data)
        classroom.save()
        return classroom

    # Update Asignature
    def update(self, instance, validated_data):
        if instance.knowledge_area != validated_data['knowledge_area']:
            raise serializers.ValidationError('Error, una vez ingresada el Área de Conocimiento no se puede cambiar el mismo.')
        update_classroom = super().update(instance, validated_data)
        update_classroom.save()
        return update_classroom

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
