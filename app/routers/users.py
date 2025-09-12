from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, models
from ..database import get_db
from .events import get_current_admin_user # We can reuse the admin dependency

router = APIRouter()

@router.get("/users/", response_model=List[schemas.User], tags=["Users"])
def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    """
    Retrieve all users. Only accessible to admin users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}/role", response_model=schemas.User, tags=["Users"])
def change_user_role(
    user_id: int,
    role_update: schemas.UserRoleUpdate, # The new role is sent in the request body
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    """
    Update a user's role. Only accessible to admin users.
    """
    # Optional: Prevent an admin from demoting themselves by accident
    if current_admin.id == user_id:
        raise HTTPException(status_code=400, detail="Admins cannot change their own role.")
        
    updated_user = crud.update_user_role(db, user_id=user_id, role=role_update.role)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user