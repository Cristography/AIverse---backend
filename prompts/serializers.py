from rest_framework import serializers
from .models import Prompt, PromptRelation, MediaAsset
from accounts.serializers import UserSerializer
from tags.models import Taggable, Tag

class PromptSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    vote_count = serializers.ReadOnlyField()
    tags = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Prompt
        fields = ['id', 'type', 'title', 'slug', 'body', 'context', 
                  'author', 'views', 'vote_count', 'tags', 'is_bookmarked',
                  'user_vote', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'author', 'views', 'created_at', 'updated_at']
    
    def get_tags(self, obj):
        taggables = Taggable.objects.filter(taggable_type=1, taggable_id=obj.id).select_related('tag')
        return [t.tag.name for t in taggables]
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from interactions.models import Bookmark
            return Bookmark.objects.filter(
                user=request.user,
                bookmarkable_type=1,
                bookmarkable_id=obj.id
            ).exists()
        return False
    
    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from interactions.models import Vote
            vote = Vote.objects.filter(
                user=request.user,
                votable_type=1,
                votable_id=obj.id
            ).first()
            return vote.value if vote else None
        return None

class PromptCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Prompt
        fields = ['type', 'title', 'body', 'context', 'tags']
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        prompt = Prompt.objects.create(**validated_data)
        
        # Handle tags
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
            Taggable.objects.create(tag=tag, taggable_type=1, taggable_id=prompt.id)
        
        return prompt
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        
        # Update prompt fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update tags if provided
        if tags_data is not None:
            Taggable.objects.filter(taggable_type=1, taggable_id=instance.id).delete()
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
                Taggable.objects.create(tag=tag, taggable_type=1, taggable_id=instance.id)
        
        return instance

class PromptRelationSerializer(serializers.ModelSerializer):
    source_prompt = PromptSerializer(read_only=True)
    target_prompt = PromptSerializer(read_only=True)
    
    class Meta:
        model = PromptRelation
        fields = ['source_prompt', 'target_prompt', 'relation_type', 'created_at']