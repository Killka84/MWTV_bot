import caldav
import logging
from My.cal_connection import url_yandex_cal, yandex_username, yandex_password_cal
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def delete_all_events():
    try:
        # Подключаемся к календарю
        client = caldav.DAVClient(url=url_yandex_cal, username=yandex_username, password=yandex_password_cal)
        principal = client.principal()

        # Выбираем календарь
        calendars = principal.calendars()
        if not calendars:
            raise ValueError("No calendars found")
        calendar = calendars[0]

        logger.info("Начало удаления всех событий в календаре...")

        # Получаем все события в календаре
        events = calendar.events()

        # Удаляем все события
        for event in events:
            event.delete()
            logger.info("Событие успешно удалено")

        logger.info("Удаление всех событий завершено.")
        return True
    except ValueError as e:
        logger.error(f"Ошибка удаления событий: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка при удалении событий: {e}")
        return False