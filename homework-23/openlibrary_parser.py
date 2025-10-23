import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import random


class OpenLibraryParser:
    """
    Парсер для получения данных о книгах с Open Library
    """
    
    def __init__(self):
        self.base_url = "https://openlibrary.org"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.books_data = []
    
    def get_subject_books(self, subject="fiction", limit=50):
        """
        Получает книги по указанной теме
        """
        print(f"Получение книг по теме: {subject}")
        
        # Используем API для получения книг по теме
        api_url = f"{self.base_url}/subjects/{subject}.json"
        params = {"limit": limit}
        
        try:
            response = requests.get(api_url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            books = []
            for work in data.get("works", []):
                book = {
                    "title": work.get("title", "N/A"),
                    "author": "N/A",
                    "year": work.get("first_publish_year", "N/A"),
                    "edition_count": work.get("edition_count", 0),
                    "subject": subject
                }
                
                # Получаем имя автора, если доступно
                authors = work.get("authors", [])
                if authors:
                    # Получаем полное имя автора через отдельный запрос
                    author_key = authors[0].get("key", "")
                    if author_key:
                        author_url = f"{self.base_url}{author_key}.json"
                        try:
                            author_response = requests.get(author_url, headers=self.headers)
                            if author_response.status_code == 200:
                                author_data = author_response.json()
                                book["author"] = author_data.get("name", "N/A")
                        except:
                            book["author"] = authors[0].get("name", "N/A")
                
                books.append(book)
                
                # Добавляем небольшую задержку, чтобы не перегружать сервер
                time.sleep(random.uniform(0.1, 0.3))
            
            return books
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе данных: {e}")
            return []
    
    def get_top_books(self, limit=50):
        """
        Получает топ книг (популярные книги на главной странице)
        """
        print("Получение топ книг с главной страницы...")
        
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ищем популярные книги (обычно они в специальных блоках)
            books = []
            
            # Популярные книги в слайдере "Books We Love"
            love_books = soup.find('div', {'id': 'books-we-love'})
            if love_books:
                book_elements = love_books.find_all('div', class_='book')
            else:
                # Альтернативный селектор для книг на главной странице
                book_elements = soup.find_all('div', class_='book')
            
            for book_elem in book_elements[:limit]:
                try:
                    title_elem = book_elem.find('a', class_='title')
                    author_elem = book_elem.find('a', class_='author')
                    
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    author = author_elem.get_text(strip=True) if author_elem else "N/A"
                    
                    if title != "N/A":
                        book = {
                            "title": title,
                            "author": author,
                            "year": "N/A",  # Год не всегда доступен на главной
                            "edition_count": 0,
                            "subject": "top_books"
                        }
                        books.append(book)
                except:
                    continue
            
            return books
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при парсинге главной страницы: {e}")
            return []
    
    def sort_books(self, books, sort_by_title=True, sort_by_year=True, sort_by_rating=False):
        """
        Сортирует книги по нескольким критериям
        Для рейтинга используем edition_count как приближенный показатель популярности
        """
        if not books:
            return books
        
        # Сортировка по году (убыванию), затем по названию (алфавитный порядок)
        sorted_books = sorted(books, 
                             key=lambda x: (
                                 x['year'] if x['year'] != 'N/A' else 0,  # Для сортировки по году
                                 x['title']  # Для сортировки по названию
                             ), 
                             reverse=sort_by_year)
        
        # Если нужно сортировать по "рейтингу" (используем edition_count как приближенный рейтинг)
        if sort_by_rating:
            sorted_books = sorted(sorted_books, 
                                 key=lambda x: x['edition_count'], 
                                 reverse=True)
        
        return sorted_books
    
    def save_to_json(self, data, filename='openlibrary_books.json'):
        """Сохраняет данные в JSON файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Данные успешно сохранены в файл '{filename}'.")
        except IOError as e:
            print(f"Ошибка при сохранении файла {filename}: {e}")
    
    def save_to_csv(self, data, filename='openlibrary_books.csv'):
        """Сохраняет данные в CSV файл"""
        if not data:
            print("Нет данных для сохранения в CSV.")
            return

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['title', 'author', 'year', 'edition_count', 'subject']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Данные успешно сохранены в файл '{filename}'.")
        except IOError as e:
            print(f"Ошибка при сохранении файла {filename}: {e}")
    
    def parse(self, subject="fiction", limit=50):
        """
        Основной метод для парсинга книг
        """
        print("Запуск парсера Open Library...")
        
        # Получаем книги по теме
        books = self.get_subject_books(subject, limit)
        
        if not books:
            print("Не удалось получить книги по API, пробуем альтернативный метод...")
            books = self.get_top_books(limit)
        
        if books:
            print(f"Получено {len(books)} книг")
            
            # Сортируем книги по году (по убыванию), названию (по алфавиту) и edition_count (как рейтинг)
            sorted_books = self.sort_books(books, sort_by_year=True, sort_by_rating=True)
            
            print("Данные отсортированы по году (по убыванию), рейтингу (по популярности) и названию (по алфавиту)")
            
            # Выводим первые 10 отсортированных книг
            print("\nТоп-10 отсортированных книг:")
            print(f"{'Название':<40} {'Автор':<30} {'Год':<6} {'Издания':<10}")
            print("-" * 90)
            for book in sorted_books[:10]:
                title = book['title'][:37] + "..." if len(book['title']) > 40 else book['title']
                author = book['author'][:27] + "..." if len(book['author']) > 30 else book['author']
                year = book['year']
                editions = book['edition_count']
                print(f"{title:<40} {author:<30} {year:<6} {editions:<10}")
            
            return sorted_books
        else:
            print("Не удалось получить данные о книгах")
            return []


def main():
    parser = OpenLibraryParser()
    
    # Парсим книги по теме "fiction"
    books_data = parser.parse(subject="fiction", limit=30)
    
    if books_data:
        # Сохраняем данные
        parser.save_to_json(books_data, 'openlibrary_fiction_books.json')
        parser.save_to_csv(books_data, 'openlibrary_fiction_books.csv')
        
        print(f"\nПарсинг завершен успешно!")
        print(f"Сохранено {len(books_data)} книг в форматах JSON и CSV")
    else:
        print("Не удалось получить данные для сохранения")


if __name__ == "__main__":
    main()