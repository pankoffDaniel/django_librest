from rest_framework import serializers


class BookReviewRatingMixin(serializers.ModelSerializer):
    """Миксин для дополнения сериализации отзыва и рейтинга книги."""
    book_title = serializers.ReadOnlyField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.username
        data["book_title"] = instance.book.title
        data.pop("book")
        return data
