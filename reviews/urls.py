from django.urls import path,include
from . import views,api_views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register(r"books", api_views.BookViewSet)
router.register(r"reviews",api_views.ReviewViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("book-search/", views.book_search, name='book_search'),
    path("books/", views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_details, name='book_details'),
    path("books/<int:pk>/media/", views.book_media, name="book_media"),
    path("publishers/<int:pk>/", views.publisher_edit, name='publisher_edit'),
    path('publishers/new/', views.publisher_edit, name='publisher_create'),
    path("reviews/<int:book_pk>/<int:review_pk>/",
         views.review_edit, name='review_edit'),
    path('reviews/<int:book_pk>/new-review/',
         views.review_edit, name='review_create'),
    path('api/',include((router.urls,'api'))),
    path("api/login", api_views.Login.as_view(),name='login'),
#    path('react-example/', views.react_example),
#     path('api/first_api_view/',api_views.first_api_view),
#     path("api/books/",api_views.AllBooks.as_view(),name="books"),
#     path('api/contributors/',api_views.ContributorView.as_view(),name="ontributors"),

]
