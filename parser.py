import re

def to_float(val):
    if not val:
        return None
    try:
        return float(val.replace(',', '.'))
    except:
        return None

def limpar_valor(valor):
    linhas = valor.split('\n')
    linhas_limpas = []
    ignore_prefixes = ['liberado por', 'responsáveis técnicos', 'dra.', 'dr.', 'hospital das clínicas', 'cep:', 'data da coleta', 'o volume do material', 'cultura para micobactéria', 'referência:']
    for linha in linhas:
        l = linha.strip()
        if any(l.lower().startswith(p) for p in ignore_prefixes):
            break
        if l:
            linhas_limpas.append(l)
    return ' '.join(linhas_limpas)

def check_alterado(valor, ref):
    if not ref or ref == '-': return False
    valor_lower = str(valor).lower()
    ref_lower = str(ref).lower()
    
    if 'negativo' in ref_lower or 'não reagente' in ref_lower or 'nao reagente' in ref_lower or 'ausente' in ref_lower:
        if ('positivo' in valor_lower or 'reagente' in valor_lower or 'presente' in valor_lower or '+' in valor_lower or 'traços' in valor_lower) and ('não reagente' not in valor_lower and 'nao reagente' not in valor_lower and 'falso positivo' not in valor_lower):
            return True
        if re.search(r'\d', valor) and not re.search(r'<', valor) and not re.search(r'<=', valor):
            return True
            
    try:
        v_match = re.search(r'(-?\d+[\.,]?\d*)', str(valor))
        if v_match:
            v_num = float(v_match.group(1).replace(',', '.'))
            
            r_match = re.search(r'(-?\d+[\.,]?\d*)\s*(?:a|-)\s*(-?\d+[\.,]?\d*)', str(ref))
            if r_match:
                r_min = float(r_match.group(1).replace(',', '.'))
                r_max = float(r_match.group(2).replace(',', '.'))
                if v_num < r_min or v_num > r_max:
                    return True
            
            r_less = re.search(r'(?:<|<=|inferior a|até|menor que)\s*(-?\d+[\.,]?\d*)', str(ref), re.IGNORECASE)
            if r_less:
                r_max = float(r_less.group(1).replace(',', '.'))
                if 'até' in ref_lower or '<=' in ref_lower:
                    if v_num > r_max:
                        return True
                else:
                    if v_num >= r_max:
                        return True
                    
            r_greater = re.search(r'(?:>|>=|superior a|maior que)\s*(-?\d+[\.,]?\d*)', str(ref), re.IGNORECASE)
            if r_greater:
                r_min = float(r_greater.group(1).replace(',', '.'))
                if '>=' in ref_lower:
                    if v_num < r_min:
                        return True
                else:
                    if v_num <= r_min:
                        return True
    except:
        pass
        
    return False

