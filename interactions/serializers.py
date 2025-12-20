from rest_framework import serializers
from .models import Comment, Vote, Bookmark
from accounts.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'commentable_type', 'commentable_id', 'author', 'body', 
                  'is_edited', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'is_edited', 'created_at', 'updated_at']

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['commentable_type', 'commentable_id', 'body']
    
    def validate(self, data):
        
        if data['commentable_type'] not in [1, 2, 3, 4]:
            raise serializers.ValidationError({
                'commentable_type': 'Must be 1=prompt, 2=tool, 3=news, 4=blog'
            })
        return data
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.is_edited = True
        instance.save()
        return instance


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['votable_type', 'votable_id', 'value', 'created_at']
        read_only_fields = ['created_at']


class BookmarkSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    
    class Meta:
        model = Bookmark
        fields = ['bookmarkable_type', 'bookmarkable_id', 'created_at', 'content_object']
    
    def get_content_object(self, obj):
        """Return the actual bookmarked content"""
        try:
            
            content = obj.content_object  
            
            if not content:
                return None
            
            
            if hasattr(content, 'slug'):
                return {
                    'id': str(content.id),
                    'slug': content.slug,
                    'title': getattr(content, 'title', None),
                    'name': getattr(content, 'name', None),
                    'body': getattr(content, 'body', None),
                    'description': getattr(content, 'description', None),
                }
            return None
        except:
            return None
