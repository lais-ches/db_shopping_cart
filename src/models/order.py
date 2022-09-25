from src.models.user import (get_user_by_email)

async def create_cart(order_collection, cart):
    try:
        cart = await order_collection.insert_one(cart)

        if cart.inserted_id:
            cart = await get_cart(order_collection, cart.inserted_id)
            return cart

    except Exception as e:
        print(f'create_cart.error: {e}')


async def get_cart(order_collection, order_id):
    try:
        data = await order_collection.find_one({'_id': order_id})
        if data:
            return data
    except Exception as e:
        print(f'get_cart.error: {e}')


async def get_cart_by_user_email(order_collection, users_collection, email):
    user = await get_user_by_email(users_collection, email)
    cart = await order_collection.find_one({'user._id': user["_id"]})
    return cart


async def update_cart(order_collection, cart_id, cart_data):
    try:
        data = {k: v for k, v in cart_data.items() if v is not None}

        cart = await order_collection.update_one(
            {'_id': cart_id},
            {'$set': data}
        )

        if cart.modified_count:
            return True, cart.modified_count

        return False, 0
    except Exception as e:
        print(f'update_cart.error: {e}')


async def delete_cart(order_collection, user_id):
    try:
        cart = await order_collection.delete_one(
            {'user._id': user_id}
        )
        if cart.deleted_count:
            return {'status': 'cart deleted'}
    except Exception as e:
        print(f'delete_cart.error: {e}')
