from rest_framework import serializers
from core.models import Book, BookNote, User, Author, Follow


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            value, _ = self.get_queryset().get_or_create(**{self.slug_field: data})
            return value
        except (TypeError, ValueError):
            self.fail("invalid")


# An example of a more "concrete" version of this:
# class AuthorSlugRelatedField(serializers.SlugRelatedField):
#     def to_internal_value(self, name):
#         value, _ = Author.objects.all().get_or_create(name=name)
#         return value


class BookNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNote
        fields = ("id", "body", "page_number", "created_at")


class BookSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api_book", lookup_field="id")
    notes = BookNoteSerializer(many=True, required=False)
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)
    authors = CreatableSlugRelatedField(
        slug_field="name", many=True, queryset=Author.objects.all()
    )

    class Meta:
        model = Book
        fields = ("id", "url", "title", "authors", "status", "owner", "notes")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class FollowSerializer(serializers.ModelSerializer):
    followed_user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ("followed_user",)
