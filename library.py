import json 
import os
from enum import Enum

import texts


class BookStatus(Enum):
    InStock = 'в наличии'
    Given = 'выдана'

    @classmethod
    def get_by_value(cls, value: str):
        '''Получение свойства по значению'''
        for item in cls:
            if item.value == value:
                return item

    @classmethod
    def get_numerate_statuses(cls) -> dict:
        '''Выводит доступные статусы'''
        i = 1
        result = {}
        for item in cls:
            result[i] = item
            i+=1
        return result

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
        book = Book(
            data['title'], 
            data['author'], 
            data['year'], 
            BookStatus.get_by_value(data['status']) or BookStatus.InStock
        )

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

    def display_books(self) -> list[int] | None:
        '''
        Выводит информацию о всех книгах в библиотеке.

        :return: Список из ID книг в библиотеке.
        '''
        if not self.books:
            print('Вы еще не добавили книги.')
            return
        book_ids = []
        for book in self.books:
            book_ids.append(book.id)
            print(texts.book_info_in_line.format(
                book.id, book.title, book.author, book.year, book.status.value
            ))
        print()
        return book_ids

    def change_status(self, book_id: int, new_status: BookStatus):
        '''
        Меняет статус книги.

        :param book_id: Идентификатор книги.
        :param new_status: Новый статус.
        :raises ValueError: Если книга с данным ID не найдена.
        :return: Книга с обновленным статусом.
        '''
        for book in self.books:
            if book.id == book_id:
                if book.status != new_status:
                    book.status = new_status
                    self.save_books()
                return book
        raise ValueError('Книга с данными ID не найдена.')


def main():
    '''Главная функция.'''
    library = Library('library.json')

    while True:
        print('Выберите действие:')
        print(texts.actions)
        choose = input('=> ')
        if choose.isdigit() and int(choose) in range(1, 6):
            try:
                if int(choose)!=4: print(texts.press_ctrl_c)
                match int(choose):
                    case 1:
                        add_book(library)
                    case 2:
                        remove_book(library)
                    case 3:
                        search_books(library)
                    case 4:
                        print()
                        library.display_books()
                    case 5:
                        change_status(library)
            except (KeyboardInterrupt, EOFError):
                print('\n\nОтмена.\n')
        else:
            print(texts.incorrect)

def add_book(library: Library):
    '''Интерактивное добавление книги'''
    title = input(texts.add_book[0])
    author = input(texts.add_book[1])
    while True:
        try:
            year = int(input(texts.add_book[2]))
            break
        except ValueError:
            print(texts.incorrect)

    book = library.add_book(title, author, year)
    print(texts.book_is_added.format(**book.to_dict()))
        

def remove_book(library: Library):
    '''Интерактивное удаление книги.'''
    book_ids = library.display_books()
    if not book_ids:
        print(texts.no_books)
        return
    while True:
        try:
            book_id = int(input(texts.enter_delete_id))
            try:
                library.remove_book(book_id)
                print(texts.book_success_removed)
                library.display_books()
                break
            except ValueError:
                print(texts.book_id_does_not_exists)
        except ValueError:
            print(texts.incorrect)
    

def search_books(library: Library):
    '''Интерактивный поиск книги.'''
    if not library.books:
        print(texts.no_books)
        return
    while True:
        query = input(texts.enter_search_query)
        books = library.search_books(query.strip())
        if books:
            for book in books:
                print(texts.book_info_in_line.format(
                    book.id, book.title, book.author, book.year, book.status.value
                ))
        else:
            print(texts.book_is_not_found)
            

def change_status(library: Library):
    '''Интерактивное изменение статуса книги.'''
    status_has_been_changed = False
    while not status_has_been_changed:
        book_ids = library.display_books()
        if not book_ids:
            print(texts.no_books)
            return
        try:
            book_id = int(input(texts.enter_change_id))
            if not book_id in book_ids:
                raise ValueError
            try:
                while True:
                    print(texts.available_statuses)
                    statuses_dict = BookStatus.get_numerate_statuses()
                    for num, status in statuses_dict.items():
                        print(f'{num}. {status.value}')
                    print()

                    try:
                        status_num = int(input(texts.enter_status_num))
                        book = library.change_status(book_id, statuses_dict[status_num])
                        print(texts.status_success_changed)
                        print(texts.book_info_in_line.format(
                            book.id, book.title, book.author, book.year, book.status.value
                        ))
                        print()
                        status_has_been_changed = True
                        break
                    except (KeyError, ValueError):
                        print(texts.incorrect)
            except ValueError:
                print(texts.book_id_does_not_exists)
        except ValueError:
            print(texts.incorrect)
        


if __name__=='__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nВыход.')
        exit()

