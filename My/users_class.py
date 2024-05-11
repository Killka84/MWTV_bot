import requests
from My.wp_connection import wp_url, access_user, access_token


def get_wordpress_users(wp_url, username, password):
    api_url = f"{wp_url}/wp-json/wp/v2/users"
    response = requests.get(api_url, auth=(username, password))
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error {response.status_code}: Failed to retrieve the list of users.")
        return None

def get_user_data(username):
    try:
        users = get_wordpress_users(wp_url, access_user, access_token)
        for user in users:
            print(users)
            if user['slug'].lower() == username.lower():
                return user
        print(f"User with username '{username}' not found.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return None


# username = "prozorovskiy_kirill"
# user_data = get_user_data(username)

def format_user_data(user_data, username):
    if user_data:
        id = user_data['id']
        name = user_data['name']
        slug = user_data['slug']

        formatted_user_data = (
            f"Имя: {name}\n"
            f"Telegram: <a href=\"https://t.me/{slug}\">@{slug}</a></li> \n"
        )

        return formatted_user_data
    else:
        return f"Пользователь с логином '{username}' не найден."
