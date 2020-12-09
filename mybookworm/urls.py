from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:search_word>/<int:page>', views.search, name='search'),
    path('bookmarks/', views.bookMarks, name='bookmarks'),
    path('bookmarks/<int:book_id>/', views.bookMarkDetails, name='book'),
] 
