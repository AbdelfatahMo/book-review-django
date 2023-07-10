import datetime
import re
from django.db.models import Count
from reviews.models import Review


def get_books_read_by_month(username) -> Count:
    current_year = datetime.datetime.now().year
    #     Filtration
    # Review.objects.filter(creator__username__contains=username,date_created__year=current_year)
    # Here you filter the review records to choose all the records that belong to the
    # current user as well as the current year. The year field can be easily accessed
    # from our date_created field by appending __year.
    #     Projection
    # Once the review records are filtered, you are not interested in all the fields that
    # might be there. What you are mainly interested in is the month and the number
    # of books read each month. For this, use the values() call to select only the
    # month field from the date_created attribute of the Review model on which
    # you are going to run the group by operation.
    #     Group By
    # Here, you select the total number of books read in a given month. This is done
    # by applying the annotate method to the QuerySet instance returned by the values() call.
    books = Review.objects.filter(creator__username=username, 
                                  date_created__year=current_year).values(
                                      'date_created__month').annotate(
                                          book_count=Count('book__title'))
    return books

def get_books_read(username):
    books=Review.objects.filter(creator__username=username).values('book__title','date_created')
    return books
