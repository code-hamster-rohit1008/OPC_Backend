from db.config import client

def add(data: dict, collection: str, database: str):
    db = client[database]
    col = db[collection]
    result = col.insert_one(data)
    return str(result.inserted_id)

def get(query: dict, collection: str, database: str):
    db = client[database]
    col = db[collection]
    result = col.find_one(query)
    return result

def get_all(query: dict, collection: str, database: str):
    db = client[database]
    col = db[collection]
    results = col.find(query)
    return list(results)

def update(query: dict, update_data: dict, collection: str, database: str, keys: dict | None = None):
    db = client[database]
    col = db[collection]
    col.update_one(query, {"$set": update_data}, upsert=keys.get('upsert') if keys else False)

def delete(query: dict, collection: str, database: str):
    db = client[database]
    col = db[collection]
    col.delete_one(query)