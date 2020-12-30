from django.db.models import Avg, F

from rest_framework import serializers

from apps.library import mixins, models


class BookAuthorSerializer(serializers.ModelSerializer):
    """Сериализатор автора книги."""

    class Meta:
        model = models.BookAuthorModel
        fields = "__all__"


class BookGenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра книги."""

    class Meta:
        model = models.BookGenreModel
        fields = "__all__"


class BooksCountSerializer(serializers.Serializer):
    """Сериализатор для добавления/убавления количества книг."""
    value = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.books_count = F("books_count") + validated_data.get("value")
        instance.save(update_fields=["books_count"])
        return instance

    def validate_value(self, data):
        new_books_count = self.instance.books_count + data
        if new_books_count < 0:
            raise serializers.ValidationError("Количество книг не может стать отрицательным.")
        return data


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор книги."""
    reviews_count = serializers.ReadOnlyField()
    common_rating = serializers.ReadOnlyField()

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["author"] = instance.author.name
        context["genre"] = instance.genre.title

        additional_info = dict()
        additional_info["reviews_count"] = models.BookReviewModel.objects \
            .filter(book=instance) \
            .count()

        common_rating = instance.ratings \
            .aggregate(rating=Avg("rating"))["rating"]

        if common_rating:
            additional_info["common_rating"] = round(common_rating, 2)

        current_user = self.context["current_user"]
        try:
            rated_book = current_user.book_ratings.get(book=instance)
            additional_info["your_rating"] = rated_book.rating
        except (AttributeError, models.BookRatingModel.DoesNotExist):
            pass
        context["additional_info"] = additional_info
        return context

    class Meta:
        model = models.BookModel
        fields = "__all__"


class BookReviewSerializer(mixins.BookReviewRatingMixin):
    """Сериализатор отзыва книги."""

    class Meta:
        model = models.BookReviewModel
        fields = "__all__"


class BookRatingSerializer(mixins.BookReviewRatingMixin):
    """Сериализатор рейтинга книги."""

    def create(self, validated_data):
        book_rating, _ = models.BookRatingModel.objects.update_or_create(
            book=validated_data.get("book"),
            user=validated_data.get("user"),
            defaults={"rating": validated_data.get("rating")}
        )
        return book_rating

    class Meta:
        model = models.BookRatingModel
        fields = "__all__"
