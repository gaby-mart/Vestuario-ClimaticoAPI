import httpx
from fastapi import HTTPException, status

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "a58cef8c0106223ee0c97c94d02030d4"

async def buscar_clima_cidade(cidade: str) -> dict:
    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    async with httpx.AsyncClient() as cliente:
        try:
            resposta = await cliente.get(BASE_URL, params=params)
            
            if resposta.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Chave da API do OpenWeather expirada, inválida ou ainda não ativada."
                )
            elif resposta.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cidade '{cidade}' não foi encontrada."
                )

            resposta.raise_for_status()
            dados = resposta.json()
            return {
                "cidade": dados.get("name", cidade),
                "temperatura": dados["main"]["temp"],
                "sensacao_termica": dados["main"]["feels_like"],
                "umidade": f"{dados['main']['humidity']}%",
                "descricao": dados["weather"][0]["description"]
            }

        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de clima temporariamente indisponível ou bloqueado pela rede/proxy."
            )