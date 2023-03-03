from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from reviews.models import Review, Title

from .filter import TitleFilter
from .permissions import (IsAdminOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly)
from .serializers import (CommentSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для Title"""
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для Review"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(
            title=title,
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Comment"""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(
            Review.objects.filter(title_id=title.id), pk=review.id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = get_object_or_404(
            Review.objects.filter(title_id=title.id), pk=review.id
        )
        serializer.save(
            review=review,
            author=self.request.user
        )
