from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# This is the base model.
# It contains all the fields that are common for
# creating and reading posts.
class PostBase(BaseModel):
    title: str
    author: str
    short_read: str
    content: str
    # We use default_factory to set the date to 'now' when a post is created
    date_published: datetime = Field(default_factory=datetime.now)

# This model is used when CREATING a new post.
# It's what you expect in the body of your POST request.
# It has all the same fields as PostBase.
class PostCreate(PostBase):
    pass

# This model is used when UPDATING a post.
# All fields are 'Optional' so the user can update
# just the title, or just the content, etc.
class PostUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    short_read: Optional[str] = None
    content: Optional[str] = None
    date_published: Optional[datetime] = None

# This model is used when READING/RETURNING a post.
# It includes the 'id' field, which MongoDB gives us.
# Notice we use 'str' for the id, not 'int'.
class PostResponse(PostBase):
    id: str

