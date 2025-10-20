import re
import easyocr
import numpy as np
import string

def only_letters_numbers(text: str) -> bool:
    """
    Verifica se o texto contém apenas letras (A-Z) e números (0-9)
    """
    text = text.replace("-", "").replace(" ", "").upper().strip()
    return bool(re.fullmatch(r'[A-Z0-9]+', text))

async def get_plate_info(img: np.ndarray) -> dict | None:
    reader = easyocr.Reader(['pt'], gpu=False, verbose=False)
    results = reader.readtext(img)

    best_plate = None
    best_confidence = 0.0

    for (bbox, text, confidence) in results:

        text = text.replace("-", "").replace(" ", "").upper().strip()

        if len(text) < 6 or text in ["BRASIL", "BR"]:
            continue
        
        if text:
            if not only_letters_numbers(text):
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_plate = text

            if best_plate is None:
                return {"plate": text, "confidence": confidence}

    return {"plate": best_plate, "confidence": best_confidence}

TAMANHO_PLACA = 7
MAX_PONTUACAO_PERFEITA = 100 

CONFUSOES_OCR = {
    "0": ["O", "Q"],
    "O": ["0", "Q"],
    "Q": ["O", "0"],
    "1": ["I", "L"],
    "I": ["1", "L"],
    "L": ["I", "1"],
    "2": ["Z"],
    "Z": ["2"],
    "5": ["S"],
    "S": ["5"],
    "8": ["B"],
    "B": ["8"],
    "6": ["G"],
    "G": ["6"],
    "4": ["A"],
    "A": ["4"]
}

def distancia_ponderada(plate_valid: str, plate_ocr: str) -> dict:
    """
    Calcula a similaridade ponderada entre duas placas (certa e OCR).
    Considera erros leves, graves e acertos em sequência.
    Retorna dicionário com pontuação total, similaridade e detalhes.
    """

    # --- Verificação inicial ---
    if len(plate_valid) != TAMANHO_PLACA or len(plate_ocr) != TAMANHO_PLACA:
        return {
            "similaridade": 0.0,
            "similaridade_pct": 0.0,
            "detalhes": [{
                "explicacao": f"Tamanho inválido - placa deve ter {TAMANHO_PLACA} caracteres (recebidos {len(plate_ocr)})"
            }]
        }

    custo_total = 70
    ordemCertaPosAnterior = False
    detalhes = []

    for i in range(TAMANHO_PLACA):
        v = plate_valid[i]
        o = plate_ocr[i]

        if v == o:
          
            pontos = 5 if ordemCertaPosAnterior else 0
            custo_total += pontos
            detalhes.append({
                "posicao": i + 1,
                "esperado": v,
                "obtido": o,
                "explicacao": f"Caractere correto (+{pontos})"
            })
            ordemCertaPosAnterior = True

        elif o in CONFUSOES_OCR.get(v, []):
            custo_total -= 3
            detalhes.append({
                "posicao": i + 1,
                "esperado": v,
                "obtido": o,
                "explicacao": f"Erro leve: confusão típica OCR ({v}->{o}) (-3)"
            })
            ordemCertaPosAnterior = False

        elif v.isalpha() != o.isalpha():
           
            custo_total -= 10
            detalhes.append({
                "posicao": i + 1,
                "esperado": v,
                "obtido": o,
                "explicacao": f"Erro grave: tipo incorreto ({'letra' if v.isalpha() else 'número'} → {'número' if o.isdigit() else 'letra'}) (-10)"
            })
            ordemCertaPosAnterior = False

        else:
          
            custo_total -= 5
            detalhes.append({
                "posicao": i + 1,
                "esperado": v,
                "obtido": o,
                "explicacao": f"Erro leve: caractere errado mas tipo certo ({v}->{o}) (-5)"
            })
            ordemCertaPosAnterior = False

    similarity = max(0.0, min(1.0, custo_total / MAX_PONTUACAO_PERFEITA))
    similarity_pct = round(similarity * 100, 1)

    return {
        "similaridade": similarity,
        "similaridade_pct": similarity_pct,
        "custo_total": custo_total,
        "detalhes": detalhes
    }