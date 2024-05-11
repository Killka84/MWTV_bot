import requests


from My.wp_connection import access_user, access_token, wp_url, headers


def get_events():
    headers = {"Authorization": "MWTV_Bot I3Gc zCNC zQPK SEFL 1WXx MRpt"}  # Замените на свой токен доступа
    events_api_url = f"{wp_url}/wp-json/tribe/events/v1/events"
    response = requests.get(events_api_url, headers=headers)
    if response.status_code == 200:
        events_data = response.json()
        return events_data
    else:
        print("Ошибка при получении данных о событиях:", response.status_code)
        return None

def display_events(events_data):
    # Получение списка событий
    events = events_data.get('events', [])
    print(events)

    # Вывод информации о каждом событии
    for event in events:
        print("Название:", event.get('title'))
        print("Дата и время начала:", event.get('start_date'))
        print("Дата и время окончания:", event.get('end_date'))
        print("Место проведения:", event.get('venue', {}).get('venue'))
        print("Адрес:", event.get('venue', {}).get('address'))
        print("----------------------")


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

# Данные нового события (пример)
new_event_data = {
    "title": "Новое событие",
    "start_date": "2024-05-15T10:00:00",
    "end_date": "2024-05-15T12:00:00",
    "venue": {
        "venue": "Место проведения",
        "address": "Адрес места проведения"
    }
}

# Добавляем новое событие
#create_event(new_event_data)

# Получаем данные о событиях
events_data = get_events()

# Отображаем список событий
if events_data:
    display_events(events_data)
