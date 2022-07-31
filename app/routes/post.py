from typing import  List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schema, oauth2
from ..models.post import  create, allPost, singlePost, delete, update, like_unlike, personal_post
from  ..database import get_db


router = APIRouter(tags = ['Posts'])


# Get post Created only by owner
@router.get("/ownerPost", response_model=List[schema.PostOpt])
async def get_owner_post(db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    return  personal_post(db, account_owner)


# Get all Post
@router.get("/allPosts", response_model=List[schema.PostAll])
async def get_allPost(db: Session = Depends(get_db)):
    return allPost(db)
    
# Create a Post
@router.post("/create", status_code=status.HTTP_201_CREATED,  response_model=schema.PostOpt)
async def createPost(request:schema.CreatePost, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    return create(request, db, account_owner)


# # Like & Unlike Post
@router.post("/like", status_code= status.HTTP_201_CREATED)
async def like_post(request: schema.Likes, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    return like_unlike(request, db, account_owner)

    
# # Get a Post
@router.get("/getOne/{id}")
async def get_singlepost(id:int, db:Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    return singlePost(id, db, account_owner)


# Delete a Post
@router.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_Post(id: int, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):    
    return delete(id, db, account_owner)


# Edit/Update a Post
@router.put("/edit/{id}",  response_model=schema.PostOpt)
async def editPost(id:int, update_post:schema.CreatePost, db: Session = Depends(get_db), account_owner: int = Depends(oauth2.get_current_user)):
    return update(id, update_post, db, account_owner)