def processar_bloco(bloco):
    exames_list = []
    nome_exame = bloco['nome']
    material = bloco['material']
    conteudo = bloco['conteudo']
    
    m_isolados = list(re.finditer(r'Isolado\s*\d+\s*:\s*(.*?)\n(?:.*?Crescimento\s*:\s*(.*?)(?:\n|$))?', conteudo, re.IGNORECASE))
    if m_isolados:
        for m in m_isolados:
            microrganismo = m.group(1).strip()
            crescimento = m.group(2).strip() if m.group(2) else ""
            valor = f"{microrganismo} ({crescimento})" if crescimento else microrganismo
            exames_list.append({
                'nome': nome_exame,
                'valor': valor,
                'referencia': 'Negativo / Sem crescimento',
                'material': material,
                'alterado': True,
                'detalhes': '-'
            })
        return exames_list
        
    m_resultado = re.search(r'RESULTADO\s*:\s*(.*?)(?:V\.R\.\s*:|Valores de refer|Valor de refer|$)', conteudo, re.IGNORECASE | re.DOTALL)
    if m_resultado:
        valor = m_resultado.group(1).strip()
        valor = limpar_valor(valor)
        valor = re.sub(r'\s+', ' ', valor)
        
        ref = "-"
        m_ref = re.search(r'(?:V\.R\.\s*:|Valores de refer[^:]*:|Valor de refer[^:]*:)\s*(.*?)(?:\n\n|\n[A-ZÇÃÕÁÉÍÓÚÂÊÔÀ][a-z]|$)', conteudo, re.IGNORECASE | re.DOTALL)
        if m_ref:
            ref = m_ref.group(1).strip()
            ref = re.sub(r'\s+', ' ', ref)
            
        if not valor and ref:
            # Special case: RESULTADO: V.R.: negativo \n Negativo.
            m_next = re.search(re.escape(ref) + r'\s*\n\s*(.*?)(?:\n\n|\n[A-ZÇÃÕÁÉÍÓÚÂÊÔÀ][a-z]|$)', conteudo, re.IGNORECASE | re.DOTALL)
            if m_next:
                valor = m_next.group(1).strip()
                valor = limpar_valor(valor)
                valor = re.sub(r'\s+', ' ', valor)
                
        exames_list.append({
            'nome': nome_exame,
            'valor': valor,
            'referencia': ref,
            'material': material,
            'alterado': check_alterado(valor, ref),
            'detalhes': '-'
        })
        return exames_list

    m_resultado_nl = re.search(r'RESULTADO\n+(.*?)(?:\n\n|\n[A-ZÇÃÕÁÉÍÓÚÂÊÔÀ][a-z]|$)', conteudo, re.IGNORECASE | re.DOTALL)
    if m_resultado_nl:
        valor = m_resultado_nl.group(1).strip()
        valor = limpar_valor(valor)
        valor = re.sub(r'\s+', ' ', valor)
        alterado = False
        if "não foram visualizadas" not in valor.lower() and "não houve" not in valor.lower() and "negativ" not in valor.lower() and "não reagente" not in valor.lower() and "nao reagente" not in valor.lower():
            alterado = True
        exames_list.append({
            'nome': nome_exame,
            'valor': valor,
            'referencia': '-',
            'material': material,
            'alterado': alterado,
            'detalhes': '-'
        })
        return exames_list
        
    linhas = conteudo.split('\n')
    for linha in linhas:
        linha = linha.strip()
        if not linha or re.search(r'Método|Material|V\.R\.', linha, re.IGNORECASE) and not re.search(r':\s*(?:V\.R\.\s*:)?', linha, re.IGNORECASE):
            continue
            
        m_hemo = re.search(r'^([\d\,\.]+\s*(?:/mm³|/campo|x\s*10³/µL|%|milhões/µL|g/dL|fL|pg)?(?:[\s\d\,\.]+%?)?)\s+([A-Za-zÀ-ÿ\s]+):\s*(?:V\.R\.\s*:)?\s*(.*)$', linha, re.IGNORECASE)
        if m_hemo:
            valor = m_hemo.group(1).strip()
            sub_nome = m_hemo.group(2).strip()
            ref = m_hemo.group(3).strip()
            if ref == "": ref = "-"
            
            exames_list.append({
                'nome': f"{nome_exame} - {sub_nome}" if nome_exame != "EXAME" else sub_nome,
                'valor': valor,
                'referencia': ref,
                'material': material,
                'alterado': check_alterado(valor, ref),
                'detalhes': '-'
            })
            continue
            
        m_urina = re.search(r'^([A-Za-zÀ-ÿ\s\-\+]+):\s*(.*?)\s+V\.R\.\s*:\s*(.*)$', linha, re.IGNORECASE)
        if m_urina:
            sub_nome = m_urina.group(1).strip()
            valor = m_urina.group(2).strip()
            ref = m_urina.group(3).strip()
            exames_list.append({
                'nome': f"{nome_exame} - {sub_nome}" if nome_exame != "EXAME" else sub_nome,
                'valor': valor,
                'referencia': ref,
                'material': material,
                'alterado': check_alterado(valor, ref),
                'detalhes': '-'
            })
            continue
            
        m_kv = re.search(r'^([A-Za-zÀ-ÿ\s\-\+]+):\s*(.*)$', linha)
        if m_kv and "V.R." not in linha and "Valores" not in linha and "Método" not in linha and "Material" not in linha:
            sub_nome = m_kv.group(1).strip()
            
            ignore_keywords = ['liberado', 'cep', 'fones', 'cnpj', 'emissão', 'cliente', 'dt. nasc', 'rg', 'médico', 'clínica', 'origem', 'pedido', 'liberação', 'data da coleta', 'cnes', 'npf', 'fl.', 'responsáveis', 'obs', 'nota', 'referência']
            if any(kw in sub_nome.lower() for kw in ignore_keywords):
                continue
                
            valor = m_kv.group(2).strip()
            valor = limpar_valor(valor)
            exames_list.append({
                'nome': f"{nome_exame} - {sub_nome}" if nome_exame != "EXAME" else sub_nome,
                'valor': valor,
                'referencia': '-',
                'material': material,
                'alterado': False,
                'detalhes': '-'
            })
            
    return exames_list

