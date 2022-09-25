import asyncio

from src.controllers.users import users_crud
from src.controllers.addresses import address_crud
from src.controllers.products import products_crud
from src.controllers.carrinho import carrinho_crud

loop = asyncio.get_event_loop()
while True:
    loop.run_until_complete(users_crud())
    loop.run_until_complete(address_crud())
    loop.run_until_complete(products_crud())
    loop.run_until_complete(carrinho_crud())