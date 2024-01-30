from rest_framework import serializers
from .models import Property, PropertyTag

class PropertyTagSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()

    class Meta:
        model = PropertyTag 
        fields = ('pk', 'name', 'property_keywords')
        depth = 1

class PropertySerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    parent_property = serializers.IntegerField(allow_null=True)
    parent_property_name = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Property 
        fields = ('pk', 'name', 'description', 'parent_property', 'parent_property_name', 'property_tags')
        depth = 1

    def to_representation(self, instance):
        property = {}
        property["pk"] = instance.pk
        property["name"] = instance.name
        property["description"] = instance.description
        
        if instance.parent_property is not None:
            property["parent_property"] = instance.parent_property.pk
            property["parent_property_name"] = instance.parent_property.name
        else:
            property["parent_property"] = None
            property["parent_property_name"] = None
        
        property["property_tags"] = instance.property_tags


        data = super(PropertySerializer, self).to_representation(property)
        return data

    def get_or_create_property_tags(self, property_tags):
        property_tags_ids = []
        for property_tag in property_tags_ids:
            property_tag_instance, created = PropertyTag.objects.get_or_create(pk=property_tag.get('pk'), defaults=property_tag)
            property_tags_ids.append(property_tag_instance.pk)
        return property_tags_ids

    def create_or_update_property_tags(self, property_tags):
        property_tags_ids = []
        for property_tag in property_tags_ids:
            property_tag_instance, created = PropertyTag.objects.update_or_create(pk=property_tag.get('pk'), defaults=property_tag)
            property_tags_ids.append(property_tag_instance.pk)
        return property_tags_ids
    
    def update(self, instance, validated_data):
        parent_property_data = validated_data.pop('parent_property')
        property_tag_data = validated_data.pop('property_tag', [])

        instance.name = validated_data["name"]
        instance.description = validated_data["description"]

        if parent_property_data is not None:
            instance.parent_property_id = Property.objects.get(pk=parent_property_data)
        else:
            instance.parent_property = None

        instance.property_tags.set(self.create_or_update_property_tags(property_tag_data)) 

        instance.save()
        # ... plus any other fields you may want to update
        return instance
    
    def create(self, validated_data):
        parent_property_data = validated_data.pop('parent_property')
        validated_data.pop('parent_property_name')
        property_tag_data = validated_data.pop('property_tag', [])
        
        if parent_property_data is not None:
            parent_property = Property.objects.get(pk=parent_property_data)
        else:
            parent_property = None

        property = Property.objects.create(parent_property=parent_property, **validated_data)
        property.property_tags.set(self.get_or_create_property_tags(property_tag_data))
        
        return property