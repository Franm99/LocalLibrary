from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView

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


class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'  # self-defined name for the model context variable.
    # template_name = 'books/book_list.html'
    
    # queryset = Book.objects.filter(author__name__iexact='George')  # Would do the same as below: 
    def get_queryset(self) -> QuerySet[Any]:
        return Book.objects.filter(author__name__iexact='George')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Then create any data and add it to the context
        context['year'] = '2024'
        return context
    

class BookDetailView(DetailView):
    model = Book


"""
Similar but with Function-based method:

def book_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    
    return render(request, 'catalog/book_detail.html', context={'book': book})

Another way:

from django.shortcuts import get_object_or_404

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

"""
        
    