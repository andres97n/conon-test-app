from rest_framework import serializers

from applications.school.models import GlosaryDetail, Glosary


class GlosaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlosaryDetail
        exclude = [
            'auth_state'
        ]

    # Create a Term
    def create(self, validated_data):
        if not Glosary.objects.glosary_exists(attrs['glosary'].id):
            raise serializers.ValidationError(
                detail='Error, no se encuentra relación con este valor; consulte con el Administrador.'
            )
        if GlosaryDetail.objects.title_exists(attrs['glosary'].id, attrs['title']):
            raise serializers.ValidationError(
                detail='Error, este Glosario ya contiene este término.'
            )
        knowledge_area = KnowledgeArea(**validated_data)
        knowledge_area.save()
        return knowledge_area

    # Update Glosary Detail
    def update(self, instance, validated_data):
        if instance.glosary != validated_data['glosary']:
            raise serializers.ValidationError(
                detail='Error, no se puede cambiar la relación de este registro; '
                       'consulte con el Administrador.'
            )
        if instance.title != validated_data['title']:
            if GlosaryDetail.objects.title_exists(attrs['glosary'].id, attrs['title']):
                raise serializers.ValidationError(
                    detail='Error, este Glosario ya contiene este término.'
                )
        update_glosary_detail = super().update(instance, validated_data)
        update_glosary_detail.save()
        return update_glosary_detail

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'glosary_id': instance.glosary.id,
            'title': instance.title,
            'description': instance.description,
            'image': instance.image,
            'url': instance.url,
            'observation': instance.observation,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }
