import typing as tp

from settings import logger


def input_events_info() -> tp.Tuple[str, str, str]:
    keyword = input('Введите ключевое слово для поиска мепроприятий: ')
    date_from = input('Введите дату начала выборки в формате "ГГГГ-ММ-ДД": ')
    date_to = input('Введите дату конца выборки в формате "ГГГГ-ММ-ДД": ')
    return keyword, date_from, date_to


def input_file_name() -> str:
    while True:
        file_name = input('Если у Вас есть файл, содержащий список посетителей мероприятия, то укажите его имя, \n'
                          'если нет, оставьте это поле пустым. Ваш файл должен быть отформатирован как Пример.xlsx, \n'
                          'иметь расширение ".xlsx" и располагаться в одной папке с запускаемой программой. \n'
                          'Имя файла: ')
        if not file_name:
            break
        else:
            if file_name[-5:] != '.xlsx':
                logger.warning('Неверное расширение файла!')
            else:
                return file_name
