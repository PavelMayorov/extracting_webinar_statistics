import requests
import pandas as pd

# search_keyword = input("Введите ключевое слово для поиска мепроприятий: ")
# search_date_from = input("Введите дату начала выборки в формате 'ГГГГ-ММ-ДД': ")
# search_date_to = input("Введите дату конца выборки в формате 'ГГГГ-ММ-ДД': ")
search_keyword = 'СТ-21-03/04'
search_date_from = '2022-03-01'
search_date_to = '2022-04-12'

headers = {
    'x-auth-token': 'af1e65517d8bc65a1deb5404048e011d',
    'Content-Type': 'application/x-www-form-urlencoded',
}


def get_id_all_events(date_from, date_to, keyword):
    url_events = f'https://userapi.webinar.ru/v3/organization/events/schedule?from={date_from}&to={date_to}' \
                 f'&perPage=100&page=1&status[0]=STOP&name={keyword}'
    events_response = requests.get(url_events, headers=headers).json()
    events_id = []
    for event in events_response:
        events_id.append(event['id'])
        print(event['name'])
    return events_id


def get_event_data(date_from, date_to, id):
    url_event = f'https://userapi.webinar.ru/v3/stats/users?from={date_from}&to={date_to}&eventId={id}'
    event_response = requests.get(url_event, headers=headers).json()
    data = []
    for pos, item in enumerate(event_response):
        data.append({})
        data[pos]['date'] = item['eventSessions'][0]['startsAt'][0:10]
        data[pos]['id'] = item['id']
        try:
            data[pos]['email'] = item['email']
        except KeyError:
            data[pos]['email'] = ''
        data[pos]['actual_presence'] = item['eventSessions'][0]['actualInvolvement']
    return data


def collection_data_all_events():
    events_id = get_id_all_events(search_date_from, search_date_to, search_keyword)
    events_data = []
    for event_id in events_id:
        event_data = get_event_data(search_date_from, search_date_to, event_id)
        events_data += event_data
    return events_data


if __name__ == "__main__":
    events_data = collection_data_all_events()
    df = pd.DataFrame(events_data)
    df.to_csv('statistic.csv')
