from datetime import datetime, timedelta
import pytz
import caldav
import logging
import ics
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
        logger.error(f"Ошибка при парсинге событий: {e}")
        raise

async def show_free_events():
    try:
        current_time = datetime.now(pytz.timezone('Europe/Moscow'))
        today = current_time.date()
        calendar_data = await get_events()
        if calendar_data:
            events = await parse_events(calendar_data)
            if events:
                message_text = '<b>Опера на сегодня</b>\n\n'
                sorted_events = sorted(events, key=lambda event: event.begin)
                for event in sorted_events:
                    if event.begin.date() == today:  # Фильтрация событий на сегодня
                        formatted_start = event.begin.strftime('%Y-%m-%d %H:%M:%S')
                        message_text += f'<u><b>{formatted_start}</b> - </u>'
                        if event.name:
                            message_text += f'<u><b>{event.name}</b></u>\n'
                        if event.description:
                            message_text += f'{event.description}\n'
                            print(message_text)
                return message_text
        return "На сегодня нет свободных событий."
    except Exception as e:
        logger.error(f"Ошибка при выводе свободных событий: {e}")
        raise

# async def main():
#     print('Начали')
#     try:
#         result = await show_free_events()
#         print(result)
#     except Exception as e:
#         print(f"Ошибка в main: {e}")
#
# # Добавим отладочный вывод, чтобы увидеть, что происходит при запуске asyncio.run()
# print("Перед запуском main()")
# asyncio.run(main())
# print("После запуска main()")
