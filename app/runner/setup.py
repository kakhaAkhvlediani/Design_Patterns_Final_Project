from fastapi import FastAPI

from app.core.facade import BitcoinWalletCore
from app.infra.api.statistics_api import statistics_api
from app.infra.api.transactions_api import transactions_api
from app.infra.api.users_api import users_api
from app.infra.api.wallets_api import wallets_api
from app.infra.SQLlite.api_keys_repository import SQLAPIKeysRepository
from app.infra.SQLlite.transactions_repository import SQLTransactionsRepository
from app.infra.SQLlite.users_repository import SQLUsersRepository
from app.infra.SQLlite.wallets_repository import SQLWalletsRepository
from app.infra.utils.currency_converter import CoindeskCurrencyConverter
from app.infra.utils.fee_strategy import FeeRateStrategy
from app.infra.utils.hasher import DefaultHashFunction


def setup() -> FastAPI:
    app = FastAPI()

    app.include_router(users_api)
    app.include_router(wallets_api)
    app.include_router(transactions_api)
    app.include_router(statistics_api)

    user_repository: SQLUsersRepository = SQLUsersRepository()
    wallets_repository: SQLWalletsRepository = SQLWalletsRepository()
    transactions_repository: SQLTransactionsRepository = SQLTransactionsRepository()
    api_keys_repository: SQLAPIKeysRepository = SQLAPIKeysRepository()

    app.state.core = BitcoinWalletCore.create(
        users_repository=user_repository,
        wallets_repository=wallets_repository,
        transactions_repository=transactions_repository,
        api_key_repository=api_keys_repository,
        hash_function=DefaultHashFunction(),
        currency_converter=CoindeskCurrencyConverter(),
        fee_strategy=FeeRateStrategy(),
    )

    return app
