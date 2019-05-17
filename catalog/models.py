from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

class Genre(models.Model):
    name = models.CharField('Наименование', max_length=200, help_text='Жанр книги. Например, Фантастика, Детектив, Поэзия и т.п.')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField('Наименование', max_length=200, help_text='Язык издания книги. Например, Русский, English, 中國 и т.п.')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField('Наименование', max_length=200, help_text='Название этой книги.')
    author = models.ForeignKey('Author', verbose_name='Автор', on_delete=models.SET_NULL, null=True, help_text='Автор этой книги.')
    summary = models.TextField('О книге', max_length=1000, help_text='Краткое описание этой книги.')
    isbn = models.CharField('ISBN', max_length=13, help_text='13-ти символьный <a href="https://www.isbn-international.org/content/what-isbn">номер ISBN</a>')
    genre = models.ManyToManyField('Genre', verbose_name='Жанр', help_text='Жанр, соответствующий этой книге.')
    language = models.ForeignKey('Language', verbose_name='Язык', on_delete=models.SET_NULL, null=True, help_text='Язык издания этой книги.')

    class Meta:
        ordering = ['title']
        permissions = (("can_change_books_data", "Add, edit, delete books"),)

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Жанр произведения'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный идентификатор этого экземпляра книги в библиотеке.')
    book = models.ForeignKey('Book', verbose_name='Книга', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField('Штамп', max_length=200, help_text='Информация об экземпляре. Например, издательство, переводчик, год, номер экземпляра в библиотеке')
    due_back = models.DateField(verbose_name='Дата возврата', null=True, blank=True, help_text='Дата ожидаемого возврата книги.')
    borrower = models.ForeignKey(User, verbose_name='Читатель', on_delete=models.SET_NULL, null=True, blank=True, help_text='Читатель, арендующий книгу.')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'На оформлении'),
        ('o', 'Выдана'),
        ('a', 'Доступна'),
        ('r', 'В резерве'),
    )

    status = models.CharField('Доступность', max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Статус доступности книги')

    class Meta:
        ordering = ['book']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)

class Author(models.Model):
    first_name = models.CharField('Имя', max_length=100, help_text='Имя автора книги.')
    last_name = models.CharField('Фамилия', max_length=100, help_text='Фамилия автора книги.')
    first_name_ml = models.CharField('Имя (родной язык)', max_length=100, null=True, blank=True, help_text='Имя автора на его родном языке.')
    last_name_ml = models.CharField('Фамилия (родной язык)', max_length=100, null=True, blank=True, help_text='Фамилия автора на его родном языке.')
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True, help_text='Дата рождения автора (если известна).')
    date_of_death = models.DateField('Дата смерти', null=True, blank=True, help_text='Дата смерти автора (если известна).')

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (("can_change_authors_data", "Add, edit, delete authors"),)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)
