# Generated by Django 2.1.4 on 2018-12-12 15:33

from django.db import migrations


def convert_author_string(apps, schema_editor):
    Book = apps.get_model("core", "Book")
    Author = apps.get_model("core", "Author")

    for book in Book.objects.all():
        author_names = [n.strip() for n in book.author_string.split(",")]
        for name in author_names:
            try:
                author = Author.objects.get(name=name)
            except Author.DoesNotExist:
                author = Author.objects.create(name=name)
            book.authors.add(author)


class Migration(migrations.Migration):

    dependencies = [("core", "0004_auto_20181212_1527")]

    operations = [migrations.RunPython(convert_author_string)]
