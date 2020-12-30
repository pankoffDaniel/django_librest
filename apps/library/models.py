from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


UserModel = get_user_model()


class BookAuthorModel(models.Model):
    """Модель автора книги."""
    name = models.CharField("Имя", max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class BookGenreModel(models.Model):
    """Модель жанра книги."""
    title = models.CharField("Название", max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class BookModel(models.Model):
    """Модель книги."""
    title = models.CharField("Название", max_length=255)
    release_year = models.PositiveSmallIntegerField("Год выхода")
    books_count = models.PositiveIntegerField("Количество книг", default=0)
    description = models.TextField("Описание")
    author = models.ForeignKey(
        BookAuthorModel,
        verbose_name="Автор",
        on_delete=models.PROTECT,
        related_name="books"
    )
    genre = models.ForeignKey(
        BookGenreModel,
        verbose_name="Жанр",
        on_delete=models.PROTECT,
        related_name="books"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BookReviewModel(models.Model):
    """Модель отзыва книги."""
    review = models.TextField("Отзыв")
    book = models.ForeignKey(
        BookModel,
        verbose_name="Книга",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        UserModel,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="book_reviews"
    )

    def __str__(self):
        return f"{self.pk}: {self.book.pk}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class BookRatingModel(models.Model):
    """Модель рейтинга книги."""
    rating = models.PositiveSmallIntegerField(
        "Значение рейтинга",
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )
    book = models.ForeignKey(
        BookModel,
        verbose_name="Книга",
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    user = models.ForeignKey(
        UserModel,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="book_ratings"
    )

    def __str__(self):
        return f"{self.rating}: {self.book.pk}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
