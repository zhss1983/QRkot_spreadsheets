try:
    from app.crud.charity_project import CRUDMeetingRoom
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен класс `CRUDMeetingRoom`. '
        'Проверьте и поправьте: он должен быть доступен в модуле `app.crud.charity_project`.',
    )
from tests.ast import Ast
from conftest import APP_DIR
FILE = APP_DIR / 'crud' / 'charity_project.py'


def test_get_projects_by_completion_rate():
    assert hasattr(CRUDMeetingRoom, 'get_projects_by_completion_rate'), (
        'У объекта `app.crud.charity_project.CRUDMeetingRoom` не обнаружен метод `get_projects_by_completion_rate`'
    )
    ast = Ast(filename=FILE)
    async_func = ast.get_AsyncFunctionDef(name='get_projects_by_completion_rate')
    ast.visit_node(async_func)
    assert 'extract' in ast._names, (
        'Не обнаружен метод `extract` в вызовах в функции '
        '`CRUDMeetingRoom.get_projects_by_completion_rate`'
    )
    assert 'year' in ast._constants, (
        'В методе `extract` используйте `year`'
    )
    assert 'month' in ast._constants, (
        'В методе `extract` используйте `month`'
    )
    assert 'day' in ast._constants, (
        'В методе `extract` используйте `day`'
    )
