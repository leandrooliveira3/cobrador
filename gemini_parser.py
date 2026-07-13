import os
import json
import urllib.request
import urllib.error
import datetime

def chamar_gemini(texto_pdf):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY não configurada no ambiente.")
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
Sua tarefa é analisar o seguinte relatório de exames laboratoriais em português (gerado pelo Hospital das Clínicas da UFMG) e extrair TODOS os exames que aparecem no relatório de forma estruturada.

Seja extremamente abrangente: localize e descreva todo e qualquer exame que apareça, tais como sorologias, líquor, urina, culturas, hemoculturas, hemograma, eletrólitos, gasometria, bioquímica, etc. Não omita nenhum exame.

Para exames complexos (como culturas e líquor):
- Para culturas (ex: Urocultura, Hemocultura), extraia os microrganismos isolados (se houver), ou se deu negativo/sem crescimento. Inclua o antibiograma nos detalhes se julgar relevante.
- Para líquor (LCR/Líquido Cefalorraquidiano), extraia todos os componentes de citometria, bioquímica e citologia.
- Para sorologias, extraia os resultados (ex: "Não Reagente", "Negativo", ou valores numéricos).

Retorne um JSON contendo os seguintes campos exatamente:
1. "exames": uma lista de objetos, onde cada objeto descreve um exame:
   - "nome" (string): Nome do exame (ex: "Urocultura", "Citometria - Células nucleadas", "Sódio", "VDRL"). Use nomes legíveis e padronizados.
   - "valor" (string): O resultado do exame conforme aparece (ex: "134 mmol/L", "Pseudomonas aeruginosa (50.000 UFC/mL)", "Não Reagente", "Negativo", "159 mg/dL").
   - "referencia" (string): O valor de referência esperado (ex: "137 a 145 mmol/L", "Negativo", "< 5 células/mm³", "15 a 45 mg/dL"). Se não houver, coloque "-".
   - "material" (string): O material biológico (ex: "SANGUE", "URINA", "LIQUOR", etc.). Se não conseguir identificar, coloque "OUTROS".
   - "alterado" (boolean): Identifique se o resultado está alterado ou anormal em relação ao valor de referência. (Ex: cultura positiva, sorologia reagente para patógeno, ou valores numéricos fora da referência).
   - "detalhes" (string): Informações adicionais do exame, se houver (ex: antibiograma, observações do laudo, observações clínicas relevantes).

2. "valores_gasometria": Um objeto contendo valores numéricos dos parâmetros de gasometria (para cálculos matemáticos subsequentes), ou null se não houver ou se não for numérico:
   - "pH" (float ou null)
   - "pO2" (float ou null)
   - "pCO2" (float ou null)
   - "HCO3" (float ou null)
   - "BE" (float ou null)
   - "Sat O2" (float ou null)
   - "Na (gaso)" (float ou null)
   - "K (gaso)" (float ou null)
   - "Ca++" (float ou null)
   - "Cl" (float ou null)
   - "Glicose" (float ou null)
   - "Lactato" (float ou null)
   - "Ur" (float ou null)

3. "albumina_sugestao" (float ou null): se o exame de albumina sérica estiver presente no texto, extraia seu valor numérico aqui (ex: 3.6).

Texto do relatório de exames:
\"\"\"
{texto_pdf}
\"\"\"
"""

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "aistudio-build"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            
            candidates = res_json.get("candidates", [])
            if candidates:
                text_content = candidates[0].get("content", {}).get("parts", [])[0].get("text", "")
                return json.loads(text_content.strip())
    except urllib.error.HTTPError as e:
        print(f"Erro HTTP ao chamar o Gemini: {e.code} - {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"Erro inesperado ao chamar o Gemini: {e}")
        
    return None

def formatar_saida_gemini(exames_list):
    hoje = datetime.datetime.now().strftime("%d/%m/%Y")
    
    grouped = {}
    for ex in exames_list:
        mat = ex.get('material', 'OUTROS').upper().strip()
        if mat not in grouped:
            grouped[mat] = []
        grouped[mat].append(ex)
        
    html_parts = []
    # Order: SANGUE, URINA, LIQUOR, then others
    ordem_materiais = ['SANGUE', 'URINA', 'LIQUOR']
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
            valor = ex.get('valor')
            alterado = ex.get('alterado', False)
            
            cor = 'red' if alterado else 'black'
            fw = 'bold' if alterado else 'normal'
            span = f"<span style='color: {cor}; font-weight: {fw};'>{nome}: {valor}</span>"
            part_items.append(span)
            
        html_parts.append(f"<strong>{mat}</strong>: " + " | ".join(part_items))
        
    return f"({hoje}) - " + "<br>".join(html_parts)
