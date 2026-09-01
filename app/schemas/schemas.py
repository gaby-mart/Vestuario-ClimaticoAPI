from pydantic import BaseModel, Field

class RecomendacaoSchema(BaseModel):
    vestuario: str = Field(..., example="Roupas leves de algodão e óculos de sol.")
    atividade: str = Field(..., example="Ótimo dia para caminhadas ao ar livre.")

class RespostaClimaSchema(BaseModel):
    cidade: str = Field(..., example="Campinas")
    temperatura: float = Field(..., example=24.5)
    sensacao_termica: float = Field(..., example=25.0)
    condicao: str = Field(..., example="Ensolarado")
    umidade: int = Field(..., example=52)
    recomendacoes: RecomendacaoSchema

class ErroRespostaSchema(BaseModel):
    detalhe: str = Field(..., example="Cidade não encontrada.")