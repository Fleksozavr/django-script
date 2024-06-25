import random

from datacenter.models import Mark, Schoolkid, Chastisement, Commendation, Lesson, Subject


def fix_marks(child_object):
    child = Mark.objects.filter(schoolkid=child_object)
    bad_marks = child.filter(points__in=[2,3])
    if bad_marks.count() == 0:
        print('Плохих оценок не найдено')
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


def fix_chastisements(chlid_object):
    chastisements = Chastisement.objects.filter(schoolkid=chlid_object)
    if chastisements.count() == 0:
        print('Замечаний не найдено')
    else:
        print(f'Найдено {chastisements.count()} замечаний')
    try:
        for chastisement in chastisements:
            chastisement.delete()
        print(f'{chastisements.count()} замечаний было успешно удалено.')
    except Exception as err:
        print(f'Error: {err}') 


def fix_commendation(child_object, subject_title):
    global COMMENDATIONS_LIST
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
            text=random.choice(COMMENDATIONS_LIST),
            created=lesson.date,
            schoolkid=child_object,
            subject=lesson.subject,
            teacher=lesson.teacher
        )
        print('Похвала успешно поставлена.')
    except Subject.MultipleObjectsReturned:
        print('Было найдено несколько предметов по указанным параметрам.')
    except Subject.DoesNotExist:
        print('Не было найдено ни одной записи в базе данных.')


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
                fix_commendation(schoolkid_object, subject_title)   
            else:
                print('Введено некорректное значение')    
    except Schoolkid.MultipleObjectsReturned:
        print("Было найдено более одного ученика.")
    except Schoolkid.DoesNotExist:
        print('Не было найдено ни одного ученика')
