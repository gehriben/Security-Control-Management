from rest_framework import serializers
from .models import Tag, Keyword

class KeywordSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()

    class Meta:
        model = Keyword 
        fields = ('pk', 'name')
        depth = 1

class TagSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    keywords = KeywordSerializer(allow_null=True, many=True)

    class Meta:
        model = Tag 
        fields = ('pk', 'name', 'description', 'keywords')
        depth = 1
    
    def get_or_create_keywords(self, keywords):
        keyword_ids = []
        for keyword in keywords:
            keyword_instance, created = Keyword.objects.get_or_create(pk=keyword.get('pk'), defaults=keyword)
            keyword_ids.append(keyword_instance.pk)
        return keyword_ids

    def create_or_update_keywords(self, keywords):
        keyword_ids = []
        for keyword in keywords:
            keyword_instance, created = Keyword.objects.update_or_create(pk=keyword.get('pk'), defaults=keyword)
            keyword_ids.append(keyword_instance.pk)
        return keyword_ids
    
    def update(self, instance, validated_data):
        keyword_data = validated_data.pop('keywords', [])

        instance.name = validated_data["name"]
        instance.description = validated_data["description"]
        instance.keywords.set(self.create_or_update_keywords(keyword_data)) 

        instance.save()
        # ... plus any other fields you may want to update
        return instance
    
    def create(self, validated_data):
        keyword_data = validated_data.pop('keywords', [])
        
        tag = Tag.objects.create( **validated_data)
        tag.keywords.set(self.get_or_create_keywords(keyword_data))
        
        return tag
        # ... plus any other fields you may want to update