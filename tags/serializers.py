from rest_framework import serializers
from .models import Tag, Taggable

class TagSerializer(serializers.ModelSerializer):
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'usage_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_usage_count(self, obj):
        return Taggable.objects.filter(tag=obj).count()

class TaggableSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(source='tag.name', read_only=True)
    
    class Meta:
        model = Taggable
        fields = ['tag', 'tag_name', 'taggable_type', 'taggable_id', 'created_at']
        read_only_fields = ['created_at']