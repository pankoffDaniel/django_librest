from django.shortcuts import get_object_or_404

from rest_framework import views, viewsets
from rest_framework.response import Response

from apps.library import models, permissions, serializers
from apps.library.serializers import BooksCountSerializer


class BookAuthorViewSet(viewsets.ModelViewSet):
    """Вьюшка автора книги."""
    queryset = models.BookAuthorModel.objects.all()
    serializer_class = serializers.BookAuthorSerializer
    permission_classes = [
        permissions.IsAdminUser |
        permissions.ReadOnly
    ]


class BookGenreViewSet(viewsets.ModelViewSet):
    """Вьюшка жанра книги."""
    queryset = models.BookGenreModel.objects.all()
    serializer_class = serializers.BookGenreSerializer
    permission_classes = [
        permissions.IsAdminUser |
        permissions.ReadOnly
    ]


class BookViewSet(viewsets.ModelViewSet):
    """Вьюшка книги."""
    queryset = models.BookModel.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [
        permissions.IsAdminUser |
        permissions.ReadOnly
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["current_user"] = self.request.user
        return context


class BookActionsView(views.APIView):
    """Вьюшка действий к книге."""
    permission_classes = [
        permissions.IsAdminUser |
        permissions.permissions.IsAuthenticated
    ]

    def patch(self, request, *args, **kwargs):
        """Добавляет/убавляет количество экземпляров книг `books_count`."""
        book = get_object_or_404(models.BookModel, pk=self.kwargs["pk"])
        serializer = BooksCountSerializer(book, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=200)
        return Response(serializer.data)


class BookReviewViewSet(viewsets.ModelViewSet):
    """Вьюшка отзыва книги."""
    queryset = models.BookReviewModel.objects.all()
    serializer_class = serializers.BookReviewSerializer
    permission_classes = [
        permissions.IsAdminUser |
        permissions.IsOwner |
        permissions.ReadOnly
    ]


class BookRatingViewSet(viewsets.ModelViewSet):
    """Вьюшка рейтинга книги."""
    queryset = models.BookRatingModel.objects.all()
    serializer_class = serializers.BookRatingSerializer
    permission_classes = [
        permissions.IsAdminUser |
        permissions.IsOwner |
        permissions.ReadOnly
    ]
