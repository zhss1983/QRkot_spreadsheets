from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle
from pydantic import EmailStr

from app.core.config import settings
from app.schemas import CharityProjectDB

FORMAT = "%Y/%m/%d %h:%M:%S"


async def spreadsheets_create(
    wrapper_services: Aiogoogle, rows: int = 100, cols: int = 10
) -> str:
    """Создаёт гугл-таблицы с отчётом на google-диске сервисного аккаунта"""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheet_body = {
        "properties": {"title": f"Отчет от {now_date_time}", "locale": "ru_RU"},
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridProperties": {"rowCount": rows, "columnCount": cols},
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response["spreadsheetId"]


async def set_user_permissions(
    spreadsheetid: str, wrapper_services: Aiogoogle, email: EmailStr = settings.email
) -> None:
    """Выдаёт права google-аккаунту на созданные документы"""
    permissions_body = {"type": "user", "role": "writer", "emailAddress": email}
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str,
    reservations: List[CharityProjectDB],
    wrapper_services: Aiogoogle,
) -> None:
    """Обновляет данные в гугл-таблице"""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    table_values = [
        [f"Отчет от {now_date_time}"],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]
    for res in reservations:
        table_values.append(
            [res.name, str(res.close_date - res.create_date), res.description]
        )
    update_body = {
        "majorDimension": "ROWS",
        "values": table_values,
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f"A1:C{len(table_values)}",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
