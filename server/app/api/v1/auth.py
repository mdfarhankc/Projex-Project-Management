from fastapi import APIRouter, HTTPException, status



router = APIRouter(tags=["Auth"])

@router.post("/register")
def auth_register():
    pass

@router.post("/login")
def auth_login():
    pass

@router.post("/refresh")
def auth_token_refresh():
    pass

@router.post("/logout")
def auth_token_refresh():
    pass