try:
    from app.crud.charity_project import CRUDCharityProject
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен класс `CRUDCharityProject`. '
        'Проверьте и поправьте: он должен быть доступен в модуле `app.crud.charity_project`.',
    )
from tests.ast import Ast
from conftest import APP_DIR
FILE = APP_DIR / 'crud' / 'charity_project.py'


def test_get_projects_by_completion_rate():
    assert hasattr(CRUDCharityProject, 'get_projects_by_completion_rate'), (
        'У объекта `app.crud.charity_project.CRUDCharityProject` не обнаружен метод `get_projects_by_completion_rate`'
    )
    ast = Ast(filename=FILE)
    async_func = ast.get_AsyncFunctionDef(name='get_projects_by_completion_rate')
    ast.visit_node(async_func)
    assert 'extract' in ast._names, (
        'Не обнаружен метод `extract` в вызовах в функции '
        '`CRUDCharityProject.get_projects_by_completion_rate`'
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
