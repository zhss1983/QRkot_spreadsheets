import pytest
try:
    from app.api.endpoints import google_api
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен файл `google_api`. '
        'Проверьте и поправьте: он должен быть доступке в модуле `app.api.endendpoints`.',
    )


from tests.ast import Ast
from conftest import APP_DIR
FILE = APP_DIR / 'api' / 'endpoints' / 'google_api.py'


@pytest.fixture
def file_ast():
    ast = Ast(filename=FILE)
    return ast


def test_get_report(file_ast):
    assert hasattr(google_api, 'get_report'), (
        'В файле `app.api.endpoints.google_api` не обнаружена функция `get_report`'
    )
    async_func = file_ast.get_AsyncFunctionDef(name='get_report')
    file_ast.visit_node(async_func)
    assert 'list' in file_ast._names, (
        'Endpoint `get_report` должен возвращать список'
    )
