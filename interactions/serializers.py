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
    class Meta:
        model = Bookmark
        fields = ['bookmarkable_type', 'bookmarkable_id', 'created_at']
        read_only_fields = ['created_at']