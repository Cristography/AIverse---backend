import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Prompt(models.Model):
    PROMPT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('music', 'Music'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=PROMPT_TYPES)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField(help_text='The actual prompt text')
    context = models.JSONField(blank=True, null=True, help_text='Type-specific parameters')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prompts')
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'prompts'
        unique_together = ['slug', 'type']
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['author']),
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.type})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def vote_count(self):
        from interactions.models import Vote
        return Vote.objects.filter(
            votable_type=1, 
            votable_id=self.id
        ).aggregate(
            total=models.Sum('value')
        )['total'] or 0

class PromptRelation(models.Model):
    RELATION_TYPES = [
        ('variation', 'Variation'),
        ('improved_version', 'Improved Version'),
        ('similar_style', 'Similar Style'),
        ('inspired_by', 'Inspired By'),
        ('related', 'Related'),
    ]
    
    source_prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='relations_from')
    target_prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='relations_to')
    relation_type = models.CharField(max_length=50, choices=RELATION_TYPES, default='related')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'prompt_relations'
        unique_together = ['source_prompt', 'target_prompt', 'relation_type']
        indexes = [
            models.Index(fields=['source_prompt']),
            models.Index(fields=['target_prompt']),
        ]
    
    def __str__(self):
        return f"{self.source_prompt.title} -> {self.target_prompt.title} ({self.relation_type})"

class MediaAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='media_assets')
    storage_path = models.TextField(help_text='e.g., s3://bucket/images/abc123.png')
    format = models.CharField(max_length=10, help_text='png, jpg, mp3, etc.')
    metadata = models.JSONField(blank=True, null=True, help_text='Width, duration, etc.')
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        db_table = 'media_assets'
        indexes = [
            models.Index(fields=['prompt']),
        ]