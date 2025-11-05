from fastapi import FastAPI, HTTPException, status
import db_blog  # Import our new database connection
import models  # Import our Pydantic models
import utils  # Import your existing utils
from bson import ObjectId  # This is needed to convert string IDs to Mongo's ObjectId
from typing import List

# --- Application Setup ---
app = FastAPI(
    title="My Blog API (Sync)",
    description="A FastAPI application to manage blog posts with a MongoDB database using pymongo.",
    version="1.0.0"
)

# --- Endpoints ---

@app.get("/", tags=["Home"])
def get_home():
    """
    Welcome endpoint.
    """
    return {"message": "Welcome to my Blogpost API"}

# --- Post Endpoints ---

@app.post("/posts", response_model=models.PostResponse, status_code=status.HTTP_201_CREATED, tags=["Posts"])
def create_post(post: models.PostCreate):
    """
    Create a new blog post.
    (Note: This is 'def', not 'async def')
    """
    # Convert the Pydantic model to a dictionary
    post_dict = post.model_dump()
    
    # Insert the new post into the database
    # .insert_one() is now a normal function call
    result = db_blog.posts_collection.insert_one(post_dict)
    
    # Get the newly created post from the DB to return it
    new_post = db_blog.posts_collection.find_one({"_id": result.inserted_id})
    
    # Use your 'replace_mongo_id' helper to format the response!
    return utils.replace_mongo_id(new_post)


@app.get("/posts", response_model=List[models.PostResponse], tags=["Posts"])
def get_all_posts():
    """
    Retrieve all blog posts from the database.
    """
    all_posts = []
    # .find() returns a 'cursor'
    # We just loop through it normally
    cursor = db_blog.posts_collection.find()
    for post in cursor:
        all_posts.append(utils.replace_mongo_id(post))
    return all_posts


@app.get("/posts/{post_id}", response_model=models.PostResponse, tags=["Posts"])
def get_post(post_id: str):
    """
    Retrieve a single blog post by its ID.
    """
    try:
        # MongoDB uses a special ObjectId, not a plain string.
        # We must convert the string ID from the URL into an ObjectId.
        post_obj_id = ObjectId(post_id)
    except Exception:
        # If the string is not a valid ObjectId, raise a 400 error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid post ID")

    # .find_one() is a normal function call
    post = db_blog.posts_collection.find_one({"_id": post_obj_id})
    
    if post is None:
        # If the post is not found, raise a 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    # Use your helper to format the _id to id
    return utils.replace_mongo_id(post)


@app.put("/posts/{post_id}", response_model=models.PostResponse, tags=["Posts"])
def update_post(post_id: str, updated_post: models.PostUpdate):
    """
    Update an existing blog post.
    """
    try:
        post_obj_id = ObjectId(post_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid post ID")

    # Check if the post exists before trying to update it
    post = db_blog.posts_collection.find_one({"_id": post_obj_id})
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    # Convert the update model to a dict,
    # 'exclude_unset=True' means we only include fields that the user actually sent
    update_data = updated_post.model_dump(exclude_unset=True)
    
    # Update the post in the database
    if update_data:
        db_blog.posts_collection.update_one(
            {"_id": post_obj_id},
            {"$set": update_data}
        )
    
    # Get the updated post from the DB and return it
    updated_post_doc = db_blog.posts_collection.find_one({"_id": post_obj_id})
    return utils.replace_mongo_id(updated_post_doc)


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
def delete_post(post_id: str):
    """
    Delete a blog post by its ID.
    """
    try:
        post_obj_id = ObjectId(post_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid post ID")

    # .delete_one() returns a result object
    result = db_blog.posts_collection.delete_one({"_id": post_obj_id})
    
    # If 'deleted_count' is 0, it means no post with that ID was found
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    # On success, return a 204 No Content response (by returning nothing)
    return




