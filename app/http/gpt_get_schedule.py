from aiohttp.web_request import Request
from babel.dates import format_date

# TODO move somewhere elso
from app.routes.commanders_chat import get_battles
from app.utils.time import get_nearest_day


async def http_get_schedule(_: Request):
    day = get_nearest_day()
    battles = await get_battles(day)
    schedule = []

    for battle in battles:
        if battle.for_user is not None:
            user = battle.for_user.name
        else:
            user = 'никто'
        schedule.append(f'в {battle.hour}:00 - {user}')
    schedule_text = '\n'.join(schedule)
    date_string = format_date(day, 'full', locale='ru_RU')
    return f'Расписание на {date_string}\n{schedule_text}'
