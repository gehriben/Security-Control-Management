from rest_framework import serializers
from .models import Control
from tags.models import Tag
from tags.serializers import TagSerializer

class ControlSerializer(serializers.ModelSerializer):
    parent_control = serializers.IntegerField(allow_null=True)
    parent_control_name = serializers.CharField(allow_null=True)
    tags = TagSerializer(allow_null=True, many=True)


    class Meta:
        model = Control 
        fields = ('pk', 'cn', 'name', 'description', 'parent_control', 'parent_control_name', 'tags')
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
            tag_instance, created = Tag.objects.update_or_create(pk=tag.get('pk'), defaults=tag)
            tag_ids.append(tag_instance.pk)
        return tag_ids
    
    def to_representation(self, instance):
        control = {}
        control["pk"] = instance.pk
        control["cn"] = instance.cn
        control["name"] = instance.name
        control["description"] = instance.description
        
        if instance.parent_control is not None:
            control["parent_control"] = instance.parent_control.pk
            control["parent_control_name"] = instance.parent_control.name
        else:
            control["parent_control"] = None
            control["parent_control_name"] = None

        control["tags"] = instance.tags

        data = super(ControlSerializer, self).to_representation(control)
        return data
    
    def update(self, instance, validated_data):
        parent_control_data = validated_data.pop('parent_control')
        tag_data = validated_data.pop('tags', [])

        fields = ['cn', 'name', 'description']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass

        if parent_control_data is not None:
            instance.parent_control_id = Control.objects.get(pk=parent_control_data)
        else:
            instance.parent_control = None
        
        instance.tags.set(self.create_or_update_tags(tag_data))           
        
        instance.save()
        return instance
    
    def create(self, validated_data):
        parent_control_data = validated_data.pop('parent_control')
        tag_data = validated_data.pop('tags', [])

        if parent_control_data is not None:
            parent_control = Control.objects.get(pk=parent_control_data)
        else:
            parent_control = None

        control = Control.objects.create(parent_control=parent_control, **validated_data)
        control.tags.set(self.get_or_create_tags(tag_data))
        
        return control