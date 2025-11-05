
from dotenv import load_dotenv

load_dotenv()

def replace_mongo_id(doc):
    """
    Converts a document's MongoDB _id (ObjectId)
    to a string and names the field 'id'.
    """
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc