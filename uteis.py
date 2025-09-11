import re

def is_plate_format_fuzzy(text: str, threshold: float = 0.8) -> list:
    """
    Verifica se o texto segue aproximadamente o formato de placa antiga ou Mercosul.
    threshold: porcentagem mínima de caracteres corretos (ex: 0.8 = 80%)
    Retorna: [True/False, 'antiga'/'mercosul'/None]
    """
    text = text.replace("-", "").replace(" ", "").upper().strip()
    textSize = len(text)
    
    padrao_antigo = ['L','L','L','N','N','N','N']
    padrao_mercosul = ['L','L','L','N','L','N','N']
    
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
    
    score_antiga = match_pattern(padrao_antigo)
    score_mercosul = match_pattern(padrao_mercosul)
    
    if score_antiga >= threshold:
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

def is_valid_plate(text: str, confidence: float) -> bool:
    """
    Valida se o texto é uma placa válida com base na confiança mínima e formato
    """
    plate_check = is_plate_format_fuzzy(text, threshold=0.8)
    
    if plate_check[0] == False:
        return False
    
    if not only_letters_numbers(text):
        return False
    
    return True