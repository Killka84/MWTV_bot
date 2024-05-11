def api_data_event(title, location, start_date, end_date, description='', excerpt='', website='', cat_name, street, show_map=True, show_map_link=True, hide_from_listings=False, sticky=True, featured=True):
    new_event_data ={
        'title': title,
        'description': description,
        'excerpt': excerpt,
        'start_date': start_date,
        'start_date_details': {
            'year': start_date.split('-')[0],
            'month': start_date.split('-')[1],
            'day': start_date.split('-')[2].split()[0],
            'hour': start_date.split()[1].split(':')[0],
            'minutes': start_date.split()[1].split(':')[1],
            'seconds': start_date.split()[1].split(':')[2]
        },
        'end_date': end_date,
        'end_date_details': {
            'year': end_date.split('-')[0],
            'month': end_date.split('-')[1],
            'day': end_date.split('-')[2].split()[0],
            'hour': end_date.split()[1].split(':')[0],
            'minutes': end_date.split()[1].split(':')[1],
            'seconds': end_date.split()[1].split(':')[2]
        },
        'timezone': 'UTC+3',
        'timezone_abbr': 'UTC+3',
        'website': website,
        'show_map': show_map,
        'show_map_link': show_map_link,
        'hide_from_listings': hide_from_listings,
        'sticky': sticky,
        'featured': featured,
        'categories': [{
            'name': cat_name,
        }],
        'tags': [],
        'venue': {
            'venue': location,
            'address': street,
            'city': 'Москва',
            'country': 'Российская Федерация',
            'province': 'Москва',
            'stateprovince': 'Москва',
            'show_map': True,
            'show_map_link': True,
        },
        'organizer': []
    }
    return new_event_data
