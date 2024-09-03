from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language, Review

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Review)


class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)
