from rest_framework import serializers
from .models import Blog, News, Tool, ToolType
from accounts.serializers import UserSerializer
from tags.models import Taggable, Tag


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content',
                  'author', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'author', 'created_at', 'updated_at']

    def get_tags(self, obj):
        taggables = Taggable.objects.filter(
            taggable_type=4, taggable_id=obj.id).select_related('tag')
        return [t.tag.name for t in taggables]


class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Blog
        fields = ['title', 'content', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        blog = Blog.objects.create(**validated_data)

        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
            Taggable.objects.create(
                tag=tag, taggable_type=4, taggable_id=blog.id)

        return blog

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            Taggable.objects.filter(
                taggable_type=4, taggable_id=instance.id).delete()
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
                Taggable.objects.create(
                    tag=tag, taggable_type=4, taggable_id=instance.id)

        return instance


class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'content',
                  'author', 'tags', 'created_at', 'updated_at','views']
        read_only_fields = ['id', 'slug', 'author', 'created_at', 'updated_at']

    def get_tags(self, obj):
        taggables = Taggable.objects.filter(
            taggable_type=3, taggable_id=obj.id).select_related('tag')
        return [t.tag.name for t in taggables]


class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = News
        fields = ['title', 'content', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        news = News.objects.create(**validated_data)

        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
            Taggable.objects.create(
                tag=tag, taggable_type=3, taggable_id=news.id)

        return news

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            Taggable.objects.filter(
                taggable_type=3, taggable_id=instance.id).delete()
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
                Taggable.objects.create(
                    tag=tag, taggable_type=3, taggable_id=instance.id)

        return instance


class ToolTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolType
        fields = ['id', 'name', 'description']


class ToolSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    type = ToolTypeSerializer(read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Tool
        fields = ['id', 'name', 'slug', 'description', 'url',
                  'type', 'author', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'author', 'created_at', 'updated_at']

    def get_tags(self, obj):
        taggables = Taggable.objects.filter(
            taggable_type=2, taggable_id=obj.id).select_related('tag')
        return [t.tag.name for t in taggables]


class ToolCreateUpdateSerializer(serializers.ModelSerializer):
    type_id = serializers.UUIDField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Tool
        fields = ['name', 'description', 'url', 'type_id', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        type_id = validated_data.pop('type_id', None)

        if type_id:
            validated_data['type_id'] = type_id

        tool = Tool.objects.create(**validated_data)

        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
            Taggable.objects.create(
                tag=tag, taggable_type=2, taggable_id=tool.id)

        return tool

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        type_id = validated_data.pop('type_id', None)

        if type_id:
            instance.type_id = type_id

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            Taggable.objects.filter(
                taggable_type=2, taggable_id=instance.id).delete()
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
                Taggable.objects.create(
                    tag=tag, taggable_type=2, taggable_id=instance.id)

        return instance
