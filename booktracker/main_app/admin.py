from django.contrib import admin
from .models import Book, Review

# Registering models

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'user', 'genre', 'publication_year', 'is_read', 'created_at')
    list_filter = ('genre', 'is_read', 'created_at')
    search_fields = ('title', 'author', 'user__username')
    ordering = ('-created_at',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('book__title', 'comment')
    ordering = ('-date',)


admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)