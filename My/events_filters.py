from datetime import datetime

from My.events_class import get_events


def filter_events_for_today(events_data):
    # Получаем сегодняшнюю дату
    today = datetime.today().date()

    # Фильтруем события, оставляя только те, которые запланированы на сегодня
    today_events = [event for event in events_data['events'] if datetime.strptime(event['start_date'], '%Y-%m-%d %H:%M:%S').date() == today]

    return today_events

def display_events(today_events):
    # Вывод информации о каждом событии
    text_message = ""
    for event in today_events:
        text_message += f"Название: {event.get('title')}\n"
        text_message += f"Дата и время начала: {event.get('start_date')}\n"
        text_message += f"Дата и время окончания: {event.get('end_date')}\n"
        venue = event.get('venue')
        if venue:
            text_message += f"Место проведения: {venue.get('venue')}\n"
            text_message += f"Адрес: {venue.get('address')}\n"
        else:
            text_message += "Место проведения: Не указано\n"
        tags = event.get('tags', [])
        text_message += "Едут:\n"
        for tag in tags:
            text_message += f"@{tag.get('slug')}\n"
        text_message += "----------------------\n"

    return text_message

# Пример использования:
events_data = get_events()
today_events = filter_events_for_today(events_data)
text_message = display_events(today_events)





