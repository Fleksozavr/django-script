import random

from datacenter.models import Mark, Schoolkid, Chastisement, Commendation, Lesson, Subject


def fix_marks(child_object):
    bad_marks = Mark.objects.filter(schoolkid=child_object, points__in=[2, 3])
    if bad_marks.count() == 0:
        print('Плохих оценок не найдено')
        return
    else:
        print(f'Найдено плохих оценок: {bad_marks.count()}')
    try:
        fixmarks_counter = 0
        for badmark in bad_marks:
            badmark.points = 5
            badmark.save()
            fixmarks_counter += 1
        print(f'{fixmarks_counter} плохих оценок было успешно удалено.')
    except Exception as err:
        print(f'Error: {err}')


def fix_chastisements(child_object):
    try:       
        deleted_count, _ = Chastisement.objects.filter(schoolkid=child_object).delete()
        print(f'{deleted_count} замечаний было успешно удалено.')
    except Chastisement.DoesNotExist:
        print('Замечаний нет')


def fix_commendation(child_object, subject_title, commendations_list):
    subject = get_object_or_404(Subject, title=subject_title, year_of_study=child_object.year_of_study)

    lesson = Lesson.objects.filter(
        subject=subject,
        year_of_study=child_object.year_of_study,
        group_letter=child_object.group_letter
    ).order_by('-date').first()
    if not lesson:
         print('Урок по данному предмету для ученика не найден.')
         return
    try:
        Commendation.objects.create(
            text=random.choice(commendations_list),
            created=lesson.date,
            schoolkid=child_object,
            subject=lesson.subject,
            teacher=lesson.teacher
        )
        print('Похвала успешно поставлена.')
    except Exceptrion as err:
        print(f"Error:, {err}")


def fix_menu():
    name = input('Введите Фамилию Имя ученика которого хотите найти в базе данных: ')
    try:     
        schoolkid_object = get_object_or_404(Schoolkid, full_name__contains=name)
        if schoolkid_object:
            print('Ученик был успешно найден!')
            print("""
Доступные функции:
1. Исправить плохую оценку
2. Удалить замечание
3. Поставить похвалу
""")
            choice = int(input('Ваш выбор: '))
            if choice == 1:
                fix_marks(schoolkid_object)
            elif choice == 2:
                fix_chastisements(schoolkid_object)
            elif choice == 3:
                subject_title = input('Введите название урока: ')
                commendations_list = ['Good job!', 'Well played.', 'Very Nice!', 'Лучший из лучших', 
                                      'Король.', 'Как же он силен, как же он умен']
                fix_commendation(schoolkid_object, subject_title, commendations_list)   
            else:
                print('Введено некорректное значение')    
    except Schoolkid.MultipleObjectsReturned:
        print("Было найдено более одного ученика.")
    except Schoolkid.DoesNotExist:
        print('Не было найдено ни одного ученика')
