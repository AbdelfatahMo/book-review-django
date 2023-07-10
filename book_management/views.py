from django.shortcuts import render
from django.views.generic.edit import CreateView ,UpdateView,DeleteView
from django.views.generic import DeleteView
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views import View
from .forms import BookForm
from .models import Book

# Create your views here.
class BookDetailView(DeleteView):
    model = Book
    fields='__all__'
    template_name = "book_management/book_detail.html"

class BookDeleteView(DeleteView):
    model = Book
    fields='__all__'
    template_name='book_management/book_delete_form.html'
    success_url="/book_management/entry_success"

class BookUpdateView(UpdateView):
    model = Book
    fields='__all__'
    template_name = "book_management/book_form.html"
    success_url="/book_management/entry_success"

class BookCreateView(CreateView):
    model = Book
    fields=['name','auther']
    template_name = "book_management/book_form.html"
    success_url = '/book_management/entry_success'


class BookRecordFormView(FormView):
    template_name = 'book_management/book_form.html'
    form_class = BookForm
    success_url = '/book_management/entry_success'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class FormSuccessView(View):
    def get(self, request, *args,**kwargs):
        return HttpResponse("Book record saved successfully")