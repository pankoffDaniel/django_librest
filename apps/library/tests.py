from django.db.models import ProtectedError

from rest_framework import status
from rest_framework.reverse import reverse

from apps.library.models import (
    BookAuthorModel,
    BookGenreModel,
    BookModel,
    BookReviewModel,
    BookRatingModel,
)
from apps.users.tests import BaseUserSetUp


class BaseSetUp(BaseUserSetUp):
    """Базовый класс с общими данными для тестирования моделей."""

    def setUp(self):
        """Подготовка к тестированию приложения."""
        super().setUp()
        self.author1 = BookAuthorModel.objects.create(name="Author1")
        self.author2 = BookAuthorModel.objects.create(name="Author2")

        self.genre1 = BookGenreModel.objects.create(title="Genre1")
        self.genre2 = BookGenreModel.objects.create(title="Genre2")

        self.new_book_data = {
            "title": "NewBook",
            "release_year": 2020,
            "description": "Description NewBook",
            "author": self.author2.pk,
            "genre": self.genre2.pk
        }

        self.book1 = BookModel.objects.create(
            title="Book1", release_year=2020, description="Description Book1",
            author=self.author1, genre=self.genre1, books_count=2
        )
        self.book2 = BookModel.objects.create(
            title="Book2", release_year=2021, description="Description Book2",
            author=self.author2, genre=self.genre2
        )


