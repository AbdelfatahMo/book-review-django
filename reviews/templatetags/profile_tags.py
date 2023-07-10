from django import template
from reviews.models import Review
register=template.Library()

@register.inclusion_tag("reviews/templatetags/book_list.html")
def book_list(username):
    book_list=[]
    user_reviews=Review.objects.filter(creator__username=username)
    
    for user_review in user_reviews:
        book=user_review.book
        book_list.append(book)
    return {'book_list':book_list}
    
    