from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt

SECRET_KEY = "7GjTLm3rPHmyJtIIA6p3kTmpglokAKK3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def gerar_hash_senha(senha_plana: str) -> str:
    senha_bytes = senha_plana.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return hash_bytes.decode('utf-8')


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    senha_bytes = senha_plana.encode('utf-8')
    hash_bytes = senha_hash.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_bytes)


def criar_token_acesso(dados: dict) -> str:
    dados_para_encode = dados.copy()
    
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    dados_para_encode.update({"exp": expiracao})
    return jwt.encode(dados_para_encode, SECRET_KEY, algorithm=ALGORITHM)