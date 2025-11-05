import os
from pymongo import MongoClient
from utils import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the connection string from the environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Create a synchronous client to connect to MongoDB
client = MongoClient(MONGO_URI)

# Select your database. Let's call it 'blog_db'
db = client.blog_db

# Select your collection. This is where all your blog post documents will be stored
posts_collection = db.posts_collection
