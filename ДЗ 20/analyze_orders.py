import json

def analyze_orders(filename="orders_july_2023.json"):
    """
    Считывает данные о заказах из JSON-файла, обрабатывает их
    и выводит статистику за июль 2023 года.
    """
    try:
        # Шаг 1: Считываем данные из файла и преобразуем их в словарь
        with open(filename, 'r', encoding='utf-8') as f:
            orders_data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return
    except json.JSONDecodeError:
        print(f"Ошибка: Не удалось декодировать JSON из файла '{filename}'.")
        return

    # Шаг 2: Инициализация переменных для хранения результатов

    # Для самого дорогого заказа
    max_price_order_id = ''
    max_price = 0

    # Для заказа с самым большим количеством товаров
    max_quantity_order_id = ''
    max_quantity = 0

    # Для подсчета заказов по дням
    daily_orders_count = {}

    # Для подсчета заказов по пользователям
    user_order_counts = {}

    # Для подсчета суммарной стоимости заказов по пользователям
    user_total_spent = {}

    # Для расчета средних значений
    total_order_value = 0
    total_items_sold = 0
    total_orders = 0

    # Шаг 3: Обработка данных в цикле
    for order_id, details in orders_data.items():
        # Извлекаем данные текущего заказа
        price = details['price']
        quantity = details['quantity']
        user_id = details['user_id']
        date = details['date']

        # 1. Находим самый дорогой заказ
        if price > max_price:
            max_price = price
            max_price_order_id = order_id

        # 2. Находим заказ с самым большим количеством товаров
        if quantity > max_quantity:
            max_quantity = quantity
            max_quantity_order_id = order_id

        # 3. Считаем количество заказов по дням
        # .get(date, 0) вернет 0, если даты еще нет в словаре
        daily_orders_count[date] = daily_orders_count.get(date, 0) + 1

        # 4. Считаем количество заказов для каждого пользователя
        user_order_counts[user_id] = user_order_counts.get(user_id, 0) + 1

        # 5. Считаем суммарную стоимость заказов для каждого пользователя
        user_total_spent[user_id] = user_total_spent.get(user_id, 0) + price

        # Обновляем общие суммы для расчета средних значений
        total_order_value += price
        total_items_sold += quantity
        total_orders += 1

    # Шаг 4: Вычисляем финальные результаты после цикла

    # 3. Находим день с наибольшим количеством заказов
    # max(daily_orders_count, key=daily_orders_count.get) находит ключ (дату) с максимальным значением
    max_orders_day = max(daily_orders_count, key=daily_orders_count.get)
    max_orders_count = daily_orders_count[max_orders_day]

    # 4. Находим пользователя с самым большим количеством заказов
    max_orders_user = max(user_order_counts, key=user_order_counts.get)
    max_orders_by_user = user_order_counts[max_orders_user]

    # 5. Находим пользователя с самой большой суммарной стоимостью заказов
    max_spent_user = max(user_total_spent, key=user_total_spent.get)
    max_spent_amount = user_total_spent[max_spent_user]

    # 6. Вычисляем среднюю стоимость заказа
    average_order_cost = total_order_value / total_orders if total_orders > 0 else 0

    # 7. Вычисляем среднюю стоимость товара
    average_item_price = total_order_value / total_items_sold if total_items_sold > 0 else 0

    # Шаг 5: Выводим результаты
    print("--- Анализ заказов за июль 2023 ---")
    print(f"1. Номер самого дорогого заказа: {max_price_order_id}, стоимость: {max_price}")
    print(f"2. Номер заказа с самым большим количеством товаров: {max_quantity_order_id}, количество: {max_quantity}")
    print(f"3. День с наибольшим количеством заказов: {max_orders_day}, количество заказов: {max_orders_count}")
    print(f"4. Пользователь с самым большим количеством заказов: {max_orders_user}, количество заказов: {max_orders_by_user}")
    print(f"5. Пользователь с самой большой суммарной стоимостью заказов: {max_spent_user}, общая сумма: {max_spent_amount}")
    print(f"6. Средняя стоимость заказа: {average_order_cost:.2f}")
    print(f"7. Средняя стоимость товара: {average_item_price:.2f}")


# Запускаем функцию анализа
if __name__ == "__main__":
    analyze_orders()