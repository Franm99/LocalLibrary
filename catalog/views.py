from django.shortcuts import render

from .models import Book, Author, BookInstance, Genre

def index(request):
    """ View function for home page of site. """

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Challenge:
    num_genres = Genre.objects.count()
    num_books_containing_The = Book.objects.filter(title__icontains='The').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_containing_The': num_books_containing_The,
    }

    # Render the HTML template 'index.html with the data in the context variable
    return render(request=request, template_name='index.html', context=context)