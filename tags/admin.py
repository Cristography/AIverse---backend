from django.contrib import admin
from .models import Tag, Taggable


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'usage_count']
    search_fields = ['name']

    def usage_count(self, obj):
        return Taggable.objects.filter(tag=obj).count()


@admin.register(Taggable)
class TaggableAdmin(admin.ModelAdmin):
    list_display = ['tag', 'taggable_type', 'taggable_id', 'created_at']
    list_filter = ['taggable_type']
    raw_id_fields = ['tag']
