from django.contrib import admin
from .models import Comment, Vote, Bookmark


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'commentable_type', 'body_preview', 'created_at']
    list_filter = ['commentable_type', 'is_edited', 'created_at']
    search_fields = ['body', 'author__username']
    raw_id_fields = ['author']

    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'votable_type', 'value', 'created_at']
    list_filter = ['votable_type', 'value', 'created_at']
    raw_id_fields = ['user']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'bookmarkable_type', 'created_at']
    list_filter = ['bookmarkable_type', 'created_at']
    raw_id_fields = ['user']
