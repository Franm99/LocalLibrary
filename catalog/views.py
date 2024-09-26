import datetime

from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm


def index(request):
    """ View function for home page of site. """

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session available.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

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
        'num_visits': num_visits
    }

    # Render the HTML template 'index.html with the data in the context variable
    return render(request=request, template_name='index.html', context=context)


class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'  # self-defined name for the model context variable.
    paginate_by = 10
    # template_name = 'books/book_list.html'
    
    # queryset = Book.objects.filter(author__name__iexact='George')  # Would do the same as below: 
    # def get_queryset(self) -> QuerySet[Any]:
    #     return Book.objects.filter(author__name__iexact='George')
    
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


class AuthorListView(ListView):
    model = Author
    context_object_name = 'author_list'
    paginate_by = 5
    

class AuthorDetailView(DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """ Generic class-based view listing books on loan to current user. """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
        
        
class AllLoanedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Generic class-based view listing all loaned books from every registered user. """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'
    
    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )
        
        
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Process the data in form.cleaned_data as required (here we just write it to the model due_back field):
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            
            # Redirect to the new URL
            return HttpResponseRedirect(reverse('all-borrowed'))
    
    # If this is a GET (or any other method), create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        
    context = {
        'form': form,
        'book_instance': BookInstance,
    }
    
    return render(request, 'catalog/book_renew_librarian.html', context)
    