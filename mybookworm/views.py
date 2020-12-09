from django.db.models.fields import NullBooleanField
from .forms import BookForm
from re import sub, template
from typing import SupportsBytes
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import json, requests 
from .models import Book

def index(request):
    return render(request, 'mybookworm/index.html')

def search(request, search_word, page):
    if request.method == "POST":
        if(request.POST.get("isAdd") == "add"):
            Book.objects.create(id=request.POST.get("book_id"), 
            title=request.POST.get("title"),
            subtitle=request.POST.get("subtitle"),
            price=request.POST.get("price"),
            url=request.POST.get("img_url"))
        else:
            Book.objects.filter(pk=request.POST.get("book_id")).delete()
        
        

    template = loader.get_template('mybookworm/search.html')
    books = []
    
    response = json.loads(requests.get("https://api.itbook.store/1.0/search/"+str(search_word)+"/"+str(page)).text)
    for book in response["books"]:
        if(float(book["price"][1:]) == 0.0):
            price = "Get it for free!"
        elif(float(book["price"][1:]) >= 50.0):
            price = "For " + book["price"]
        else:
            price = "Only for " + book["price"]
        isAdded = False
        if Book.objects.filter(pk=book["isbn13"]).exists():
            isAdded = True
        books.append((book["title"], book["subtitle"], price, book["image"], book["isbn13"], isAdded))
    
    context = {
        'books':books,
        'search_word':search_word,
        'page':page,
        'max_page':response["total"],
    }
    return HttpResponse(template.render(context, request))

def bookMarks(request):
    template = loader.get_template("mybookworm/bookmarks.html")
    bookmarks = Book.objects.all()
    context = {
        "bookmarks":bookmarks,
    }
    return HttpResponse(template.render(context,request))

def bookMarkDetails(request, book_id):
    book = None
    if request.method == "POST":
        if(request.POST.get("isAdd") == "add"):
            Book.objects.create(id=request.POST.get("book_id"), 
            title=request.POST.get("title"),
            subtitle=request.POST.get("subtitle"),
            price=request.POST.get("price"),
            url=request.POST.get("img_url"))
        else:
            book = Book.objects.filter(pk=request.POST.get("book_id"))[0]
            Book.objects.filter(pk=request.POST.get("book_id")).delete()
    
    template = loader.get_template("mybookworm/bookmark_details.html")
    if Book.objects.filter(pk=book_id).exists():
        book = Book.objects.filter(pk=book_id)[0]
        isAdded = True
        print(book)
        context = {
            "book":book,
            "isAdded":isAdded,
        }
        return HttpResponse(template.render(context,request))
    else:
        isAdded = False
        print(book)
        context = {
            "book":book,
            "isAdded":isAdded,
        }
        return HttpResponse(template.render(context,request))

    