def processar_exames_geral(texto):
    blocos = []
    lines = texto.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r'^(?:Material|MATERIAL)\s*:', line, re.IGNORECASE):
            nome_exame = lines[i-1].strip() if i > 0 else "EXAME"
            nome_exame = re.sub(r'=+', '', nome_exame).strip()
            material = re.sub(r'^(?:Material|MATERIAL)\s*:\s*', '', line, flags=re.IGNORECASE).strip()
            
            conteudo = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if j+1 < len(lines) and re.match(r'^(?:Material|MATERIAL)\s*:', lines[j+1].strip(), re.IGNORECASE):
                    break
                conteudo.append(lines[j])
                j += 1
            
            blocos.append({
                'nome': nome_exame,
                'material': material,
                'conteudo': '\n'.join(conteudo)
            })
            i = j
        else:
            i += 1

    exames_list = []
    for bloco in blocos:
        exames_list.extend(processar_bloco(bloco))
        
    return exames_list

def extrair_gasometria(texto):
    exames = processar_exames_geral(texto)
    gaso = {}
    for ex in exames:
        nome = ex['nome'].lower()
        val_match = re.search(r'(-?\d+[\.,]?\d*)', str(ex['valor']))
        if val_match:
            val = float(val_match.group(1).replace(',', '.'))
            if 'ph' in nome: gaso['pH'] = val
            elif 'po2' in nome: gaso['pO2'] = val
            elif 'pco2' in nome: gaso['pCO2'] = val
            elif 'hco3' in nome: gaso['HCO3'] = val
            elif 'be' in nome: gaso['BE'] = val
            elif 'sat o2' in nome or 'saturação' in nome: gaso['Sat O2'] = val
            elif 'sódio' in nome or 'na' in nome.split(): gaso['Na'] = val
            elif 'potássio' in nome or 'k' in nome.split(): gaso['K'] = val
            elif 'cálcio' in nome or 'ca++' in nome.split(): gaso['Ca++'] = val
            elif 'cloro' in nome or 'cl' in nome.split(): gaso['Cl'] = val
            elif 'glicose' in nome: gaso['Glicose'] = val
            elif 'lactato' in nome: gaso['Lactato'] = val
            elif 'uréia' in nome or 'ur' in nome.split(): gaso['Ur'] = val
    return gaso

def formatar_saida(exames_list):
    import datetime
    hoje = datetime.datetime.now().strftime("%d/%m/%Y")
    
    grouped = {}
    for ex in exames_list:
        mat = ex.get('material', 'OUTROS').upper().strip()
        if mat in ['LÍQUIDO CEFALORRAQUEANO', 'LIQUOR', 'LÍQUOR', 'LÍQUIDO CEFALORRAQUIDIANO', 'LÍQUIDO CEFALORRAQUIANO']:
            mat = 'LÍQUOR'
        if mat not in grouped:
            grouped[mat] = []
        grouped[mat].append(ex)
        
    html_parts = []
    ordem_materiais = ['SANGUE', 'URINA', 'LÍQUOR']
    for m in list(grouped.keys()):
        if m not in ordem_materiais:
            ordem_materiais.append(m)
            
    for mat in ordem_materiais:
        if mat not in grouped or not grouped[mat]:
            continue
        items = grouped[mat]
        part_items = []
        for ex in items:
            nome = ex.get('nome')
            if ' - ' in nome:
                nome = nome.split(' - ')[-1] # Show only sub-name in summary
                
            valor = str(ex.get('valor'))
            m_val = re.search(r'(-?\d+[\.,]?\d*)', valor)
            if m_val and len(valor) < 15:
                valor = m_val.group(1)
                
            alterado = ex.get('alterado', False)
            
            cor = 'red' if alterado else 'black'
            fw = 'bold' if alterado else 'normal'
            span = f"<span style='color: {cor}; font-weight: {fw};'>{nome}: {valor}</span>"
            part_items.append(span)
            
        html_parts.append(f"<strong>{mat}</strong>: " + " | ".join(part_items))
        
    if not html_parts:
        return f"({hoje}) - Nenhum exame reconhecido."
        
    return f"({hoje}) - " + "<br>".join(html_parts)
