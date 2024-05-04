from datetime import datetime, timedelta
import pytz
import caldav
import logging

from My.cal_connection import url_yandex_cal, yandex_username, yandex_password_cal

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_event(calendar, title, start, end):
    try:
        event = caldav.Event()
        event_data = {
            "BEGIN": "VCALENDAR",
            "BEGIN": "VEVENT",
            "SUMMARY": title,
            "DESCRIPTION": "",
            "DTSTART;TZID=Europe/Moscow": start.strftime('%Y%m%dT%H%M%S'),
            "DTEND;TZID=Europe/Moscow": end.strftime('%Y%m%dT%H%M%S'),
            "END": "VEVENT",
            "END": "VCALENDAR"
        }
        event.data = "\n".join([f"{key}:{value}" for key, value in event_data.items()])
        calendar.add_event(event.data)
        logger.info(f"Создано событие: {title} с {start} по {end}")
        return True
    except Exception as e:
        logger.error(f"Ошибка создания события: {e}")
        return False

def create_events(event_title, start_date):
    try:
        # Подключаемся к календарю
        client = caldav.DAVClient(url=url_yandex_cal, username=yandex_username, password=yandex_password_cal)
        principal = client.principal()

        # Выбираем календарь
        calendars = principal.calendars()
        if not calendars:
            raise ValueError("No calendars found")
        calendar = calendars[0]

        # Определяем часовой пояс
        moscow_tz = pytz.timezone('Europe/Moscow')

        # Определяем диапазон дат (3 месяца вперед)
        end_date = start_date + timedelta(days=90)

        logger.info("Начало создания событий в календаре...")

        # Проходим по каждому дню в указанном диапазоне
        current_date = start_date
        while current_date < end_date:
            # Дежурство
            create_event(calendar, event_title + " дежурство", moscow_tz.localize(current_date.replace(hour=11)), moscow_tz.localize(current_date.replace(hour=23)))
            current_date += timedelta(days=1)
            # Дежурство
            create_event(calendar, event_title + " дежурство", moscow_tz.localize(current_date.replace(hour=11)), moscow_tz.localize(current_date.replace(hour=23)))
            current_date += timedelta(days=1)
            # Выезды/подхват
            create_event(calendar, event_title + " Выезды/подхват", moscow_tz.localize(current_date.replace(hour=11)), moscow_tz.localize(current_date.replace(hour=23)))
            current_date += timedelta(days=1)
            # Выезды/подхват
            create_event(calendar, event_title + " Выезды/подхват", moscow_tz.localize(current_date.replace(hour=11)), moscow_tz.localize(current_date.replace(hour=23)))
            current_date += timedelta(days=1)
            # Выходной
            create_event(calendar, event_title + " Выходной", moscow_tz.localize(current_date.replace(hour=11)), moscow_tz.localize(current_date.replace(hour=23)))
            current_date += timedelta(days=1)
            # Выходной
            create_event(calendar, event_title + " Выходной", moscow_tz.localize(current_date.replace(hour=11)), moscow_tz.localize(current_date.replace(hour=23)))
            current_date += timedelta(days=1)

        logger.info("Создание событий завершено.")
        return True
    except ValueError as e:
        logger.error(f"Ошибка создания событий: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка при создании событий: {e}")
        return False

if __name__ == "__main__":
    # Создание событий
    start_date = datetime(2024, 4, 28)  # Здесь укажите нужную дату начала
    event_title = "Аня"
    create_events(event_title, start_date)
