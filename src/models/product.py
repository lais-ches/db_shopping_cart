async def create_product(product_collection, product):
    try:
        product = await product_collection.insert_one(product)

        if product.inserted_id:
            product = await get_product(product_collection, product.inserted_id)
            return product

    except Exception as e:
        print(f'create_product.error: {e}')

async def get_product(product_collection, product_id):
    try:
        data = await product_collection.find_one({'_id': product_id})
        if data:
            return data
    except Exception as e:
        print(f'get_product.error: {e}')

async def get_product_by_code(product_collection, code):
    product = await product_collection.find_one({'code': code})
    return product


async def delete_product(product_collection, product_id):
    try:
        product = await product_collection.delete_one(
            {'_id': product_id}
        )
        if product.deleted_count:
            return {'status': 'Product deleted'}
    except Exception as e:
        print(f'delete_product.error: {e}')
