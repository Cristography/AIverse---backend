from django.contrib import admin
from .models import Prompt, PromptRelation, MediaAsset


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'author', 'views', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['title', 'body', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']


@admin.register(PromptRelation)
class PromptRelationAdmin(admin.ModelAdmin):
    list_display = ['source_prompt', 'target_prompt', 'relation_type']
    list_filter = ['relation_type']
    raw_id_fields = ['source_prompt', 'target_prompt']


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['prompt', 'format', 'created_at','storage_path']
    list_filter = ['format']
    raw_id_fields = ['prompt']
