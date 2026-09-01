from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.users_models import UsuarioModel
from app.schemas.users_schema import (
    UsuarioCriarSchema, 
    UsuarioRespostaSchema, 
    UsuarioAtualizarSchema
)
from app.core.security import gerar_hash_senha
from app.core.deps import obter_usuario_atual  

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioRespostaSchema, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCriarSchema, db: Session = Depends(get_db)):
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


@router.get("/", response_model=List[UsuarioRespostaSchema])
def listar_usuarios(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(obter_usuario_atual)
):
    return db.query(UsuarioModel).offset(skip).limit(limit).all()

@router.get("/{usuario_id}", response_model=UsuarioRespostaSchema)
def buscar_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(obter_usuario_atual)
):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioRespostaSchema)
def atualizar_usuario(
    usuario_id: int, 
    dados: UsuarioAtualizarSchema, 
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(obter_usuario_atual)
):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if dados.email is not None:
        usuario.email = dados.email
    if dados.senha is not None:
        usuario.senha_hash = gerar_hash_senha(dados.senha)
    if dados.ativo is not None:
        usuario.ativo = dados.ativo

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(obter_usuario_atual)
):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(usuario)
    db.commit()
    return None