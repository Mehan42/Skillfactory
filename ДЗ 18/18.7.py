import random

def main():
    # список учеников
    students = ['Аполлон', 'Ярослав', 'Александра', 'Дарья', 'Ангелина']
    # отсортируем список учеников
    students.sort()
    # список предметов
    classes = ['Математика', 'Русский язык', 'Информатика']
    # пустой словарь с оценками по каждому ученику и предмету
    students_marks = {}
    # сгенерируем данные по оценкам:
    # цикл по ученикам
    for student in students:
        students_marks[student] = {}
        # цикл по предметам
        for class_ in classes:
            marks = [random.randint(1,5) for i in range(3)]
            students_marks[student][class_] = marks

    # выводим получившийся словарь с оценками:
    for student in students:
        print(f'{student}: {students_marks[student]}')

    print('''
    Список команд:
    1. Добавить оценки ученика по предмету
    2. Вывести средний балл по всем предметам по каждому ученику
    3. Вывести все оценки по всем ученикам
    4. Удалить оценку ученика по предмету
    5. Редактировать оценку ученика по предмету
    6. Добавить нового ученика
    7. Удалить ученика
    8. Добавить новый предмет
    9. Удалить предмет
    10. Вывести все оценки определенного ученика
    11. Вывести средний балл по каждому предмету для определенного ученика
    12. Вывести список всех учеников и предметов
    13. Выход из программы
    ''')

    while True:
        try:
            command = int(input('\nВведите команду: '))

            if command == 1:
                print('1. Добавить оценку ученика по предмету')
                student = input('Введите имя ученика: ')
                class_ = input('Введите предмет: ')
                mark = int(input('Введите оценку: '))

                if student in students_marks and class_ in students_marks[student]:
                    students_marks[student][class_].append(mark)
                    print(f'Для {student} по предмету {class_} добавлена оценка {mark}')
                else:
                    print('ОШИБКА: неверное имя ученика или название предмета')

            elif command == 2:
                print('2. Вывести средний балл по всем предметам по каждому ученику')
                for student in students:
                    print(f'\n{student}:')
                    for class_ in classes:
                        if class_ in students_marks[student]:
                            marks = students_marks[student][class_]
                            avg = sum(marks) / len(marks)
                            print(f'  {class_} - {avg:.2f}')

            elif command == 3:
                print('3. Вывести все оценки по всем ученикам')
                for student in students:
                    print(f'\n{student}:')
                    for class_ in classes:
                        if class_ in students_marks[student]:
                            print(f'  {class_} - {students_marks[student][class_]}')

            elif command == 4:
                print('4. Удалить оценку ученика по предмету')
                student = input('Введите имя ученика: ')
                class_ = input('Введите предмет: ')

                if student in students_marks and class_ in students_marks[student]:
                    print(f'Оценки {student} по {class_}: {students_marks[student][class_]}')
                    mark_index = int(input('Введите индекс оценки для удаления (начиная с 0): '))

                    if 0 <= mark_index < len(students_marks[student][class_]):
                        removed_mark = students_marks[student][class_].pop(mark_index)
                        print(f'Удалена оценка {removed_mark}')
                    else:
                        print('ОШИБКА: неверный индекс оценки')
                else:
                    print('ОШИБКА: неверное имя ученика или название предмета')

            elif command == 5:
                print('5. Редактировать оценку ученика по предмету')
                student = input('Введите имя ученика: ')
                class_ = input('Введите предмет: ')

                if student in students_marks and class_ in students_marks[student]:
                    print(f'Оценки {student} по {class_}: {students_marks[student][class_]}')
                    mark_index = int(input('Введите индекс оценки для редактирования (начиная с 0): '))
                    new_mark = int(input('Введите новую оценку: '))

                    if 0 <= mark_index < len(students_marks[student][class_]):
                        old_mark = students_marks[student][class_][mark_index]
                        students_marks[student][class_][mark_index] = new_mark
                        print(f'Оценка {old_mark} изменена на {new_mark}')
                    else:
                        print('ОШИБКА: неверный индекс оценки')
                else:
                    print('ОШИБКА: неверное имя ученика или название предмета')

            elif command == 6:
                print('6. Добавить нового ученика')
                new_student = input('Введите имя нового ученика: ')

                if new_student not in students:
                    students.append(new_student)
                    students.sort()
                    students_marks[new_student] = {}

                    for class_ in classes:
                        students_marks[new_student][class_] = []

                    print(f'Ученик {new_student} добавлен')
                else:
                    print('ОШИБКА: ученик с таким именем уже существует')

            elif command == 7:
                print('7. Удалить ученика')
                student = input('Введите имя ученика для удаления: ')

                if student in students:
                    students.remove(student)
                    del students_marks[student]
                    print(f'Ученик {student} удален')
                else:
                    print('ОШИБКА: ученик не найден')

            elif command == 8:
                print('8. Добавить новый предмет')
                new_class = input('Введите название нового предмета: ')

                if new_class not in classes:
                    classes.append(new_class)

                    for student in students:
                        students_marks[student][new_class] = []

                    print(f'Предмет {new_class} добавлен')
                else:
                    print('ОШИБКА: предмет с таким названием уже существует')

            elif command == 9:
                print('9. Удалить предмет')
                class_ = input('Введите название предмета для удаления: ')

                if class_ in classes:
                    classes.remove(class_)

                    for student in students:
                        if class_ in students_marks[student]:
                            del students_marks[student][class_]

                    print(f'Предмет {class_} удален')
                else:
                    print('ОШИБКА: предмет не найден')

            elif command == 10:
                print('10. Вывести все оценки определенного ученика')
                student = input('Введите имя ученика: ')

                if student in students_marks:
                    print(f'\nВсе оценки {student}:')
                    for class_ in classes:
                        if class_ in students_marks[student]:
                            print(f'  {class_} - {students_marks[student][class_]}')
                else:
                    print('ОШИБКА: ученик не найден')

            elif command == 11:
                print('11. Вывести средний балл по каждому предмету для определенного ученика')
                student = input('Введите имя ученика: ')

                if student in students_marks:
                    print(f'\nСредние баллы {student}:')
                    for class_ in classes:
                        if class_ in students_marks[student] and students_marks[student][class_]:
                            marks = students_marks[student][class_]
                            avg = sum(marks) / len(marks)
                            print(f'  {class_} - {avg:.2f}')
                        else:
                            print(f'  {class_} - нет оценок')
                else:
                    print('ОШИБКА: ученик не найден')

            elif command == 12:
                print('12. Вывести список всех учеников и предметов')
                print('\nУченики:')
                for student in students:
                    print(f'  - {student}')
                print('\nПредметы:')
                for class_ in classes:
                    print(f'  - {class_}')

            elif command == 13:
                print('13. Выход из программы')
                break

            else:
                print('ОШИБКА: неверная команда')

        except ValueError:
            print('ОШИБКА: введите число команды')
        except Exception as e:
            print(f'ОШИБКА: {e}')

if __name__ == "__main__":
    main()
