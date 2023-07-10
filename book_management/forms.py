from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields="__all__"
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'