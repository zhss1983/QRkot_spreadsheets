from datetime import datetime
from typing import Generic, Sequence, TypeVar, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject, Donation

CharityProject = TypeVar('CharityProject', bound=CharityProject)
Donation = TypeVar('Donation', bound=Donation)


def check_close(obj: Generic[Donation, CharityProject]) -> bool:
    """Проверяю надо или нет закрыть запись"""
    return obj.full_amount <= obj.invested_amount


def object_close(
        obj: Generic[Donation, CharityProject],
        transfer_time
) -> Generic[Donation, CharityProject]:
    """Меняю статус записи с открытой на закрытую"""
    obj.fully_invested = True
    obj.close_date = transfer_time
    return obj


def change_invested_amount(
    charity_project: CharityProject,
    donation: Donation,
    delta: int
) -> Tuple[CharityProject, Donation]:
    """Изменяю параметр отвечающий за уровень инвестиций"""
    charity_project.invested_amount += delta
    donation.invested_amount += delta
    return charity_project, donation


def delta(delta_item: Generic[Donation, CharityProject]) -> int:
    """расчитываю доступный уровень для инвестиций"""
    return delta_item.full_amount - delta_item.invested_amount


def multi_check_close(
        obj: Generic[Donation, CharityProject]
) -> Generic[Donation, CharityProject]:
    """Проверяю записи на остаток суммы и возвращаю только закртые"""
    for item in obj:
        if check_close(item):
            object_close(item, obj)
            yield item


def transfer(
        obj_1: Generic[Donation, CharityProject],
        obj_1_index: int,
        obj_1_count: int,
        obj_1_delta: int,
        obj_2: Generic[Donation, CharityProject],
        obj_2_index: int,
        transfer_time: datetime
):
    add_updates = []
    obj_1, obj_2 = change_invested_amount(obj_1, obj_2, obj_1_delta)
    obj_1 = object_close(obj_1, transfer_time)
    add_updates.append(obj_1)
    if check_close(obj_2):
        object_close(obj_2, transfer_time)
        add_updates.append(obj_2)
        obj_2_index += 1
    obj_1_index += 1
    if obj_1_index >= obj_1_count:
        add_updates.append(obj_2)
        return add_updates, False, obj_1_index, obj_2_index
    return add_updates, True, obj_1_index, obj_2_index


def money_transfer(
    donations: Sequence[Donation],
    charity_projects: Sequence[CharityProject]
):
    """Переписываю деньги из донатов в проекты и возвращаю каждый изменённый"""
    result = []
    donation_index, donations_count = 0, len(donations)
    charity_index, charity_projects_count = 0, len(charity_projects)
    transfer_time = datetime.utcnow()
    if donations_count == 0:
        return [*multi_check_close(charity_projects)]
    elif charity_projects_count == 0:
        return [*multi_check_close(donations)]
    interrupt = True
    while interrupt:
        donation = donations[donation_index]
        charity_project = charity_projects[charity_index]
        charity_project_delta = delta(charity_project)
        donation_delta = delta(donation)
        if donation_delta <= charity_project_delta:
            add_updates, interrupt, donation_index, charity_index = transfer(
                donation, donation_index, donations_count, donation_delta,
                charity_project, charity_index, transfer_time)
        else:
            add_updates, interrupt, charity_index, donation_index = transfer(
                charity_project, charity_index, charity_projects_count,
                charity_project_delta, donation, donation_index, transfer_time)
        result += add_updates
    return result


async def invested_amount(
    session: AsyncSession,
) -> None:
    """Расчёт итога по приходу доната или проекта для финансирования."""
    donations = await donation_crud.get_active(session)
    donations = donations.all()
    charity_projects = await charity_project_crud.get_active(session)
    charity_projects = charity_projects.all()
    updates = money_transfer(donations, charity_projects)
    await donation_crud.update_multi(updates, session)
