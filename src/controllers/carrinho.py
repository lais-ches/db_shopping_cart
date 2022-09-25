from src.models.order import (
   create_cart,
   get_cart_by_user_email,
   update_cart,
   delete_cart
)

from src.models.order_item import (
    add_product_to_order,
    delete_product_from_order,
    get_order_item_by_order_id_and_product_id
)

from src.models.user import (get_user_by_email)
from src.models.product import (get_product_by_code)
from src.models.address import (get_address_by_street)

from src.server.database import connect_db, db, disconnect_db


async def carrinho_crud():
    option = input("Entre com a opção de CRUD do carrinho: ")
    
    await connect_db()
    order_collection = db.order_collection
    order_items_collection = db.order_items_collection
    address_collection = db.address_collection
    product_collection = db.product_collection
    users_collection = db.users_collection

    user = await get_user_by_email(users_collection, "lu_domagalu@gmail.com")
    product = await get_product_by_code(product_collection, 1)
    address = await get_address_by_street(address_collection, "Rua cocada, 50")
   
    order = {
        "user": user,
        "price": 0,
        "paid": False,
        "address": address
    }

    order_item = {
        "order": order,
        "product": product
    }

    if option == '1':
        # create cart
       
        cart = await create_cart(
            order_collection,
            order
        )
        print(cart)
    elif option == '2':
        # get cart
        cart = await get_cart_by_user_email(
            order_collection,
            users_collection,
            user["email"]
        )
        print(cart)
    elif option == '3':
        # update cart // add products
        cart = await get_cart_by_user_email(
            order_collection,
            users_collection,
            user["email"]
        )

        new_order_item = {
            "order": order,
            "product": product
        }
        print(new_order_item)

        new_order_item = await add_product_to_order(
            order_items_collection, 
            new_order_item
        )

        cart_data = {
            "price": cart["price"] + new_order_item["product"]["price"]
        }

        is_updated, numbers_updated = await update_cart(
            order_collection,
            cart["_id"],
            cart_data
        )
        if is_updated:
            print(f"Carrinho de compras atualizado com sucesso, número de documentos alterados {numbers_updated}")
        else:
            print("A ataulização do carrinho de compras falhou!")
    elif option == '4':
        # delete product from cart
        cart = await get_cart_by_user_email(
            order_collection,
            users_collection,
            user["email"]
        )
        
        product = await get_product_by_code(
            product_collection,
            1
        )
        
        order_item = await get_order_item_by_order_id_and_product_id(
            order_items_collection, 
            cart["user"]["_id"],
            product["code"]
        )
        
        result = await delete_product_from_order(
            order_items_collection,
            order_item["_id"]
        )

        cart_data = {
            "price": cart["price"] - order_item["product"]["price"]
        }

        is_updated, numbers_updated = await update_cart(
            order_collection,
            cart["_id"],
            cart_data
        )
        if is_updated:
            print(f"Carrinho de compras atualizado com sucesso, número de documentos alterados {numbers_updated}")
        else:
            print("A ataulização do carrinho de compras falhou!")
    elif option == '5':
        # cart total price 
        cart_total_price = await get_cart_by_user_email(
            order_collection,
            users_collection,
            user["email"]
        )
        print(cart_total_price["price"])
    elif option == '6':
        # delete cart
        cart = await get_cart_by_user_email(
            order_collection,
            users_collection,
            user["email"]
        )

        result = await delete_cart(
            order_collection,
            cart["user"]["_id"]
        )

        print(result)

    await disconnect_db()
