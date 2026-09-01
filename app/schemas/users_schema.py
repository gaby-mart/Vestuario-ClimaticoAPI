from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioCriarSchema(BaseModel):
    email: EmailStr
    senha: str

class UsuarioAtualizarSchema(BaseModel):
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    ativo: Optional[bool] = None

class UsuarioRespostaSchema(BaseModel):
    id: int
    email: EmailStr
    ativo: bool

    class Config:
        from_attributes = True