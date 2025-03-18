from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

# Initialize FastAPI app
app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb+srv://kumkumpatel64:0SMHm4HtXy88ZPB9@cluster0.xysjt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.key_value_database
collection = db.data

# Pydantic Model for Data Validation
class DataItem(BaseModel):
    value: str

# Store a Key-Value Pair
@app.post("/store/{key}")
async def post_value(key: str, item: DataItem):
    # Store key-value pair in MongoDB
    if collection.find_one({"key": key}):
        raise HTTPException(status_code=400, detail="Key already exists")

    collection.insert_one({"key": key, "value": item.value})
    return {"message": "Stored successfully", "key": key, "value": item.value}

# Retrieve a Value by Key
@app.get("/store/{key}")
async def get_value(key: str):
    # Retrieves the value for a given key from MongoDB
    result = collection.find_one({"key": key})
    if not result:
        raise HTTPException(status_code=404, detail="Key not found")

    return {"key": key, "value": result["value"]}

# Delete a Key-Value Pair
@app.delete("/store/{key}")
async def delete_value(key: str):
    # Deletes a key-value pair from MongoDB
    result = collection.delete_one({"key": key})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Key not found")

    return {"message": "Deleted successfully", "key": key}
