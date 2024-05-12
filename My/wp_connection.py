# Токен доступа
import base64

access_token = "vgGg e6XQ 5OBX IQq1 54Bp J7g8"
access_user = "k.prozorovskiy@yandex.ru"
wp_url = "https://mwtvoper.site"
# Кодируем имя пользователя и токен доступа в base64
credentials = f"{access_user}:{access_token}"
credentials_encoded = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {credentials_encoded}",
    "Content-Type": "application/json"
}
events_api_url = "https://mwtvoper.site/wp-json/tribe/events/v1/events"
users_api_url = f"{wp_url}/wp-json/wp/v2/users"