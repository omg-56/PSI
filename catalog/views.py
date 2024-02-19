from django.shortcuts import render
from .models import Book, Author, Genre, BookInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


from catalog.forms import RenewBookForm


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

    num_genres = Genre.objects.all().count()

    word = request.GET.get("word", "")

    num_books_with_letter = Book.objects.filter(title__icontains='a').count()

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
        "num_genres": num_genres,
        "num_genres_with_word": num_genres_with_word,
        "num_books_with_letter": num_books_with_letter,
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

import datetime


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']
    permission_required = 'catalog.add_book'
    permission_required = 'catalog.can_mark_returned' # CAMBIO

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']
    permission_required = 'catalog.change_book'
    permission_required = 'catalog.can_mark_returned' # CAMBIO

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'
    permission_required = 'catalog.can_mark_returned' # CAMBIO

    def form_valid(self, form):
        # Check if there are any book instances
        if self.object.bookinstance_set.exists():
            # If there are, add an error message and redirect back to the delete page
            messages.error(self.request, 'Cannot delete book with existing instances.')
            return HttpResponseRedirect(reverse("book-delete", kwargs={"pk": self.object.pk}))
        else:
            # If there are no book instances, proceed with the deletion
            try:
                self.object.delete()
                return HttpResponseRedirect(self.success_url)
            except Exception as e:
                return HttpResponseRedirect(reverse("book-delete", kwargs={"pk": self.object.pk}))