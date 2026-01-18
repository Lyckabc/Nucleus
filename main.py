from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import setup_db

app = FastAPI(
    title="Nucleus Database Management API",
    description="Central database management service for creating databases and users",
    version="1.0.0"
)


class DatabaseCreateRequest(BaseModel):
    new_db: str = Field(..., description="Name of the new database to create", min_length=1)
    new_user: str = Field(..., description="Name of the new database user to create", min_length=1)
    new_pass: str = Field(..., description="Password for the new database user", min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "new_db": "my_database",
                "new_user": "my_user",
                "new_pass": "secure_password123"
            }
        }


class DatabaseCreateResponse(BaseModel):
    success: bool
    message: str
    database: Optional[str] = None
    user: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "Nucleus Database Management API",
        "version": "1.0.0",
        "endpoints": {
            "create_database": "/api/database/create",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/database/create", response_model=DatabaseCreateResponse)
async def create_database(request: DatabaseCreateRequest):
    """
    Create a new PostgreSQL database and user.
    
    This endpoint creates:
    - A new PostgreSQL user with SUPERUSER privileges
    - A new PostgreSQL database owned by the new user
    
    If the user or database already exists, they will be skipped.
    """
    try:
        setup_db.create_database_and_user(
            new_db=request.new_db,
            new_user=request.new_user,
            new_pass=request.new_pass
        )
        
        return DatabaseCreateResponse(
            success=True,
            message=f"Database '{request.new_db}' and user '{request.new_user}' created successfully",
            database=request.new_db,
            user=request.new_user
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create database: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
