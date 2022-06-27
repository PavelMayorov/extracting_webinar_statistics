import openpyxl

from extract_statistic_to_csv import collection_data_all_events, user_input
from settings import RED, GREEN, CENTER, logger


def input_file_name():
    while True:
        file_name = input('Введите имя файла, содержащего список студентов (этот файл должен находиться в одной '
                          'директории с запускаемой программой и иметь расширение ".xlsx") (Пример: имя_файла.xlsx): ')
        if file_name[-5:] != '.xlsx':
            logger.error('Неверное расширение файла!')
        else:
            return file_name


def cell_entry(sheet, row, column, value, fill, alignment=CENTER):
    cell = sheet.cell(row=row, column=column)
    cell.value = value
    cell.fill = fill
    cell.alignment = alignment


def write_to_csv_file(file_name, events_data):
    try:
        students_list = openpyxl.load_workbook(filename=file_name)
    except Exception as ex:
        logger.error('Не удалось открыть файл! Проверьте имя файла и его расположение!')
        logger.error(ex)
    else:
        sheet = students_list['Лист1']
        row = 1
        column = 4
        for event_data in events_data:
            date = event_data['date']
            if sheet.cell(row=row, column=column).value != date:
                column += 1
                sheet.cell(row=row, column=column).value = date
                sheet.column_dimensions[chr(64+column)].width = 10
            i = 2
            while (sheet.cell(row=row+i, column=4).value or sheet.cell(row=row+i+1, column=4).value or
                   sheet.cell(row=row+i+2, column=4).value):
                if not sheet.cell(row=row+i, column=column).value and sheet.cell(row=row+i, column=4).value:
                    cell_entry(sheet, row+i, column, 'н', RED)
                if event_data['email'].lower() == str(sheet.cell(row=row+i, column=4).value).lower().strip():
                    if event_data['actual_presence'] == '100,00%' or event_data['actual_presence'] >= '60,00%':
                        cell_entry(sheet, row+i, column, '+', GREEN)
                    else:
                        cell_entry(sheet, row+i, column, '-', RED)
                i += 1
        students_list.save(file_name)
        logger.info(f'Данные о мероприятиях успешно сохранены в файл {file_name}.')


def main():
    search_keyword, search_date_from, search_date_to = user_input()
    events_data = collection_data_all_events(search_keyword, search_date_from, search_date_to)
    if events_data:
        file_name = input_file_name()
        write_to_csv_file(file_name, events_data)


if __name__ == '__main__':
    main()
