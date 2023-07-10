from django.contrib import admin
from reviews.models import *
# Register your models here.

### we cannot include fields of type ManyToManyField in display_list ###

# Override list_display for book model to display 'title', 'isbn'
# class BookAdmin(admin.ModelAdmin):
# list_display = ('title', 'isbn')

# takes a function that takes the model instance as an argument
# def initialled_name(obj):
#     """ obj.first_names='Jerome David', obj.last_names='Salinger'
#     => 'Salinger, JD' """
#     initials = ''.join([name[0] for name in \
#     obj.first_names.split(' ')])
#     return "{}, {}".format(obj.last_names, initials)
# class ContributorAdmin(admin.ModelAdmin):
#     list_display = (initialled_name,)


class BookAdmin(admin.ModelAdmin):
    def get_publisher(self,obj):
        return obj.publisher.name
    list_display = ('title', 'isbn', 'get_publisher', 'publication_date')
    # filter by a specific year or a specific month in a specific year
    date_hierarchy = 'publication_date'

    # Search bar with attribute
    # search on the Publisher.name of publisher foreignkey
    # __exact need enter full to search
    search_fields = ("title", "isbn__exact", 'publisher__name')

    list_filter = ("publisher", 'publication_date')
    # isbn13 func defined in Book class model
    # takes a method from the ModelAdmin subclass that takes the model object as a single argument
    # def isbn13(self, obj):
    #     """ '9780316769174' => '978-0-31-676917-4' """
    #     return "{}-{}-{}-{}-{}".format(obj.isbn[0:3], obj.isbn[3:4],obj.isbn[4:6], obj.isbn[6:12],obj.isbn[12:13])


class ReviewAdmin(admin.ModelAdmin):
    # Exclude field from display
    # exclude = ('date_edited')

    # Enter specific fields to display this more efficient
    # fields=('content', 'rating', 'creator', 'book')

    # fieldsets specify the form layout as a series of grouped fields
    fieldsets = (
        ("Linkage", {'fields': ("creator", "book")}),
        ('Review content', {"fields": ("content", "rating")})
    )


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("last_names", "first_names")
    search_fields = ("last_names__startswith", "first_names__startswith")
    list_filter = ("last_names",)


# Register class Models in admin site
admin.site.register(Book, BookAdmin)
admin.site.register(Publisher)
admin.site.register(Contributor,ContributorAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)
