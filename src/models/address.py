import traceback

async def create_address(users_collection, address_collection, address):
    try:
        user = await (users_collection.find_one({"email":address["user"]["email"]}))

        if user == None:
            return "Não existe usuário"
        locate_address = await (address_collection.find_one({"user._id":user["_id"]}))
        if locate_address == None:
            address = await address_collection.insert_one(address)
        
            if address.inserted_id:
                address = await get_address(address_collection, address.inserted_id)
                return address
        else:
            address = await address_collection.update_one(
            {'user._id': user["_id"]},
            {'$set': {'address':address}}
            )
            if address.modified_count:
                return True, address.modified_count
        
    except Exception as e:
        print(traceback.format_exc())
        print(f'create_address.error: {e}')

async def get_address(address_collection, address_street):
    try:
        data = await address_collection.find_one({'address.street': address_street})
        if data:
            return data
    except Exception as e:
        print(f'get_address.error: {e}')


async def get_address_by_street(address_collection, street):
    try:
        address = await address_collection.find_one({"address.street": street})
        return address
    except Exception as e:
        print(f'get_address_by_street.error: {e}')


async def delete_address(address_collection, address_id):
    try:
        address = await address_collection.delete_one(
            {'_id': address_id}
        )
        if address.deleted_count:
            return {'status': 'Address deleted'}
    except Exception as e:
        print(f'delete_address.error: {e}')
