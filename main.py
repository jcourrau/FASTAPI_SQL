from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uuid
import models
import schemas
import crud
import database

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="MLOPs first API",
    description="MLOPs API",
    version="0.0.1"
)

# Mensaje cuando se accede a /
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenido a la API de Usuarios"}

# POST: Crear usuario
@app.post("/users/", response_model=schemas.UserResponse, tags=["Users"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        new_user = crud.create_user(db, user)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": f"User {new_user.name} {new_user.lastname} created successfully.",
                "user": {
                    "id": new_user.id,
                    "name": new_user.name,
                    "lastname": new_user.lastname,
                    "age": new_user.age,
                    "email": new_user.email
                }
            }
        )
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# GET: Obtener usuario por ID (UUID)
@app.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
async def read_user(user_id: str, db: Session = Depends(database.get_db)):
    try:
        # Validar formato UUID
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID inválido, debe ser un UUID válido"
            )

        user = crud.get_user(db, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "User found successfully",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "lastname": user.lastname,
                    "age": user.age,
                    "email": user.email
                }
            }
        )
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
