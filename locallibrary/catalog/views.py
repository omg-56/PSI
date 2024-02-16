from django.shortcuts import render
from .models import Book, Author, Genre, BookInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.


def index(request):
    """View function for home page of site"""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = "a")
    num_instances_available = BookInstance.objects.filter(
        status__exact="a").count()

    # The "all()" is implied by default
    num_authors = Author.objects.count()

    word = request.GET.get("word", "")

    num_genres_with_word = Genre.objects.filter(name__icontains=word).count()
    num_books_with_word = Book.objects.filter(title__icontains=word).count()

    # Number of visits to this view, as counted in the session variable
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "word": word,
        "num_genres_with_word": num_genres_with_word,
        "num_books_with_word": num_books_with_word,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/book_list.html"
    paginate_by = 3

    def get_queryset(self):
        """ here you can add some logic to
        filter the books that you want to show """
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["some_data"] = "This is just some data"
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "books/book_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context["some_data"] = "This is just some data"
        return context


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    template_name = "authors/author_list.html"
    paginate_by = 10

    def get_queryset(self):
        """here you can add some logic to filter
        the authors that you want to show"""
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context["some_data"] = "This is just some data"
        return context


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "authors/author_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context["some_data"] = "This is just some data"
        return context

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
class AllBooksBorrowedListView(LoginRequiredMixin,generic.ListView, PermissionRequiredMixin):
    """Generic class-based view listing all books on loan."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )