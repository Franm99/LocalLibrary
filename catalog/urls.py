from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('staff/allbooks', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', view=views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update', view=views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', view=views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', view=views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update', view=views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', view=views.BookDelete.as_view(), name='book-delete'),
]