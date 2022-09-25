from src.models.address import (
    create_address,
    get_address_by_street,
    delete_address  
)

from src.models.user import (get_user_by_email)

from src.server.database import connect_db, db, disconnect_db

async def address_crud():
    option = input("Entre com a opção de CRUD para o endereço: ")
    
    await connect_db()
    address_collection = db.address_collection
    users_collection = db.users_collection

    user = await get_user_by_email(users_collection, "lu_domagalu@gmail.com")

    address =  {
        "street": "Rua cocada, 50",
        "cep": "55999000",
        "district": "Centro",
        "city": "Azul",
        "state": "Pernambuco",
        "is_delivery": True 
    }
    

    user_address = {
        "user": user,
        "address": [address]
    }

    if option == '1':
        # create address

        address = await create_address(
            users_collection,
            address_collection,
            user_address
            
        )
        print(user_address)
    elif option == '2':
        # get address
        address = await get_address_by_street(
            address_collection,
            address["street"]
        )
        print(address)
    elif option == '3':
        # delete address
        address = await get_address_by_street(
            address_collection,
            address["street"]
        )

        result = await delete_address(
            address_collection,
            address["_id"]
        )

        print(result)

    await disconnect_db()
