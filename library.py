import json 
import os
from enum import Enum


class BookStatus(Enum):
    InStock = 'в наличии'
    Given = 'выдана'

class Book:
    '''Класс, представляющий книгу в библиотеке'''

    def __init__(
        self, 
        title: str, 
        author: str, 
        year: int, 
        status: BookStatus = BookStatus.InStock
    ) -> None:
        '''
        Инициализация книги.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param status: Статус книги (по умолчанию "в наличии").
        '''
        self.id: int | None = None # идентификатор будет устоновлен позже
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        '''Преобразует объект книги в словарь для сохранения в JSON.'''
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status.value
        }
        

class Library:
    '''Класс, представляющий библиотеку'''
    
    def __init__(self, filename: str) -> None:
        '''
        Инициализация библиотеки.

        :param filename: Имя файла для хранения данных библиотеки
        '''
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self) -> None:
        '''Загружает книги из файла, если он существует.'''
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [self.create_book_from_dict(book_in_dict) for book_in_dict in data]

    def create_book_from_dict(self, data: dict) -> Book:
        '''
        Создает объект книги из словаря.

        :param data: Словарь с данными книги.
        :return: Объект книги.
        '''
        book = Book(data['title'], data['author'], data['year'], data['status'])
        book.id = data['id']
        return book

    def add_book(self, title: str, author: str, year: int) -> Book:
        '''
        Добавляет новую книгу в библиотеку.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :return: Объект книги.
        '''
        book = Book(title, author, year)
        book.id = self.generate_id()
        self.books.append(book)
        self.save_books()
        return book

    def generate_id(self) -> int:
        '''Генерирует уникальный идентификатор для новой книги.'''
        max_id = max([book.id for book in self.books if book.id is not None], default=-1)
        return max_id + 1

    def save_books(self) -> None:
        '''Сохраняет список книг в файл в формате JSON.'''
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(
                [book.to_dict() for book in self.books], 
                file, 
                ensure_ascii=False, 
                indent=4
            )

    def remove_book(self, book_id: int) -> None:
        '''
        Удаляет книгу из библиотеки по ID.

        :param book_id: ID книги для удаления.
        :raises ValueError: Если книга с данным ID не найдена.
        '''
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return
        raise ValueError("Книга с данным ID не найдена.")

    def search_books(self, query: str) -> list:
        '''
        Ищет книги по названию, автору или году.

        :param query: Запрос для поиска.
        :return: Список найденных книг.
        '''
        query = query.lower()
        results = [book for book in self.books if query in book.title.lower() 
            or query in book.author.lower() 
            or query in str(book.year)]
        return results

    def display_books(self):
        for book in self.books:
            print(f'ID: {book.id}, Название: {book.title}, \
            Автор: {book.author}, Год: {book.year}, Статус: {book.status.value}')

    def change_status(self, book_id: int, new_status: BookStatus):
        for book in self.books:
            if book.id == book_id:
                if book.status != new_status:
                    book.status = new_status
                    self.save_books()
                return book
        raise ValueError('Книга с данными ID не найдена.')

def main():
    pass


if __name__=='__main__':
    main()

