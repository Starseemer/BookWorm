from django.forms import fields
from .models import Book
from django import forms

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = {
            "id",
            "title",
            "subtitle",
            "price",
            "url"
        }
