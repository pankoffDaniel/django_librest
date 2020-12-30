from django.urls import path

from rest_framework import routers

from apps.library import views


router = routers.SimpleRouter()
router.register('authors', views.BookAuthorViewSet, basename="author")
router.register('genres', views.BookGenreViewSet, basename="genre")
router.register('books', views.BookViewSet, basename="book")
router.register('reviews', views.BookReviewViewSet, basename="review")
router.register('ratings', views.BookRatingViewSet, basename="rating")
router.register('authors', views.BookAuthorViewSet, basename="author")


urlpatterns = [
    path("books/<int:pk>/change-count/", views.BookActionsView.as_view(), name="book-change-count")
]

urlpatterns += router.urls
