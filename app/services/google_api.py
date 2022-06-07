from datetime import datetime
from pydantic import EmailStr

from aiogoogle import Aiogoogle
# В секретах лежит адрес вашего личного google-аккаунта
from app.core.config import settings


# Константа с форматом строкового представления времени
FORMAT = "%Y/%m/%d %h:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создаёт гугл-таблицы с отчётом на google-диске сервисного аккаунта"""
    # print('--------------------=======================----------------------')
    # print('async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:')
    # report
    # Получаем текущую дату для заголовка документа
    # print('--------------------=======================----------------------')
    # print('now_date_time = datetime.now().strftime(FORMAT)')
    now_date_time = datetime.now().strftime(FORMAT)
    # Создаём экземпляр класса Resourse
    # print('--------------------=======================----------------------')
    # print('service = await wrapper_services.discover(\'sheets\', \'v4\')')
    service = await wrapper_services.discover('sheets', 'v4')
    # Формируем тело запроса
    # print('--------------------=======================----------------------')
    # print('spreadsheet_body = {')
    spreadsheet_body = {
        'properties': {'title': f'QRKot report on {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
    # Выполняем запрос
    # print('--------------------=======================----------------------')
    # print('response = await wrapper_services.as_service_account('\
    #     'service.spreadsheets.create(json=spreadsheet_body)')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    # print('--------------------=======================----------------------')
    # print('response[\'spreadsheetId\']')
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle,
        email: EmailStr = settings.email
) -> None:
    """Выдаёт права google-аккаунту на созданные документы"""
    # print('--------------------=======================----------------------')
    # print('async def set_user_permissions(')
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


# Новая функция
async def spreadsheets_update_value(
        spreadsheetid: str,
        reservations: list,
        wrapper_services: Aiogoogle
) -> None:
    """Обновляет данные в гугл-таблице"""
    # print('--------------------=======================----------------------')
    # print('async def spreadsheets_update_value(')
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    # Здесь формируется тело таблицы
    table_values = [
        ['Отчет от', now_date_time],
        ['Сроки инвестирования проектов'],
        ['Название проекта', 'Срок инвестирования', 'Описание проекта']
    ]
    # Здесь в таблицу добавляются строчки
    for res in reservations:
        new_row = [
            str(res['name']),
            str(res['close_date'] - res['create_date']),
            str(res['description'])
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


