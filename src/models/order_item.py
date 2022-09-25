async def get_order_item(order_items_collection, order_item_id):
    try:
        data = await order_items_collection.find_one({'_id': order_item_id})
        if data:
            return data
    except Exception as e:
        print(f'get_order_item.error: {e}')


async def get_order_item_by_order_id_and_product_id(order_items_collection, order_id, product_code):
    try:
        data = await order_items_collection.find_one({"$and":[{"order.user._id": order_id}, {"product.code": product_code}]})
        if data:
            return data
    except Exception as e:
        print(f'get_order_item_by_order_id_and_product_id.error: {e}')


async def add_product_to_order(order_items_collection, order_item):
    try:
        order_item = await order_items_collection.insert_one(order_item)
        if order_item.inserted_id:
            order_item = await get_order_item(order_items_collection, order_item.inserted_id)
            return order_item

    except Exception as e:
        print(f'add_product_to_order.error: {e}')


async def delete_product_from_order(order_items_collection, order_item_id):
    try:
        order_item = await order_items_collection.delete_one(
            {'_id': order_item_id}
        )
        if order_item.deleted_count:
            return {'status': 'order item deleted'}
    except Exception as e:
        print(f'delete_order_item.error: {e}')
