from pydantic import BaseModel, EmailStr

class UsuarioCriarSchema(BaseModel):
    email: EmailStr
    senha: str

class UsuarioRespostaSchema(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"