from datetime import datetime, timedelta
import pytz
import caldav
import logging
import ics  # Добавлен импорт модуля ics
import asyncio


# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к серверу CalDAV
url_yandex_cal = "https://caldav.yandex.ru/calendars/k.prozorovskiy%40yandex.ru/events-28804337/"
yandex_username = "k.prozorovskiy@yandex.ru"
yandex_password_cal = "jalpurxduzsdohim"

async def get_events():
    try:
        # Подключение к серверу CalDAV
        client = caldav.DAVClient(url_yandex_cal, username=yandex_username, password=yandex_password_cal)

        # Получение всех доступных календарей
        principal = client.principal()
        calendars = principal.calendars()
        print(calendars)

        # Выбор первого календаря из списка
        calendar = calendars[0]  # Выберите нужный календарь или уточните логику

        # Определение временных интервалов для поиска событий до конца следующего дня
        now = datetime.now(pytz.timezone('Europe/Moscow'))
        tomorrow_end = now.replace(hour=23, minute=59, second=59, microsecond=999) + timedelta(days=1)

        # Отправка запроса для получения событий в указанном временном интервале
        results = calendar.date_search(now, tomorrow_end)

        # Обработка результатов
        events = []
        for event in results:
            events.append(event.data)
            print(events)

        return events

    except Exception as e:
        logger.error(f"Ошибка при получении событий: {e}")
        raise

async def parse_events(calendar_data):
    try:
        events = []
        for data in calendar_data:
            cal = ics.Calendar(data)
            events.extend(cal.events)
        return events
    except Exception as e:
        logger.error(f"Error parsing events: {e}")
        raise

async def show_free_events(update, context):
    try:
        calendar_data = await get_events()
        if calendar_data:
            events = await parse_events(calendar_data)
            if events:
                message_text = '<b>Ближайшие свободные события</b>\n\n'
                sorted_events = sorted(events, key=lambda event: event.begin)
                for event in sorted_events:
                    formatted_start = event.begin.strftime('%Y-%m-%d %H:%M:%S')
                    message_text += f'<u><b>{formatted_start}</b> - </u>'
                    if event.name:
                        message_text += f'<u><b>{event.name}</b></u>\n'
                    if event.description:
                        message_text += f'{event.description}\n'
                return message_text, events
        return "На сегодня и завтра нет свободных событий."
    except Exception as e:
        logger.error(f"Error showing free events: {e}")
        raise

async def main():
    try:
        result = await show_free_events(123, 321)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
