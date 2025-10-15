from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Book(models.Model):
    # genre list (key, value)
    GENRE_CHOICES = [
        ('Novel', 'Novel'),
        ('Science Fiction', 'Science Fiction'),
        ('History', 'History'),
        ('Self Development', 'Self Development'),
        ('Biography', 'Biography'),
        ('Literature', 'Literature'),
        ('Poetry', 'Poetry'),
        ('Children', 'Children'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(choices=GENRE_CHOICES)
    description = models.TextField(max_length=500)
    publication_year = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(2025)] # To select year between 1000 and 2025
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        null=True,  # temp (we used it to solve makemigrations issue)
        blank=True  # temp
    )

# return book title when you call Book
    def __str__(self):
        return self.title

# Ordering the Books
    class Meta:
        ordering = ['-created_at']


# Review and Rating
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="From 1 to 5 stars"
    )
    comment = models.TextField(max_length=500)
    
# Ordering the Reviews
    class Meta:
        ordering = ['-date']


