import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tags'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Taggable(models.Model):
    """
    Polymorphic tagging system
    Type mapping: 1=prompts, 2=tools, 3=news, 4=blogs
    """
    TAGGABLE_TYPES = [
        (1, 'Prompt'),
        (2, 'Tool'),
        (3, 'News'),
        (4, 'Blog'),
    ]
    
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='taggables')
    taggable_type = models.IntegerField(choices=TAGGABLE_TYPES)
    taggable_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'taggables'
        unique_together = ['tag', 'taggable_type', 'taggable_id']
        indexes = [
            models.Index(fields=['taggable_type', 'taggable_id']),
            models.Index(fields=['tag']),
        ]
    
    def __str__(self):
        return f"{self.tag.name} -> {self.get_taggable_type_display()}#{self.taggable_id}"
    
    def clean(self):
        if self.taggable_type not in [1, 2, 3, 4]:
            raise ValidationError('Invalid taggable_type')