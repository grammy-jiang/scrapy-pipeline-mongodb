from scrapy.settings import Settings

from ..settings.default_settings import MONGODB_DATABASE
from ..settings.default_settings import MONGODB_HOST
from ..settings.default_settings import MONGODB_OPTIONS_
from ..settings.default_settings import MONGODB_PASSWORD
from ..settings.default_settings import MONGODB_PORT
from ..settings.default_settings import MONGODB_USERNAME


def get_mongodb_uri(settings: Settings) -> str:
    return 'mongodb://{account}{path}{options}'.format(
        account=_gen_mongo_account(settings),
        path=_gen_mongo_path(settings),
        options=_gen_mongo_option(settings))


def _gen_mongo_account(settings: Settings) -> str:
    return {
        True: '{username}:{password}@'.format(
            username=settings[MONGODB_USERNAME],
            password=settings[MONGODB_PASSWORD]),
        False: ''
    }.get(all(map(settings.get, [MONGODB_USERNAME, MONGODB_PASSWORD])))


def _gen_mongo_path(settings: Settings) -> str:
    return '{host}:{port}/{database}'.format(
        host=settings.get(MONGODB_HOST, 'localhost'),
        port=settings.get(MONGODB_PORT, 27017),
        database=settings.setdefault(MONGODB_DATABASE, ''))


def _gen_mongo_option(settings: Settings) -> str:
    options = list(filter(
        lambda x: all([x[0].startswith(MONGODB_OPTIONS_),
                       x[0].replace(MONGODB_OPTIONS_, '')]),
        settings.items()
    ))
    if options:
        return '?{options}'.format(
            options='&'.join(map(
                lambda x: '{option}={value}'.format(
                    option=x[0].replace(MONGODB_OPTIONS_, '').lower(),
                    value=x[1]),
                options)))
    else:
        return ''
