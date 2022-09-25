from src.models.product import (
    create_product,
    get_product_by_code,
    delete_product
)
from src.server.database import connect_db, db, disconnect_db


async def products_crud():
    option = input("Entre com a opção de CRUD para produtos: ")
    
    await connect_db()
    product_collection = db.product_collection

    product = {
        "name": "Playstation 5",
        "description": "Videogame caro e legal",
        "price": 5000.00,
        "image": "https://m.media-amazon.com/images/S/aplus-media-library-service-media/2c0fa2e1-ec30-4ff2-95fb-92230e028788.__CR0,0,970,600_PT0_SX970_V1___.jpg",
        "code": 1 
    }
    
    if option == '1':
        # create product
       
        product = await create_product(
            product_collection,
            product
        )
        print(product)
    elif option == '2':
        # get product
        product = await get_product_by_code(
            product_collection,
            product["code"]
        )
        print(product)
    
    elif option == '3':
        # delete product
        product = await get_product_by_code(
            product_collection,
            product["code"]
        )

        result = await delete_product(
            product_collection,
            product["_id"]
        )

        print(result)

    await disconnect_db()
