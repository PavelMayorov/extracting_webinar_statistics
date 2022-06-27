import logging
from openpyxl.styles import PatternFill, Alignment


# Создание нового логгера и установка уровня логирования 'error' другим логгерам
logging.basicConfig(level='DEBUG')
logger = logging.getLogger()
logging.getLogger('urllib3').setLevel('ERROR')

# Настройки ячеек excel
RED = PatternFill(start_color="FF1E3A", end_color="FF1E3A", fill_type="solid")
GREEN = PatternFill(start_color="7CFC00", end_color="7CFC00", fill_type="solid")
CENTER = Alignment(horizontal='center')

# Заголовки для обращения к API Webinar
HEADERS = {
    'x-auth-token': 'af1e65517d8bc65a1deb5404048e011d',
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Имя csv файла по умолчанию
DEFAULT_CSV_FILENAME = 'statistic.csv'
