import re

def to_float(val):
    if not val:
        return None
    try:
        return float(val.replace(',', '.'))
    except:
        return None

def extract_inline(texto, keyword):
    pattern = re.compile(rf'{keyword}\s*:\s*(-?\d+[\.,]?\d*)', re.IGNORECASE)
    match = pattern.search(texto)
    if match:
        return to_float(match.group(1))
    return None

def extract_resultado_after_title(texto, title):
    # Match the title, then up to 150 non-RESULTADO chars, then RESULTADO and extract first number
    pattern = re.compile(rf'{title}.{{0,150}}?RESULTADO[^\d]*?(-?\d+[\.,]?\d*)', re.IGNORECASE | re.DOTALL)
    match = pattern.search(texto)
    if match:
        return to_float(match.group(1))
    return None

def extract_wbc(texto, keyword):
    pattern = re.compile(rf'^[^\n]*?{keyword}[^\n]*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.search(texto)
    if match:
        line = match.group(0)
        idx = re.search(keyword, line, re.IGNORECASE).start()
        line_before = line[:idx]
        
        m_x = re.search(r'(\d+[\.,]?\d*)\s*x', line_before)
        if m_x:
            return to_float(m_x.group(1))
            
        m_first = re.search(r'(\d+[\.,]?\d*)', line_before)
        if m_first:
            return to_float(m_first.group(1))
            
    # Fallback to "Keyword: value"
    pattern2 = re.compile(rf'{keyword}\s*:\s*(-?\d+[\.,]?\d*)', re.IGNORECASE)
    match2 = pattern2.search(texto)
    if match2:
        return to_float(match2.group(1))
        
    return None

def extract_general(texto, keyword):
    pattern = re.compile(rf'^[^\n]*?{keyword}[^\n]*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.search(texto)
    if match:
        line = match.group(0)
        idx = re.search(keyword, line, re.IGNORECASE).start()
        line_before = line[:idx]
        
        nums = re.findall(r'(-?\d+[\.,]?\d*)(?:\s*(%|x|milhões|g/dL|fL|pg|mmol/L|mg/dL|mmHg|U/L|ng/mL|µg/dL))?', line_before)
        for val, unit in nums:
            if unit != '%':
                return to_float(val)
        
        if nums:
            return to_float(nums[0][0])
            
    pattern2 = re.compile(rf'{keyword}\s*:\s*(-?\d+[\.,]?\d*)', re.IGNORECASE)
    match2 = pattern2.search(texto)
    if match2:
        return to_float(match2.group(1))
        
    return None

def extrair_gasometria(texto):
    return {
        'pH': extract_general(texto, r'pH'),
        'pO2': extract_general(texto, r'pO2'),
        'pCO2': extract_general(texto, r'pCO2'),
        'HCO3': extract_general(texto, r'HCO3'),
        'BE': extract_general(texto, r'BE\b'),
        'Sat O2': extract_general(texto, r'Sat\.? O2'),
        'Na': extract_general(texto, r'NA'),
        'K': extract_general(texto, r'K'),
        'Ca++': extract_general(texto, r'CA\+'),
        'Cl': extract_general(texto, r'CL'),
        'Glicose': extract_general(texto, r'Glicose'),
        'Lactato': extract_general(texto, r'Lactato')
    }

def extrair_hemograma(texto):
    return {
        'Leucócitos': extract_general(texto, r'Leuc[óo]citos'),
        'Neutrófilos': extract_wbc(texto, r'Neutr[óo]filos'),
        'Eosinófilos': extract_wbc(texto, r'Eosin[óo]filos'),
        'Basófilos': extract_wbc(texto, r'Bas[óo]filos'),
        'Monócitos': extract_wbc(texto, r'Mon[óo]citos'),
        'Linfócitos': extract_wbc(texto, r'Linf[óo]citos'),
        'Hemácias': extract_general(texto, r'Hem[áa]cias'),
        'Hb': extract_general(texto, r'Hemoglobina'),
        'Ht': extract_general(texto, r'Hemat[óo]crito'),
        'VCM': extract_general(texto, r'VCM'),
        'HCM': extract_general(texto, r'HCM'),
        'CHCM': extract_general(texto, r'CHCM'),
        'RDW': extract_general(texto, r'RDW(?:-CV)?'),
        'PLQ': extract_general(texto, r'Plaquetas'),
        'Ret': extract_resultado_after_title(texto, r'CONTAGEM DE RETICUL[ÓO]CITOS') or extract_general(texto, r'Percentual')
    }

def processar_exames(texto):
    gaso = extrair_gasometria(texto)
    hemo = extrair_hemograma(texto)
    
    exames = {
        'Ur': extract_resultado_after_title(texto, r'UR[ÉE]IA'),
        'Cr': extract_resultado_after_title(texto, r'CREATININA'),
        'PCR': extract_resultado_after_title(texto, r'PROTE[ÍI]NA C REATIVA.*?PCR'),
        'AST': extract_resultado_after_title(texto, r'ASPARTATO AMINOTRANSFERASE(?:.*?AST)?'),
        'ALT': extract_resultado_after_title(texto, r'ALANINO AMINOTRANSFERASE(?:.*?ALT)?'),
        'IST': extract_resultado_after_title(texto, r'[ÍI]NDICE DE SATURA[ÇC][ÃA]O DA TRANSFERRINA'),
        'TIBC': extract_resultado_after_title(texto, r'CAPACIDADE TOTAL DE FIXA[ÇC][ÃA]O DE FERRO'),
        'Ferro': extract_resultado_after_title(texto, r'FERRO S[ÉE]RICO'),
        'VitD': extract_resultado_after_title(texto, r'25-OH VITAMINA D TOTAL'),
        'C3': extract_resultado_after_title(texto, r'COMPLEMENTO C3'),
        'C4': extract_resultado_after_title(texto, r'COMPLEMENTO C4'),
        'Ferritina': extract_resultado_after_title(texto, r'FERRITINA'),
        'Mg': extract_resultado_after_title(texto, r'MAGN[ÉE]SIO'),
        'P': extract_resultado_after_title(texto, r'F[ÓO]SFORO')
    }
    
    for k in ['Leucócitos', 'Neutrófilos', 'Eosinófilos', 'Basófilos', 'Monócitos', 'Linfócitos']:
        val = hemo.get(k)
        if val is not None and val < 1000:
            hemo[k] = val * 1000

    if hemo.get('PLQ') is not None and hemo.get('PLQ') < 10000:
        hemo['PLQ'] = hemo['PLQ'] * 1000
        
    exames.update(hemo)
    
    gaso_renamed = {
        'pH': gaso.get('pH'),
        'pO2': gaso.get('pO2'),
        'pCO2': gaso.get('pCO2'),
        'HCO3': gaso.get('HCO3'),
        'BE': gaso.get('BE'),
        'Sat O2': gaso.get('Sat O2'),
        'K (gaso)': gaso.get('K'),
        'Na (gaso)': gaso.get('Na'),
        'Ca++': gaso.get('Ca++'),
        'Cl': gaso.get('Cl'),
        'Glicose': gaso.get('Glicose'),
        'Lactato': gaso.get('Lactato'),
    }
    exames.update(gaso_renamed)
    
    return {k: v for k, v in exames.items() if v is not None}

def formatar_saida(exames_classificados):
    import datetime
    hoje = datetime.datetime.now().strftime("%d/%m/%Y")
    
    ordem = ['Ur', 'Cr', 'PCR', 'AST', 'ALT', 'IST', 'TIBC', 'Ferro', 'VitD', 'C3', 'C4', 'Ferritina', 'Mg', 'P', 
             'Leucócitos', 'Neutrófilos', 'Eosinófilos', 'Basófilos', 'Monócitos', 'Linfócitos', 
             'Hemácias', 'Hb', 'Ht', 'VCM', 'HCM', 'CHCM', 'RDW', 'PLQ', 'Ret',
             'pH', 'pO2', 'pCO2', 'HCO3', 'BE', 'Sat O2', 
             'K (gaso)', 'Na (gaso)', 'Ca++', 'Cl', 'Glicose', 'Lactato']
    
    display_names = {
        'Neutrófilos': 'Neutr.',
        'Eosinófilos': 'Eo.',
        'Basófilos': 'Bas.',
        'Monócitos': 'Mono.',
        'Linfócitos': 'Linf.'
    }
    
    html = f"({hoje}) - SANGUE: "
    
    items = []
    for k in ordem:
        if k in exames_classificados:
            exame = exames_classificados[k]
            nome = display_names.get(k, k)
            
            val = exame['valor']
            if val.is_integer() or k in ['Leucócitos', 'Neutrófilos', 'Eosinófilos', 'Basófilos', 'Monócitos', 'Linfócitos', 'PLQ']:
                val_str = str(int(val))
            else:
                val_str = f"{val:.2f}".rstrip('0').rstrip('.')
            
            cor = 'red' if exame['alterado'] else 'black'
            span = f"<span style='color: {cor}; font-weight: {'bold' if exame['alterado'] else 'normal'};'>{nome}: {val_str}</span>"
            items.append(span)
            
    html += " | ".join(items)
    return html
