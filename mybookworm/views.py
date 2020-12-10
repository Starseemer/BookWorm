from django.db.models.fields import NullBooleanField
from re import sub, template
from typing import SupportsBytes
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import json, requests 
from .models import Book

def index(request):
    #Render plain HTML
    return render(request, 'mybookworm/index.html')

def search(request, search_word, page):
    #Check if POST request recieved
    if request.method == "POST":
        #Check if user wants to delete or add the book to bookmarks table
        if(request.POST.get("isAdd") == "add"):
            #Create new book entity in the table with the is as isbn13
            Book.objects.create(id=request.POST.get("book_id"), 
            title=request.POST.get("title"),
            subtitle=request.POST.get("subtitle"),
            price=request.POST.get("price"),
            url=request.POST.get("img_url"))
        else:
            #Delete the book that matches with recieved book_id
            Book.objects.filter(pk=request.POST.get("book_id")).delete()
        
    template = loader.get_template('mybookworm/search.html') #Create a template object
    books = [] #This array will be used to store the books that are recieved from API
    
    response = json.loads(requests.get("https://api.itbook.store/1.0/search/"+str(search_word)+"/"+str(page)).text) #Make a API call based on search query and assign to response
    #Scroll through all the books and add them to books array
    for book in response["books"]:
        #To be fair, just for fun
        if(float(book["price"][1:]) == 0.0):
            price = "Get it for free!"
        elif(float(book["price"][1:]) >= 50.0):
            price = "For " + book["price"]
        else:
            price = "Only for " + book["price"]
        
        isAdded = False
        if Book.objects.filter(pk=book["isbn13"]).exists(): #Check if this book already in the table, if so isAdded = True
            isAdded = True
        books.append((book["title"], book["subtitle"], price, book["image"], book["isbn13"], isAdded))
    max_page= int(int(response["total"]) / 10) + (int(response["total"]) % 10 > 0) #Find how many pages of search result are there
    
    #Create a context to send to front-end
    context = {
        'books':books,
        'search_word':search_word,
        'page':page,
        'max_page':max_page,
    }

    return HttpResponse(template.render(context, request))

def bookMarks(request):
    template = loader.get_template("mybookworm/bookmarks.html") #Create template object
    bookmarks = Book.objects.all() #Get all bookmarked books
    #Create a context to send to front-end
    context = {
        "bookmarks":bookmarks,
    }
    return HttpResponse(template.render(context,request))

def bookMarkDetails(request, book_id):
    book = None
    #Check if POST request recieved
    if request.method == "POST":
        #Check if user wants to delete or add the book to bookmarks table
        if(request.POST.get("isAdd") == "add"):
            #Create new book entity in the table with the is as isbn13
            Book.objects.create(id=request.POST.get("book_id"), 
            title=request.POST.get("title"),
            subtitle=request.POST.get("subtitle"),
            price=request.POST.get("price"),
            url=request.POST.get("img_url"))
        else:
            #Before deleting the we store its information into a varible since user might change his/her idea
            book = Book.objects.filter(pk=request.POST.get("book_id"))[0]
            #Delete the book that matches with recieved book_id
            Book.objects.filter(pk=request.POST.get("book_id")).delete()
    
    template = loader.get_template("mybookworm/bookmark_details.html")
    #Check if a book exists with this id
    if Book.objects.filter(pk=book_id).exists():
        book = Book.objects.filter(pk=book_id)[0] #Get book from table
        isAdded = True #Since it already in the table
        #Create a context to send to front-end
        context = {
            "book":book,
            "isAdded":isAdded,
        }
        return HttpResponse(template.render(context,request))
    else:
        isAdded = False #Since we know user just deleted this book
        #Create a context to send to front-end
        context = {
            "book":book,
            "isAdded":isAdded,
        }
        return HttpResponse(template.render(context,request))

    