class BookAuthorTests(BaseSetUp):
    """Тестирование модели автора книги."""

    # GET

    def test_get_author_detail(self):
        response = self.client.get(reverse("author-detail", kwargs={"pk": self.author1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({"id": 1, "name": "Author1"}, response.json())

    def test_get_author_list(self):
        response = self.client.get(reverse("author-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertIn({"id": 1, "name": "Author1"}, response.json())

    # POST

    def test_create_author_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("author-list"), data={"name": "NewAuthor"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_exist_author_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("author-list"), data={"name": "Author1"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_empty_author_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("author-list"), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_author_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.post(reverse("author-list"), data={"name": "NewAuthor"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_create_author_by_anonymous_user(self):
        response = self.client.post(reverse("author-list"), data={"name": "NewAuthor"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # PUT

    def test_full_change_author_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.put(
            reverse("author-detail", kwargs={"pk": self.author1.pk}),
            data={"name": "ChangedAuthor"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_full_change_author_to_empty_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("author-list"), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_full_change_author_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.put(
            reverse("author-detail", kwargs={"pk": self.author1.pk}),
            data={"name": "ChangedAuthor"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_full_change_author_by_anonymous_user(self):
        response = self.client.put(
            reverse("author-detail", kwargs={"pk": self.author1.pk}),
            data={"name": "ChangedAuthor"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE

    def test_fail_delete_author_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        with self.assertRaises(ProtectedError):
            self.client.delete(reverse("author-detail", kwargs={"pk": self.author1.pk}))

    def test_fail_delete_author_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.delete(reverse("author-detail", kwargs={"pk": self.author1.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_delete_author_by_anonymous_user(self):
        response = self.client.delete(reverse("author-detail", kwargs={"pk": self.author1.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookGenreTests(BaseSetUp):
    """Тестирование модели жанра книги."""

    # GET

    def test_get_genre_detail(self):
        response = self.client.get(reverse("genre-detail", kwargs={"pk": self.genre1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({"id": 1, "title": "Genre1"}, response.json())

    def test_get_genre_list(self):
        response = self.client.get(reverse("genre-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertIn({"id": 1, "title": "Genre1"}, response.json())

    # POST

    def test_create_genre_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("genre-list"), data={"title": "NewGenre"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_exist_genre_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("genre-list"), data={"title": "Genre1"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_empty_genre_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("genre-list"), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_genre_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.post(reverse("genre-list"), data={"title": "NewGenre"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_create_genre_by_anonymous_user(self):
        response = self.client.post(reverse("genre-list"), data={"title": "NewGenre"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # PUT

    def test_full_change_genre_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.put(
            reverse("genre-detail", kwargs={"pk": self.genre1.pk}),
            data={"title": "ChangedGenre"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_full_change_author_to_empty_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.put(
            reverse("genre-list"), kwargs={"pk": self.genre1.pk}, data={}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_fail_full_change_genre_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.put(
            reverse("genre-detail", kwargs={"pk": self.genre1.pk}),
            data={"title": "ChangedGenre"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_full_change_genre_by_anonymous_user(self):
        response = self.client.put(
            reverse("genre-detail", kwargs={"pk": self.genre1.pk}),
            data={"title": "ChangedGenre"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE

    def test_fail_delete_genre_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        with self.assertRaises(ProtectedError):
            self.client.delete(reverse("genre-detail", kwargs={"pk": self.genre1.pk}))

    def test_fail_delete_genre_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.delete(reverse("genre-detail", kwargs={"pk": self.genre1.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_delete_genre_by_anonymous_user(self):
        response = self.client.delete(reverse("genre-detail", kwargs={"pk": self.genre1.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookTests(BaseSetUp):
    """Тестирование модели книги."""

    def setUp(self):
        super().setUp()
        self.book1_data = {
            "id": 1,
            "title": "Book1",
            "release_year": 2020,
            "books_count": 2,
            "description": "Description Book1",
            "author": "Author1",
            "genre": "Genre1",
            "additional_info": {
                "reviews_count": 0
            }
        }

        self.book1_data_to_full_change = {
            "title": "FullChangedBook1",
            "release_year": 2010,
            "books_count": 10,
            "description": "Description Book1",
            "author": 2,
            "genre": 2,
        }

    # GET

    def test_get_book_detail(self):
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book1.pk}))
        self.assertEqual(response.json(), self.book1_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book_list(self):
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    # POST

    def test_create_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("book-list"), data=self.new_book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_empty_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("book-list"), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_book_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.post(reverse("book-list"), data=self.new_book_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_create_book_by_anonymous_user(self):
        response = self.client.post(reverse("book-list"), data=self.new_book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # PUT

    def test_full_change_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        data = self.book1_data_to_full_change
        response = self.client.put(
            reverse("book-detail", kwargs={"pk": self.book1.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_empty_full_change_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.put(
            reverse("book-detail", kwargs={"pk": self.book1.pk}), data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_full_change_book_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        data = self.book1_data_to_full_change
        response = self.client.put(
            reverse("book-detail", kwargs={"pk": self.book1.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_full_change_book_by_anonymous_user(self):
        data = self.book1_data_to_full_change
        response = self.client.put(
            reverse("book-detail", kwargs={"pk": self.book1.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # PATCH

    def test_partial_change_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.patch(
            reverse("book-detail", kwargs={"pk": self.book1.pk}),
            data={"title": "PatchedBook1"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_empty_partial_change_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.patch(
            reverse("book-detail", kwargs={"pk": self.book1.pk}), data={}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_books_count_for_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.patch(
            reverse("book-change-count", kwargs={"pk": self.book1.pk}),
            data={"value": 3}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = BookModel.objects.get(pk=self.book1.pk)
        self.assertEqual(book.books_count, 5)

    def test_remove_books_count_for_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.patch(
            reverse("book-change-count", kwargs={"pk": self.book1.pk}),
            data={"value": -1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = BookModel.objects.get(pk=self.book1.pk)
        self.assertEqual(book.books_count, 1)

    def test_fail_remove_too_much_books_count_for_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.patch(
            reverse("book-change-count", kwargs={"pk": self.book1.pk}),
            data={"value": -10}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        book = BookModel.objects.get(pk=self.book1.pk)
        self.assertEqual(book.books_count, 2)

    def test_fail_add_word_instead_books_count_for_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.patch(
            reverse("book-change-count", kwargs={"pk": self.book1.pk}),
            data={"value": "BooksCount"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        book = BookModel.objects.get(pk=self.book1.pk)
        self.assertEqual(book.books_count, 2)

    def test_fail_add_empty_books_count_for_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.patch(
            reverse("book-change-count", kwargs={"pk": self.book1.pk}),
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        book = BookModel.objects.get(pk=self.book1.pk)
        self.assertEqual(book.books_count, 2)

    def test_fail_add_books_count_for_not_found_book_page_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.patch(
            reverse("book-change-count", kwargs={"pk": "999"}),
            data={"value": "BooksCount"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        book = BookModel.objects.get(pk=self.book1.pk)
        self.assertEqual(book.books_count, 2)

    def test_fail_partial_change_book_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.patch(
            reverse("book-detail", kwargs={"pk": self.book1.pk}),
            data={"title": "PatchedBook1"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_partial_change_book_by_anonymous_user(self):
        response = self.client.patch(
            reverse("book-detail", kwargs={"pk": self.book1.pk}),
            data={"title": "PatchedBook1"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE

    def test_delete_book_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.delete(reverse("book-detail", kwargs={"pk": self.book1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_delete_book_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.delete(reverse("book-detail", kwargs={"pk": self.book1.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_delete_book_by_anonymous_user(self):
        response = self.client.delete(reverse("book-detail", kwargs={"pk": self.book1.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookReviewsTest(BaseSetUp):
    """Тестирование модели отзыва книги."""

    def setUp(self):
        super().setUp()
        self.review0 = BookReviewModel.objects.create(
            review="Review0", book=self.book1, user=self.superuser
        )
        self.review1 = BookReviewModel.objects.create(
            review="Review1", book=self.book1, user=self.user1
        )
        self.review2 = BookReviewModel.objects.create(
            review="Review2", book=self.book2, user=self.user2
        )

    # GET

    def test_get_review_detail(self):
        response = self.client.get(reverse("review-detail", kwargs={"pk": self.review1.pk}))
        data = {
            "id": self.review1.pk,
            "review": self.review1.review,
            "user": self.user1.username,
            "book_title": self.book1.title
        }
        self.assertEqual(response.json(), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_review_list(self):
        response = self.client.get(reverse("review-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    # POST

    def test_create_review_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        data = {
            "review": "NewReview0",
            "book": self.book1.pk
        }
        response = self.client.post(reverse("review-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        data = {
            "review": "NewReview2",
            "book": self.book2.pk
        }
        response = self.client.post(reverse("review-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_empty_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("review-list"), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_review_by_anonymous_user(self):
        response = self.client.post(reverse("review-list"), data=self.new_book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # PUT

    def test_full_change_review_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        data = {
            "review": "ChangedReviewByAdmin",
            "book": self.book1.pk
        }
        response = self.client.put(
            reverse("review-detail", kwargs={"pk": self.review0.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(
            reverse("review-detail", kwargs={"pk": self.review1.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_change_review_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        data = {
            "review": "ChangedReviewByOwner",
            "book": self.book1.pk
        }
        response = self.client.put(
            reverse("review-detail", kwargs={"pk": self.review1.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_full_change_review_to_empty_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.put(
            reverse("review-detail", kwargs={"pk": self.review0.pk}), data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_full_change_review_by_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        data = {
            "review": "ChangedReviewByAnotherUser",
            "book": self.book2.pk
        }
        response = self.client.put(
            reverse("review-detail", kwargs={"pk": self.review2.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_full_change_review_by_anonymous_user(self):
        data = {
            "review": "ChangedReviewByAnonymousUser",
            "book": self.book1.pk
        }
        response = self.client.put(
            reverse("review-detail", kwargs={"pk": self.review0.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE

    def test_delete_review_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.delete(reverse("review-detail", kwargs={"pk": self.review0.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse("review-detail", kwargs={"pk": self.review1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_review_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.delete(reverse("review-detail", kwargs={"pk": self.review1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_delete_review_by_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.delete(reverse("review-detail", kwargs={"pk": self.review2.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_delete_review_by_anonymous_user(self):
        response = self.client.delete(reverse("review-detail", kwargs={"pk": self.review0.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookRatingTest(BaseSetUp):
    """Тестирование модели рейтинга книги."""

    def setUp(self):
        super().setUp()
        self.rating0 = BookRatingModel.objects.create(
            rating=9, book=self.book1, user=self.superuser
        )
        self.rating1 = BookRatingModel.objects.create(
            rating=8, book=self.book1, user=self.user1
        )
        self.rating2 = BookRatingModel.objects.create(
            rating=7, book=self.book2, user=self.user2
        )

    # GET

    def test_get_rating_detail(self):
        response = self.client.get(reverse("rating-detail", kwargs={"pk": self.rating1.pk}))
        data = {
            "id": self.rating1.pk,
            "rating": self.rating1.rating,
            "user": self.user1.username,
            "book_title": self.book1.title
        }
        self.assertEqual(response.json(), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rating_list(self):
        response = self.client.get(reverse("rating-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    # POST

    def test_create_rating_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        data = {
            "rating": 1,
            "book": self.book1.pk
        }
        response = self.client.post(reverse("rating-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rating_is_change_exist_rating(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        data = {
            "rating": 7,
            "book": self.book1.pk
        }
        response = self.client.post(reverse("rating-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse("rating-detail", kwargs={"pk": self.rating1.pk}))
        data = {
            "id": 2,
            "rating": 7,
            "user": self.user1.username,
            "book_title": self.book1.title
        }
        self.assertEqual(response.json(), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_rating_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        book = self.client.get(reverse("book-detail", kwargs={"pk": self.book2.pk}))
        self.assertNotIn("your_rating", book.json()["additional_info"])

        data = {
            "rating": 2,
            "book": self.book2.pk
        }
        response = self.client.post(reverse("rating-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        book = self.client.get(reverse("book-detail", kwargs={"pk": self.book2.pk}))
        self.assertEqual(2, book.json()["additional_info"]["your_rating"])

    def test_fail_create_invalid_value_rating(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        data = {
            "rating": 11,
            "book": self.book1.pk
        }
        response = self.client.post(reverse("rating-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {
            "rating": 0,
            "book": self.book1.pk
        }
        response = self.client.post(reverse("rating-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_empty_rating(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.post(reverse("rating-list"), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_rating_by_anonymous_user(self):
        response = self.client.post(reverse("rating-list"), data=self.new_book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # PUT

    def test_full_change_rating_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        data = {
            "rating": 3,
            "book": self.book1.pk
        }
        response = self.client.put(
            reverse("rating-detail", kwargs={"pk": self.rating0.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(
            reverse("rating-detail", kwargs={"pk": self.rating1.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_change_rating_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        data = {
            "rating": 4,
            "book": self.book1.pk
        }
        response = self.client.put(
            reverse("rating-detail", kwargs={"pk": self.rating1.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_full_change_rating_to_empty_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.put(
            reverse("rating-detail", kwargs={"pk": self.rating0.pk}), data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_full_change_rating_by_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        data = {
            "rating": 5,
            "book": self.book2.pk
        }
        response = self.client.put(
            reverse("rating-detail", kwargs={"pk": self.rating2.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_full_change_rating_by_anonymous_user(self):
        data = {
            "rating": 3,
            "book": self.book1.pk
        }
        response = self.client.put(
            reverse("rating-detail", kwargs={"pk": self.rating0.pk}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE

    def test_delete_rating_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser.key}")
        response = self.client.delete(reverse("rating-detail", kwargs={"pk": self.rating0.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse("rating-detail", kwargs={"pk": self.rating1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_rating_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.delete(reverse("rating-detail", kwargs={"pk": self.rating1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_delete_rating_by_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user1.key}")
        response = self.client.delete(reverse("rating-detail", kwargs={"pk": self.rating2.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_delete_rating_by_anonymous_user(self):
        response = self.client.delete(reverse("rating-detail", kwargs={"pk": self.rating0.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
