from rest_framework import serializers
from .models import Asset, Assettype, AssetControlMatch
from tags.models import Tag
from tags.serializers import TagSerializer
from properties.models import Property
from properties.serializers import PropertySerializer
from controls.models import Control
from controls.serializers import ControlSerializer

class AssettypeSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()

    class Meta:
        model = Assettype
        fields = ('pk', 'name')

class AssetSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    assettype = AssettypeSerializer()
    tags = TagSerializer(allow_null=True, many=True)
    properties = PropertySerializer(allow_null=True, many=True)

    class Meta:
        model = Asset 
        fields = ('pk', 'name', 'description', 'assettype', 'tags', 'properties')
        depth = 1
    
    def get_or_create_tags(self, tags):
        tag_ids = []
        for tag in tags:
            tag_instance, created = Tag.objects.get_or_create(pk=tag.get('pk'), defaults=tag)
            tag_ids.append(tag_instance.pk)
        return tag_ids

    def create_or_update_tags(self, tags):
        tag_ids = []
        for tag in tags:
            tag_instance = Tag.objects.get(pk=tag.get('pk'))
            if not tag_instance:
                tag_instance = Tag.objects.create()
            
            serializer = TagSerializer()
            serializer.update(tag_instance, tag)
            # tag_instance, created = Tag.objects.update_or_create(pk=tag.get('pk'), defaults=tag)
            tag_ids.append(tag_instance.pk)
        return tag_ids
    
    def get_or_create_properties(self, properties):
        property_ids = []
        for property in properties:
            property_instance, created = Property.objects.get_or_create(pk=property.get('pk'), defaults=property)
            property_ids.append(property_instance.pk)
        return property_ids

    def create_or_update_properties(self, properties):
        property_ids = []
        for property in properties:
            property.pop("parent_property_name")
            property_instance, created = Property.objects.update_or_create(pk=property.get('pk'), defaults=property)
            property_ids.append(property_instance.pk)
        return property_ids
    
    def update(self, instance, validated_data):
        assettype_data = validated_data.pop('assettype')
        tag_data = validated_data.pop('tags', [])
        property_data = validated_data.pop('properties', [])

        instance.name = validated_data["name"]
        instance.description = validated_data["description"]
        instance.assettype_id = Assettype.objects.get(pk=list(assettype_data.items())[0][1])
        instance.tags.set(self.create_or_update_tags(tag_data)) 
        instance.properties.set(self.create_or_update_properties(property_data)) 

        instance.save()
        # ... plus any other fields you may want to update
        return instance
    
    def create(self, validated_data):
        assettype_data = validated_data.pop('assettype')
        tag_data = validated_data.pop('tags', [])
        property_data = validated_data.pop('properties', [])
        
        assettype = Assettype.objects.get(pk=list(assettype_data.items())[0][1])
        asset = Asset.objects.create(assettype=assettype, **validated_data)
        asset.tags.set(self.get_or_create_tags(tag_data))
        asset.properties.set(self.get_or_create_properties(property_data))
        
        return asset
        # ... plus any other fields you may want to update

class AssetControlMatchSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()
    control = ControlSerializer()

    class Meta:
        model = AssetControlMatch 
        fields = ('pk', 'asset', 'control')
        depth = 1
    
    def update(self, instance, validated_data):
        asset_data = validated_data.pop('asset')
        control_data = validated_data.pop('control')

        instance.asset_id = Asset.objects.get(pk=list(asset_data.items())[0][1])
        instance.control_id = Control.objects.get(pk=list(control_data.items())[0][1])

        instance.save()
        return instance
    
    def create(self, validated_data):
        asset_data = validated_data.pop('asset')
        control_data = validated_data.pop('control')
        
        asset = Asset.objects.get(pk=list(asset_data.items())[0][1])
        control = Control.objects.get(pk=list(control_data.items())[0][1])
            
        asset_control_match = AssetControlMatch.objects.create(asset=asset, control=control)
        
        return asset_control_match