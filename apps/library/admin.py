from django.contrib import admin

from apps.library import models


@admin.register(models.BookAuthorModel)
class BookAuthorAdmin(admin.ModelAdmin):
    """Админка автора книги."""
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(models.BookGenreModel)
class BookGenreAdmin(admin.ModelAdmin):
    """Админка жанра книги."""
    list_display = ("id", "title")
    list_display_links = ("id", "title")


@admin.register(models.BookModel)
class BookAdmin(admin.ModelAdmin):
    """Админка книги."""
    list_display = (
        "id", "title", "genre", "author",
        "release_year", "books_count"
    )
    list_display_links = (
        "id", "title", "genre", "author",
        "release_year", "books_count"
    )


@admin.register(models.BookReviewModel)
class BookReviewAdmin(admin.ModelAdmin):
    """Админка отзыва книги."""
    list_display = ("id", "user", "book")
    list_display_links = ("id", "user", "book")


@admin.register(models.BookRatingModel)
class BookRatingAdmin(admin.ModelAdmin):
    """Админка рейтинга книги."""
    list_display = ("id", "rating", "user", "book")
    list_display_links = ("id", "rating", "user", "book")
