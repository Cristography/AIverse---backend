import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.apps import apps

class Comment(models.Model):
    """
    Polymorphic comments
    Type mapping: 1=prompts, 2=tools, 3=news, 4=blogs
    """
    COMMENTABLE_TYPES = [
        (1, 'Prompt'),
        (2, 'Tool'),
        (3, 'News'),
        (4, 'Blog'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commentable_type = models.IntegerField(choices=COMMENTABLE_TYPES)
    commentable_id = models.UUIDField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        indexes = [
            models.Index(fields=['commentable_type', 'commentable_id']),
            models.Index(fields=['author']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.get_commentable_type_display()}"
    


class Bookmark(models.Model):
    """
    Polymorphic bookmarks
    Type mapping: 1=prompts, 2=tools, 3=news, 4=blogs
    """
    BOOKMARKABLE_TYPES = [
        (1, 'Prompt'),
        (2, 'Tool'),
        (3, 'News'),
        (4, 'Blog'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    bookmarkable_type = models.IntegerField(choices=BOOKMARKABLE_TYPES)
    bookmarkable_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bookmarks'
        unique_together = ['user', 'bookmarkable_type', 'bookmarkable_id']
        indexes = [
            models.Index(fields=['bookmarkable_type', 'bookmarkable_id']),
        ]
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.get_bookmarkable_type_display()}"
    
    def clean(self):
        if self.bookmarkable_type not in [1, 2, 3, 4]:
            raise ValidationError('Invalid bookmarkable_type')

    def get_content_object(self):
        """Resolve and return the actual bookmarked object instance (or None)."""
        try:
            model_map = {
                1: 'prompts.Prompt',
                2: 'content.Tool',
                3: 'content.News',
                4: 'content.Blog',
            }
            model_label = model_map.get(self.bookmarkable_type)
            if not model_label:
                return None
            Model = apps.get_model(model_label)
            if not Model:
                return None
            return Model.objects.filter(pk=self.bookmarkable_id).first()
        except Exception:
            return None

    @property
    def content_object(self):
        return self.get_content_object()

class Vote(models.Model):
    """
    Polymorphic voting
    Type mapping: 1=prompts, 2=tools, 3=news, 4=blogs
    """
    VOTABLE_TYPES = [
        (1, 'Prompt'),
        (2, 'Tool'),
        (3, 'News'),
        (4, 'Blog'),
    ]
    
    VOTE_VALUES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    votable_type = models.IntegerField(choices=VOTABLE_TYPES)
    votable_id = models.UUIDField()
    value = models.IntegerField(choices=VOTE_VALUES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    prompts = models.ForeignKey('prompts.Prompt', null=True, blank=True, on_delete=models.CASCADE)
    tool = models.ForeignKey('content.Tool', null=True, blank=True, on_delete=models.CASCADE)
    news = models.ForeignKey('content.News', null=True, blank=True, on_delete=models.CASCADE)
    blog = models.ForeignKey('content.Blog', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'votes'
        unique_together = ['user', 'votable_type', 'votable_id']
        indexes = [
            models.Index(fields=['votable_type', 'votable_id']),
        ]
    
    def __str__(self):
        vote_type = 'upvoted' if self.value == 1 else 'downvoted'
        return f"{self.user.username} {vote_type} {self.get_votable_type_display()}"
    
    def clean(self):
        if self.votable_type not in [1, 2, 3, 4]:
            raise ValidationError('Invalid votable_type')
        if self.value not in [1, -1]:
            raise ValidationError('Vote value must be 1 or -1')