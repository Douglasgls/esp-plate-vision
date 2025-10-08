import re
import easyocr
import numpy as np

def is_plate_format_fuzzy(text: str, threshold: float = 0.8) -> list:
    """
    Verifica se o texto segue aproximadamente o formato de placa antiga ou Mercosul.
    threshold: porcentagem mínima de caracteres corretos (ex: 0.8 = 80%)
    Retorna: [True/False, 'antiga'/'mercosul'/None]
    """
    text = text.replace("-", "").replace(" ", "").upper().strip()
    textSize = len(text)
    
    old_pattern = ['L','L','L','N','N','N','N']
    mercosul_pattern = ['L','L','L','N','L','N','N']
    
    def match_pattern(padrao):
        if textSize != len(padrao):
            return 0
        score = 0
        for i, p in enumerate(padrao):
            if p == 'L' and text[i].isalpha():
                score += 1
            elif p == 'N' and text[i].isdigit():
                score += 1
        return score / len(padrao)
    
    score_old = match_pattern(old_pattern)
    score_mercosul = match_pattern(mercosul_pattern)
    
    if score_old >= threshold:
        return [True, 'antiga']
    elif score_mercosul >= threshold:
        return [True, 'mercosul']
    
    return [False, None]

def only_letters_numbers(text: str) -> bool:
    """
    Verifica se o texto contém apenas letras (A-Z) e números (0-9)
    """
    text = text.replace("-", "").replace(" ", "").upper().strip()
    return bool(re.fullmatch(r'[A-Z0-9]+', text))

def is_valid_plate(text: str) -> bool:
    """
    Valida se o texto é uma placa válida com base na confiança mínima e formato
    """
    plate_check = is_plate_format_fuzzy(text, threshold=0.8)

    if plate_check[0] == False:
        return False

    if not only_letters_numbers(text):
        return False

    return True

async def validate_plate(img: np.ndarray) -> dict | None:
    reader = easyocr.Reader(['pt'])
    results = reader.readtext(img)

    best_plate = None
    best_confidence = 0.0

    for (bbox, text, confidence) in results:

        text = text.replace("-", "").replace(" ", "").upper().strip()

        if len(text) < 6 or text in ["BRASIL", "BR"]:
            continue
        
        if text:
            if is_valid_plate(text):
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_plate = text

            if best_plate is None:
                return {"plate": text, "confidence": confidence}

    return {"plate": best_plate, "confidence": best_confidence}