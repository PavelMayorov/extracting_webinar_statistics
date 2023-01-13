import typing as tp

import requests

from settings import HEADERS, logger


def get_event_ids(date_from: str, date_to: str, keyword: str) -> tp.Optional[tp.List[str]]:
    url_events = f'https://userapi.webinar.ru/v3/organization/events/schedule?from={date_from}&to={date_to}' \
                 f'&perPage=100&page=1&status[0]=STOP&name={keyword}'
    try:
        events_response = requests.get(url_events, headers=HEADERS)
    except Exception as ex:
        logger.error(f'Нет соединения с сайтом Webinar! \n{ex}')
    else:
        if events_response.status_code == 200:
            if events_response.json():
                ids = []
                for event in events_response.json():
                    ids.append(event['id'])
                    logger.info(f'Найдено мероприятие: {event["name"]}.')
                return ids
            else:
                logger.info(f'Мероприятия с заданными параметрами не найдены.')
        else:
            logger.error('Не удалось получить данные о мероприятиях, проверьте вводимые данные!')


def get_event_data(date_from: str, date_to: str, event_id: str) -> tp.Optional[tp.List[dict]]:
    url_event = f'https://userapi.webinar.ru/v3/stats/users?from={date_from}&to={date_to}&eventId={event_id}'
    try:
        event_response = requests.get(url_event, headers=HEADERS).json()
    except Exception as ex:
        logger.error(f'Нет соединения с сайтом Webinar! \n{ex}')
    else:
        data = []
        for pos, item in enumerate(event_response):
            data.append({})
            data[pos]['date'] = item['eventSessions'][0]['startsAt'][0:10]
            data[pos]['id'] = item['id']
            data[pos]['name'] = item['name'] if item.get('name') else ''
            data[pos]['name'] += ' ' + item['secondName'] if item.get('secondName') else ''
            data[pos]['email'] = item['email'] if item.get('email') else ''
            data[pos]['actual_presence'] = item['eventSessions'][0]['actualInvolvement']
        return data


def collection_data_all_events(keyword: str, date_from: str, date_to: str) -> tp.Optional[tp.List[dict]]:
    event_ids = get_event_ids(date_from, date_to, keyword)
    if event_ids:
        data = []
        for event_id in event_ids:
            data += get_event_data(date_from, date_to, event_id)
        return data
