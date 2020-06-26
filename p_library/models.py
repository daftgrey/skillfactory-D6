from django.db import models


class Author(models.Model):
    full_name = models.TextField(verbose_name='ФИО автора')
    birth_year = models.SmallIntegerField(verbose_name='Год рождения')
    country = models.CharField(max_length=2, verbose_name='Страна')

    def __str__(self):
        return self.full_name


class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    year_release = models.SmallIntegerField(verbose_name='Год издания')
    pic = models.ImageField(upload_to='pics/%Y/%m/%d/', default='')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='ФИО автора')
    copy_count = models.IntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, null=True, blank=True, related_name='books', verbose_name='Издательство')
    friend = models.ForeignKey('Friend', on_delete=models.PROTECT, null=True, blank=True, related_name='borrowed_books', verbose_name='Имя друга')
    is_borrowed = models.BooleanField(default=False, verbose_name='Одолжена')

    def __str__(self):
        return self.title


class Publisher(models.Model):
    title = models.CharField(max_length=128, verbose_name='Наименование издателя')

    def __str__(self):
        return self.title


class Friend(models.Model):
    f_name = models.CharField(max_length=128, verbose_name='Имя друга')

    def __str__(self):
        return self.f_name
