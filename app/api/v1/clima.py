from fastapi import APIRouter
from app.service.openweather import buscar_clima_cidade

router = APIRouter()

@router.get("/clima")
async def obter_clima(cidade: str):
    return await buscar_clima_cidade(cidade)