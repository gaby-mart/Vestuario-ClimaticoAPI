from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.users_models import UsuarioModel
from app.core.security import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UsuarioModel:
    """
    Dependência que valida o Token JWT recebido no cabeçalho 'Authorization'.
    Retorna o objeto do usuário logado se o token for válido.
    """
    excecao_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais de acesso.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise excecao_credenciais
            
    except JWTError:
        raise excecao_credenciais

    
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    
    if usuario is None:
        raise excecao_credenciais

    return usuario