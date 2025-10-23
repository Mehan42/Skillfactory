from openlibrary_parser import OpenLibraryParser

def main():
    """
    Главная функция проекта для парсинга Open Library.
    """
    print("=== Парсер Open Library ===")
    print("Сбор данных о книгах с openlibrary.org")
    
    # Создаем экземпляр парсера
    parser = OpenLibraryParser()
    
    # Парсим книги по теме "fiction" (можно изменить на другую тему)
    books_data = parser.parse(subject="fiction", limit=50)
    
    if books_data:
        print(f"\nНачинаем сохранение {len(books_data)} книг...")
        
        # Сохраняем в JSON
        parser.save_to_json(books_data, 'openlibrary_books.json')
        
        # Сохраняем в CSV
        parser.save_to_csv(books_data, 'openlibrary_books.csv')
        
        print("\nДанные успешно сохранены!")
        print("- openlibrary_books.json")
        print("- openlibrary_books.csv")
    else:
        print("Не удалось получить данные о книгах.")


if __name__ == "__main__":
    main()