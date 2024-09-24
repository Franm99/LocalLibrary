import uuid

from datetime import date 

from django.conf import settings
from django.urls import reverse

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q, F
from django.db.models.functions import Lower


class Genre(models.Model):
    """ Genres model """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g., Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """ String for representing the Model object. """
        return self.name
    
    def get_absolute_url(self):
        """ Returns the url to access a particular genre instance. """
        return reverse('genre-detail', args=[str(self.id)])
    
    class Meta:
        """
        Setting the unique=True constraint for the name field prevents genres being created with 'exactly' the same name,
        but not variations such as 'fantasy', 'FantasY', 'FanTASy', etc. The following constraint prevents that.
        """
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message="Genre already exists (case insensitive match)"
            )
        ]
        

class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name="language_lower_case_insensitive_unique",
                violation_error_message="Language already exists (case insensitive match)"
            )
        ]


class Book(models.Model):
    """ Book model. It is like the template of the book, not a physical copy or instance. """
    
    """
    Some details about the fields definition:
    - author: is declared as a foreign key because one author can have multiple books, but one book cannot have multiple authors.
    Additionally, instead of giving it the class Author, the string 'Author' is used because the class Author is not declared at the
    top of this class Book.
    The last detail about author: on_delete=models.RESTRICT prevents an author being removed if it is referenced by any book.
    """
    title = models.CharField(max_length=200, help_text="Book's title", verbose_name="Title")
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book", verbose_name="Summary")
    isbn = models.CharField('ISBN', max_length=13, unique=True, 
                            help_text='13 character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ManyToManyField(Language, help_text='Select a language for this book')
    
    def __str__(self) -> str:
        """ String for representing the Model object. """
        return self.title
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """
        Create a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'
    
    
class BookInstance(models.Model):
    """Model representing a specific copy of a book."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          help_text="Unique ID for this particular book across the whole library.")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200, help_text='Specific release of the book')
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )
    
    class Meta:
        ordering = ['due_back']
        
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
    @property
    def is_overdue(self):
        """ Determines if the book is overdue based on the due date and current date. """
        return bool(self.due_back and date.today() > self.due_back)
    
    
class Author(models.Model):
    """ Model representing an author. """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        constraints = [
            CheckConstraint(
                check=Q(date_of_birth__lt=F('date_of_death')),
                name='author_date_of_birth_lower_than_date_of_death'
            )
        ]
        
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
    
class Review(models.Model):
    """ Model representing a book review. """
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    publish_date = models.DateTimeField("Publish Date", null=True, blank=True)
    content = models.TextField(max_length=1000, help_text="Add some comments to the review.")
    grade = models.FloatField(help_text="Add a grade from 0.0 (awful) to 10.0 (perfect)", 
                              validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    # TODO: add user field
    
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(grade__gte=0.0) & Q(grade__lte=10.0),
                name='review_grade_min_and_max_limits'
            )
        ]
        
    # TODO: Add __str__ method
    