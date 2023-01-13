from extracting_statistics import collection_data_all_events
from user_inputs import input_file_name, input_events_info
from creating_presence_table import write_users_info, write_statistics


def main():
    search_keyword, search_date_from, search_date_to = input_events_info()
    events_data = collection_data_all_events(search_keyword, search_date_from, search_date_to)
    if events_data:
        file_name = input_file_name()
        if not file_name:
            file_name = 'Статистика.xlsx'
            write_users_info(events_data, file_name)
        write_statistics(events_data, file_name)


if __name__ == '__main__':
    main()
