from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlmodel import Session, select, func
from ..schemas import PostOut, PostBase, TokenData, PostCreate, PostsWithVotes
from ..database import get_session
from ..models import Posts, Votes
from ..oauth2 import get_current_user

router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)

@router.get("/", status_code=status.HTTP_200_OK,response_model=list[PostsWithVotes])
def get_posts(db: Session = Depends(get_session),
              limit: int = 10,
              skip: int = 0,
              search: str = ""):
    
    posts = db.exec(select(Posts,func.count(Votes.user_id).label("votes"))
                    .join(Votes, Votes.post_id == Posts.id,isouter=True)
                    .where(Posts.title.contains(search))
                    .limit(limit).offset(skip).group_by(Posts.id)
                    .order_by((func.count(Votes.user_id)).desc())).all()
    return posts

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostsWithVotes)
def get_a_post(id: int, 
               db: Session = Depends(get_session), 
               current_user: str = Depends(get_current_user)):
    
    post = db.exec(select(Posts,func.count(Votes.user_id).label("votes"))
                .join(Votes, Votes.post_id == Posts.id,isouter=True)
                .group_by(Posts.id)
                .where(Posts.id == id)).first()
    
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    if post.Posts.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    print(post)
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostCreate)
def create_post(payload: PostBase,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):
    
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    new_post = Posts(**payload.model_dump(), user_id=int(current_user))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostBase)
def update_post(id: int, 
                payload: PostBase, 
                db: Session = Depends(get_session), 
                current_user: str = Depends(get_current_user)):
    
    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    if post.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    # actualizamos los campos manualmente
    post.title = payload.title
    post.content = payload.content
    post.published = payload.published

    db.add(post)      # opcional, pero recomendable
    db.commit()
    db.refresh(post)  # para devolver el valor actualizado
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_session), 
                current_user: str = Depends(get_current_user)):

    post = db.get(Posts, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    if post.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    db.delete(post)
    db.commit()
    return