import requests
import pandas as pd

from settings import HEADERS, DEFAULT_CSV_FILENAME, logger


def user_input():
    keyword = input('Введите ключевое слово для поиска мепроприятий: ')
    date_from = input('Введите дату начала выборки в формате "ГГГГ-ММ-ДД": ')
    date_to = input('Введите дату конца выборки в формате "ГГГГ-ММ-ДД": ')
    return keyword, date_from, date_to


def get_event_ids(date_from, date_to, keyword):
    url_events = f'https://userapi.webinar.ru/v3/organization/events/schedule?from={date_from}&to={date_to}' \
                 f'&perPage=100&page=1&status[0]=STOP&name={keyword}'
    try:
        events_response = requests.get(url_events, headers=HEADERS)
    except Exception as ex:
        logger.error('Нет соединения с сайтом Webinar!')
        logger.error(ex)
    else:
        if events_response.status_code == 200:
            if events_response.json():
                ids = []
                for event in events_response.json():
                    ids.append(event['id'])
                    logger.info(f'Найдено мероприятие {event["name"]}.')
                return ids
            else:
                logger.info(f'Мероприятия с заданными параметрами не найдены.')
        else:
            logger.error('Не удалось получить данные о мероприятиях, проверьте вводимые данные!')


def get_event_data(date_from, date_to, event_id):
    url_event = f'https://userapi.webinar.ru/v3/stats/users?from={date_from}&to={date_to}&eventId={event_id}'
    try:
        event_response = requests.get(url_event, headers=HEADERS).json()
    except Exception as ex:
        logger.error('Нет соединения с сайтом Webinar!')
        logger.error(ex)
    else:
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


def collection_data_all_events(keyword, date_from, date_to):
    event_ids = get_event_ids(date_from, date_to, keyword)
    if event_ids:
        data = []
        for event_id in event_ids:
            data += get_event_data(date_from, date_to, event_id)
        return data


def write_to_csv_file(data, file_name=DEFAULT_CSV_FILENAME):
    df = pd.DataFrame(data)
    df.to_csv(file_name)
    logger.info(f'Данные о мероприятиях успешно сохранены в файл {file_name}.')


def main():
    search_keyword, search_date_from, search_date_to = user_input()
    events_data = collection_data_all_events(search_keyword, search_date_from, search_date_to)
    if events_data:
        write_to_csv_file(events_data)


if __name__ == '__main__':
    main()
