from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect

from p_library.models import Book, Publisher, Author, Friend
from p_library.forms import AuthorForm, BookForm, FriendForm


class availible_books(ListView):
    model = Book
    context_object_name = "books"
    template_name = "availible_books.html"
    extra_context = {'title': 'Список книг в наличии'}


class books(ListView):
    model = Book
    context_object_name = "books"
    template_name = "index.html"
    extra_context = {'title': 'Список всех книг'}


class publishers(ListView):
    template_name = 'publishers.html'
    model = Publisher
    context_object_name = "publishers"
    extra_context = {'title': 'Список издателей'}


class friends(ListView):
    template_name = 'friends.html'
    model = Friend
    context_object_name = "friends"
    extra_context = {'title': 'Список должников'}


class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('author_create')
    template_name = 'author_edit.html'


class BookEdit(CreateView):
    form_class = BookForm
    template_name = 'book_edit.html'
    success_url = reverse_lazy('book_create')


class AuthorList(ListView):
    model = Author
    template_name = 'authors_list.html'
    extra_context = {'title': 'Список авторов'}


class FriendEdit(CreateView):
    form_class = FriendForm
    template_name = 'friend_edit.html'
    success_url = reverse_lazy('friend_create')


class FriendList(ListView):
    model = Friend
    template_name = 'friend_list.html'
    extra_context = {'title': 'Список друзей'}



def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm,
                                    extra=2)  # Первым делом, получим класс, который будет создавать наши формы. Обратите внимание на параметр `extra`, в данном случае он равен двум, это значит, что на странице с несколькими формами изначально будет появляться 2 формы создания авторов.
    if request.method == 'POST':  # Наш обработчик будет обрабатывать и GET и POST запросы. POST запрос будет содержать в себе уже заполненные данные формы
        author_formset = AuthorFormSet(request.POST, request.FILES,
                                       prefix='authors')  # Здесь мы заполняем формы формсета теми данными, которые пришли в запросе. Обратите внимание на параметр `prefix`. Мы можем иметь на странице не только несколько форм, но и разных формсетов, этот параметр позволяет их отличать в запросе.
        if author_formset.is_valid():  # Проверяем, валидны ли данные формы
            for author_form in author_formset:
                author_form.save()  # Сохраним каждую форму в формсете
            return HttpResponseRedirect(
                reverse_lazy('p_library:author_list'))  # После чего, переадресуем браузер на список всех авторов.
    else:  # Если обработчик получил GET запрос, значит в ответ нужно просто "нарисовать" формы.
        author_formset = AuthorFormSet(
            prefix='authors')  # Инициализируем формсет и ниже передаём его в контекст шаблона.
    return render(request, 'manage_authors.html', {'author_formset': author_formset})


def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(
        request,
        'manage_books_authors.html',
        {
            'author_formset': author_formset,
            'book_formset': book_formset,
        }
    )
