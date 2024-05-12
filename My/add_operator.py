import requests
from datetime import datetime, timedelta

from My.users_class import get_user_data, format_user_data
from My.wp_connection import headers


def create_event(event_data):
    events_api_url = "https://mwtvoper.site/wp-json/tribe/events/v1/events"
    response = requests.post(events_api_url, json=event_data, headers=headers)
    if response.status_code == 201:
        new_event_data = response.json()
        print("Событие успешно добавлено:")
        print(new_event_data)
        return new_event_data
    else:
        print("Ошибка при добавлении события:", response.status_code)
        return None


def create_events_oper(start_date, num_cycles, username):
    events = []

    # Задаем список событий для каждого цикла
    cycle_events = [
        {'title': f'Дежурство в студии {name}', 'location': 'Студия на тверской', 'description': f'{username}',
         'categories': ['Графики работы'], 'tags': [name]},
        {'title': f'Дежурство в студии {name}', 'location': 'Студия на тверской', 'description': f'{username}',
         'categories': ['Графики работы'], 'tags': [name]},
        {'title': f'Выезды/подхват {name}', 'description': f'{username}', 'categories': ['Графики работы'],
         'tags': [name]},
        {'title': f'Выезды/подхват {name}', 'description': f'{username}', 'categories': ['Графики работы'],
         'tags': [name]},
        {'title': f'Выходной {name}', 'description': f'{username}', 'categories': ['Графики работы'],
         'tags': [name]},
        {'title': f'Выходной {name}', 'description': f'{username}', 'categories': ['Графики работы'],
         'tags': [name]}
    ]

    # Повторяем создание событий нужное количество раз
    for _ in range(num_cycles):
        for event_data in cycle_events:
            event_data['start_date'] = start_date.strftime('%Y-%m-%d 11:00:00')
            event_data['end_date'] = start_date.strftime('%Y-%m-%d 23:00:00')
            events.append(event_data)
            create_event(event_data)

            # Переходим к следующей дате
            start_date += timedelta(days=1)

    return events


# Текущая дата
start_date = datetime.strptime('2024-05-12', '%Y-%m-%d')
user_data = get_user_data("Prozorovskiy_Kirill")
name = user_data['name']
username = format_user_data(user_data, "Prozorovskiy_Kirill")
# Создаем события на 90 дней вперед (по x циклов по 6 дней)
events = create_events_oper(start_date, 20, username)



