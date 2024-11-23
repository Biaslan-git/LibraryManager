import unittest
import json
import os, sys
from io import StringIO

from library import Book, BookStatus, Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        '''Создание тестовой библиотеки перед запуском тестов.'''
        self.test_library_filename = 'test_library.json'
        self.library = Library(self.test_library_filename)

    def tearDown(self):
        '''Удаление тестовой библиотеки после завершения тестов.'''
        if os.path.exists(self.test_library_filename):
            os.remove(self.test_library_filename)

    def check_book_in_library(
            self, 
            book_id: int, 
            title: str, 
            author: str, 
            year: int, 
            status: BookStatus,
            item_id: int | None = None, 
    ):
        '''Функция для проверки существования книги в библотеке.'''
        item_id = item_id or book_id
        self.assertEqual(self.library.books[item_id].id, book_id)
        self.assertEqual(self.library.books[item_id].title, title)
        self.assertEqual(self.library.books[item_id].author, author)
        self.assertEqual(self.library.books[item_id].year, year)
        self.assertEqual(self.library.books[item_id].status, status)
        self.assertEqual(self.library.books[item_id].status.value, status.value)

    def test_add_book(self):
        '''Тестирование добавления книги.'''
        self.library.add_book("Test Book", "Test Author", 2023)
        
        self.assertEqual(len(self.library.books), 1)
        self.check_book_in_library(0, "Test Book", "Test Author", 2023, BookStatus.InStock)

        self.library.add_book("Test Book 2", "Test Author 2", 2024)
        
        self.assertEqual(len(self.library.books), 2)
        self.check_book_in_library(1, "Test Book 2", "Test Author 2", 2024, BookStatus.InStock)

    def test_remove_book(self):
        '''Тестирование удаления книги.'''
        self.library.add_book("Test Book", "Test Author", 2023)
        self.library.add_book("Test Book 2", "Test Author 2", 2024)
        self.library.remove_book(book_id=1)

        self.assertEqual(len(self.library.books), 1)
        self.check_book_in_library(0, "Test Book", "Test Author", 2023, BookStatus.InStock)

    def test_raise_when_try_remove_not_exists_book(self):
        '''Тестирование вызова ошибки ValueError при попытке удаления несуществующей книги.'''
        self.library.add_book("Test Book", "Test Author", 2023)
        with self.assertRaises(ValueError):
            self.library.remove_book(999)

    def test_search_books(self):
        '''Тестирование поиска книг.'''
        self.library.add_book("Test Book 1", "Test Author 1", 2023)
        res1 = self.library.search_books(query='book 1')
        res2 = self.library.search_books(query='author 1')
        res3 = self.library.search_books(query='2023')

        self.assertEqual(res1[0].id, 0)
        self.assertEqual(res2[0].id, 0)
        self.assertEqual(res3[0].id, 0)

    def test_display_books(self):
        '''Тестирование отображения всех книг'''
        book1 = self.library.add_book("Test Book 1", "Test Author 1", 2023)
        book2 = self.library.add_book("Test Book 2", "Test Author 2", 2024)

        self.maxDiff = None
        capture_output = StringIO()
        sys.stdout = capture_output

        self.library.display_books()

        sys.stdout = sys.__stdout__
        output = capture_output.getvalue().strip()

        correct_output = f'ID: {book1.id}, Название: {book1.title}, \
            Автор: {book1.author}, Год: {book1.year}, Статус: {book1.status.value}\n' + \
            f'ID: {book2.id}, Название: {book2.title}, \
            Автор: {book2.author}, Год: {book2.year}, Статус: {book2.status.value}'

        self.assertEqual(output, correct_output)

    def test_change_status(self):
        book1 = self.library.add_book("Test Book 1", "Test Author 1", 2023)
        book2 = self.library.add_book("Test Book 2", "Test Author 2", 2024)
        self.library.change_status(book_id=0, new_status=BookStatus.Given)
        self.library.change_status(book_id=1, new_status=BookStatus.Given)

        self.assertEqual(book1.status, BookStatus.Given)
        self.assertEqual(book2.status, BookStatus.Given)




if __name__=='__main__':
    unittest.main()
