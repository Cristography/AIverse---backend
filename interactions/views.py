from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Comment, Vote, Bookmark
from .serializers import (
    CommentSerializer, CommentCreateUpdateSerializer,
    VoteSerializer, BookmarkSerializer
)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateUpdateSerializer
        return CommentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        commentable_type = self.request.query_params.get('commentable_type')
        commentable_id = self.request.query_params.get('commentable_id')
        
        if commentable_type and commentable_id:
            queryset = queryset.filter(
                commentable_type=commentable_type,
                commentable_id=commentable_id
            )
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        # Only author can update their comment
        if serializer.instance.author != self.request.user:
            raise PermissionError("You can only edit your own comments")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Author or moderator can delete
        user = self.request.user
        if instance.author == user or user.is_moderator or user.is_superuser:
            instance.delete()
        else:
            raise PermissionError("You can only delete your own comments")

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        votable_type = request.data.get('votable_type')
        votable_id = request.data.get('votable_id')
        value = request.data.get('value')
        
        # Check if vote exists
        vote, created = Vote.objects.update_or_create(
            user=request.user,
            votable_type=votable_type,
            votable_id=votable_id,
            defaults={'value': value}
        )
        
        serializer = self.get_serializer(vote)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
    
    @action(detail=False, methods=['delete'])
    def remove_vote(self, request):
        votable_type = request.query_params.get('votable_type')
        votable_id = request.query_params.get('votable_id')
        
        Vote.objects.filter(
            user=request.user,
            votable_type=votable_type,
            votable_id=votable_id
        ).delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        bookmarkable_type = request.data.get('bookmarkable_type')
        bookmarkable_id = request.data.get('bookmarkable_id')
        
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            bookmarkable_type=bookmarkable_type,
            bookmarkable_id=bookmarkable_id
        )
        
        serializer = self.get_serializer(bookmark)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
    
    @action(detail=False, methods=['delete'])
    def remove_bookmark(self, request):
        bookmarkable_type = request.query_params.get('bookmarkable_type')
        bookmarkable_id = request.query_params.get('bookmarkable_id')
        
        Bookmark.objects.filter(
            user=request.user,
            bookmarkable_type=bookmarkable_type,
            bookmarkable_id=bookmarkable_id
        ).delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)