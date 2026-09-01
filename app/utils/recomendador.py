def gerar_recomendacao(temperatur : float, condicao : str) -> dict:
    condicao_lower = condicao.lower()

    if "chuva" in condicao_lower or "garoa" in condicao_lower:
        return {
            "vestuario": "Leve capa de chuva ou guarda-chuva e calçado fechado.",
            "atividade": "Bom dia para atividades em locais cobertos ou ficar em casa."
        }

    if temperatura < 15.0:
        return {
            "vestuario": "Frio! Use casaco pesado, jaqueta e calça comprida.",
            "atividade": "Ideal para bebidas quentes e passeios em locais fechados."
        }
    elif 15.0 <= temeperatura <= 23.0:
        return {
            "vestuario": "Clima ameno. Uma jaqueta leve ou moletom resolve bem.",
            "atividade": "Ótimo clima para caminhar no parque de casaco leve."
        }
    else:
        return {
            "vestuario": "Calor! Use camisetas leves, shorts e óculos de sol.",
            "atividade": "Excelente dia para atividades ao ar livre e muita hidratação."
        }