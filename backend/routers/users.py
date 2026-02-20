from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from schemas.user import UserOut,RoleUpdate,UserCreate,UserBase
from dependencies import require_role
from enums.roles import UserRole

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.admin))):
    new_user = User(username=user_data.username, password=user_data.password, role=user_data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

@router.get("/", response_model=List[UserOut])
def get_all_users(db:Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.admin))):
    return db.query(User).all()



@router.patch("/{user_id}/role", response_model=UserOut)
def update_user_role(user_id: int, role_update: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.admin))):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.role = role_update.role
    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.admin))):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()

    return