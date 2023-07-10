from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from .models import Book, Review, Contributor, Publisher
from .utils import average_rating
from .forms import ReviewForm, SearchForm, PublisherForm, BookMediaForm
from django.utils import timezone
from PIL import Image
from django.core.files.images import ImageFile
from io import BytesIO


# Create your views here.


def index(request):
    return render(request, "base.html")


def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({'book': book, 'book_rating': book_rating,
                         'number_of_reviews': number_of_reviews})
    context = {
        'book_list': book_list
    }
    return render(request, "reviews/book_list.html", context)


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    book_rating = average_rating([review.rating for review in reviews])
    content = {
        'book': book,
        'book_rating': book_rating,
        'reviews': reviews,
    }
    if request.user.is_authenticated:
        max_viewed_books_length = 10
        viewed_books = request.session.get("viewed_books", [])
        viewed_book = [book.pk, book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
        viewed_books.insert(0, viewed_book)
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session["viewed_books"] = viewed_books
    return render(request, "reviews/book_details.html", content)



def book_search(request):
    search = request.GET.get("search", '')
    form = SearchForm(request.GET)
    books = []
    if form.is_valid() and form.cleaned_data['search']:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data["search_in"] or 'title'
        if request.user.is_authenticated:
            max_search_history = 10
            search_history = request.session.get("search_history", [])
            history = [search_in, search]
            if history in search_history:
                search_history.pop(search_history.index(history))
            search_history.insert(0, history)
            search_history = search_history[:max_search_history]
            request.session["search_history"] = search_history
            print(search_history)
        if search_in == 'title':
            books = Book.objects.filter(title__icontains=search)
        else:
            fname_contributors = Contributor.objects.filter(
                first_names__icontains=search)
            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.append(book)
            lname_contributors = Contributor.objects.filter(
                last_names__icontains=search)
            for contributor in lname_contributors:
                for book in contributor.book_set.all():
                    books.append(book)
    return render(request, "reviews/search-results.html",
                  {"form": form, 'books': books, 'search': search})

#### AUTHENTICIANS ####
# @permission_required('edit_publisher') or


def is_staff_user(user):
    return user.is_staff


@user_passes_test(is_staff_user)
def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is not None:
                messages.success(
                    request, ("Publisher {} was updated.".format(updated_publisher)))
            else:
                messages.success(
                    request, ("Publisher {} was Created.".format(updated_publisher)))
            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    return render(request, "reviews/instance-form.html", {"form": form, 'instance': publisher, 'model_type': 'Publisher'})


@login_required
def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
        if book.id != review.book_id:
            review = None
    else:
        review = None
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            updated_review.book = book
            updated_review.creator = request.user
            if review == None:
                pass
            else:
                updated_review.date_edited = timezone.now()
            updated_review.save()
            if review is None:
                messages.success(
                    request, "Review for \"{}\" created".format(book))
            else:
                messages.success(
                    request, "Review for \"{}\" updated".format(book))
            return redirect('book_details', book.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/instance-form.html",
                  {"form": form, 'instance': review, 'related_instance': book,
                   'related_model_type': 'Book', 'model_type': 'Review'})


@login_required
def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            # we can also override save method on book model
            cover = form.cleaned_data.get("cover")
            if cover:
                # Open and resize the image file
                image = Image.open(cover)
                image.thumbnail((300, 300))
                # Save the resized image to a BytesIO object (save in memory)
                image_data = BytesIO()
                image.save(fp=image_data, format=cover.image.format)
                # Create a new ImageFile object and save it to the book cover field
                image_file = ImageFile(image_data)
                book.cover.save(cover.name, image_file)
                book.save()

            messages.success(
                request, "Book {} was successfully updated.".format(book))
            return redirect("book_details", book.pk)
    else:
        form = BookMediaForm(instance=book)
    return render(request, "reviews/instance-form.html",
                  {"form": form, 'instance': book, 'model_type': 'Book'})


# def react_example(request):
#     return render(request,"reviews/react-example.html",{'name':'Ben','target':5})
