from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.auth import UsuarioCriarSchema, UsuarioRespostaSchema, TokenSchema
from app.core.security import gerar_hash_senha, verificar_senha, criar_token_acesso
from app.core.deps import get_db
from app.models.users_models import UsuarioModel

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/cadastrar", response_model=UsuarioRespostaSchema, status_code=201)
def cadastrar_usuario(usuario: UsuarioCriarSchema, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    novo_usuario = UsuarioModel(
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.post("/login", response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == form_data.username).first()
    
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    token = criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}