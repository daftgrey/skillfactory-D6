from django.urls import path
from .views import *


urlpatterns = [
    path('', availible_books.as_view(), name='home'),
    path('publishers/', publishers.as_view(), name='pub_list'),
    path('author/create/', AuthorEdit.as_view(), name='author_create'),
    path('authors/', AuthorList.as_view(), name='author_list'),
    path('author/create_many/', author_create_many, name='author_create_many'),
    path('author_book/create_many/', books_authors_create_many, name='author_book_create_many'),
    path('borrowed_books/', friends.as_view(), name='b_books'),
    path('friend/create/', FriendEdit.as_view(), name='friend_create'),
    path('friends/', FriendList.as_view(), name='friend_list'),
    path('books/create', BookEdit.as_view(), name='book_create'),
    path('books/', books.as_view(), name='books'),
]