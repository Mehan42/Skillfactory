import json
import csv

def save_to_json(data: list, filename: str = 'movies.json'):
    """
    Сохраняет список словарей в JSON-файл.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Данные успешно сохранены в файл '{filename}'.")
    except IOError as e:
        print(f"Ошибка при сохранении файла {filename}: {e}")

def save_to_csv(data: list, filename: str = 'movies.csv'):
    """
    Сохраняет список словарей в CSV-файл.
    """
    if not data:
        print("Нет данных для сохранения в CSV.")
        return

    # Определяем заголовки из ключей первого словаря
    headers = data[0].keys()

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Данные успешно сохранены в файл '{filename}'.")
    except IOError as e:
        print(f"Ошибка при сохранении файла {filename}: {e}")
