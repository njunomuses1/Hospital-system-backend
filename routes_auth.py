"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
import schemas
import models
import auth


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.ApiResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        db_user = auth.create_user(db=db, user=user)
        
        # Create token for immediate login after registration
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": db_user.id},
            expires_delta=access_token_expires
        )
        
        return schemas.ApiResponse(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "user": schemas.User.model_validate(db_user)
            },
            message="User registered successfully",
            success=True
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=schemas.ApiResponse)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    try:
        user = auth.authenticate_user(db, user_credentials.email, user_credentials.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )
        
        return schemas.ApiResponse(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "user": schemas.User.model_validate(user)
            },
            message="Login successful",
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ LOGIN ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=schemas.ApiResponse)
async def get_current_user_info(current_user: models.User = Depends(auth.get_current_active_user)):
    """Get current logged-in user information"""
    return schemas.ApiResponse(
        data=schemas.User.model_validate(current_user),
        success=True
    )


@router.post("/refresh", response_model=schemas.ApiResponse)
async def refresh_token(current_user: models.User = Depends(auth.get_current_active_user)):
    """Refresh access token"""
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": current_user.id},
        expires_delta=access_token_expires
    )
    
    return schemas.ApiResponse(
        data={
            "access_token": access_token,
            "token_type": "bearer"
        },
        message="Token refreshed successfully",
        success=True
    )


