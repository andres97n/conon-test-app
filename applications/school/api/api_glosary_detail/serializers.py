from rest_framework import serializers

from applications.school.models import GlosaryDetail, Glosary


class GlosaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlosaryDetail
        exclude = [
            'auth_state'
        ]

    def validate(self, attrs):
        if not GlosaryDetail.objects.title_exists(
            pk=attrs['glosary'].id,
            title=attrs['title']
        ):
            raise serializers.ValidationError(
                detail='Error, este Glosario ya contiene este término.'
            )
        return attrs

    # Create a Glosary Detail
    def create(self, validated_data):
        if not Glosary.objects.glosary_exists(validated_data['glosary'].id):
            raise serializers.ValidationError(
                detail='Error, no se encuentra relación con este valor; consulte con el Administrador.'
            )
        glosary = Glosary(**validated_data)
        glosary.save()
        return glosary

    # Update Glosary Detail
    def update(self, instance, validated_data):
        if instance.glosary != validated_data['glosary']:
            raise serializers.ValidationError(
                detail='Error, no se puede cambiar la relación de este registro; '
                       'consulte con el Administrador.'
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
