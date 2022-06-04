import pytest
try:
    from app.services import google_api
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен файл `google_api`. '
        'Проверьте и поправьте: он должен быть доступке в модуле `app.services`.',
    )


from tests.ast import Ast
from conftest import APP_DIR
FILE = APP_DIR / 'services' / 'google_api.py'


@pytest.fixture
def file_ast():
    ast = Ast(filename=FILE)
    return ast


def test_set_user_permissions(file_ast):
    assert hasattr(google_api, 'set_user_permissions'), (
        'В файле `app.services.google_api` не обнаружена функция `set_user_permissions`'
    )
    async_func = file_ast.get_AsyncFunctionDef(name='set_user_permissions')
    file_ast.visit_node(async_func)
    assert 'discover' in file_ast._attrs, (
        'Используйте метод `discover` в функции `set_user_permissions`'
    )
    assert 'drive' in file_ast._constants, (
        'Укажите атрибут `drive` в методе `discover` в функции `set_user_permissions`'
    )
    assert 'v3' in file_ast._constants, (
        'Укажите атрибут `v3` в методе `discover` в функции `set_user_permissions`'
    )


def test_spreadsheets_create(file_ast):
    assert hasattr(google_api, 'spreadsheets_create'), (
        'В файле `app.services.google_api` не обнаружена функция `spreadsheets_create`'
    )
    async_func = file_ast.get_AsyncFunctionDef(name='spreadsheets_create')
    file_ast.visit_node(async_func)
    assert 'discover' in file_ast._attrs, (
        'Используйте метод `discover` в функции `spreadsheets_create`'
    )
    assert 'sheets' in file_ast._constants, (
        'Укажите атрибут `drive` в методе `discover` в функции `spreadsheets_create`'
    )
    assert 'v4' in file_ast._constants, (
        'Укажите атрибут `v4` в методе `discover` в функции `spreadsheets_create`'
    )
    assert 'Отчет на ' in file_ast._constants, (
        'Название таблицы должно быть `Отчет на <дата и время>`'
    )
    assert 'json' in file_ast._call_args, (
        'Аргументом метода `create` укажите `json`'
    )
    assert 'spreadsheetId' in file_ast._constants, (
        'Функция `spreadsheets_create` должна возвращать значение ключа `spreadsheetId`'
    )


def test_spreadsheets_update_value(file_ast):
    assert hasattr(google_api, 'spreadsheets_update_value'), (
        'В файле `app.services.google_api` не обнаружена функция `spreadsheets_update_value`'
    )
    async_func = file_ast.get_AsyncFunctionDef(name='spreadsheets_update_value')
    file_ast.visit_node(async_func)
    assert 'Отчет от' in file_ast._constants, (
        'Значение таблицы должно быть `Отчет от <дата и время>`'
    )
    assert 'Топ проектов по скорости закрытия' in file_ast._constants, (
        'Значение таблицы должно быть `Топ проектов по скорости закрытия`'
    )
    assert 'Название проекта' in file_ast._constants, (
        'Значение таблицы должно быть `Название проекта`'
    )
    assert 'Время сбора' in file_ast._constants, (
        'Значение таблицы должно быть `Время сбора`'
    )
    assert 'Описание' in file_ast._constants, (
        'Значение таблицы должно быть `Описание`'
    )
    assert 'update' in file_ast._attrs, (
        'Используйте метод `update` в функции `spreadsheets_update_value`'
    )
    assert 'valueInputOption' in file_ast._call_args, (
        'Укажите ключевой аргумент `valueInputOption` в методе `update`'
    )
    assert 'USER_ENTERED' in file_ast._constants, (
        'Значение аргумента `valueInputOption` `USER_ENTERED`'
    )

    assert 'json' in file_ast._call_args, (
        'Укажите ключевой аргумент `json` в методе `update`'
    )
