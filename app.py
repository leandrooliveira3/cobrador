from flask import Flask, render_template, request, jsonify
import urllib.parse
from parser import processar_exames, formatar_saida
from gasometria import calcular_gasometria
from referencias import classificar_exames
from gemini_parser import chamar_gemini, formatar_saida_gemini

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    texto = request.form.get('texto', '')
    albumina_str = request.form.get('albumina', '4.0')
    
    try:
        albumina = float(albumina_str.replace(',', '.'))
    except ValueError:
        albumina = 4.0
        
    gemini_res = None
    # Tentamos usar o Gemini se a chave de API estiver configurada
    try:
        gemini_res = chamar_gemini(texto)
    except Exception as e:
        print(f"Erro ao executar parse do Gemini: {e}")
        
    if gemini_res and "exames" in gemini_res:
        exames_list = gemini_res["exames"]
        
        # Reconstrói os valores numéricos para o cálculo de gasometria matemática
        valores_gaso = gemini_res.get("valores_gasometria") or {}
        exames_gaso = {
            'pH': valores_gaso.get('pH'),
            'pCO2': valores_gaso.get('pCO2'),
            'HCO3': valores_gaso.get('HCO3'),
            'Na (gaso)': valores_gaso.get('Na (gaso)'),
            'K (gaso)': valores_gaso.get('K (gaso)'),
            'Cl': valores_gaso.get('Cl'),
            'Glicose': valores_gaso.get('Glicose'),
            'Ur': valores_gaso.get('Ur'),
        }
        
        # Sugestão inteligente de albumina se detectado e o usuário não recalculou explicitamente
        albumina_sugestao = gemini_res.get("albumina_sugestao")
        if albumina_str == '4.0' and albumina_sugestao is not None:
            albumina = albumina_sugestao
            
        albumina_encontrada = (albumina_sugestao is not None) or any(
            e.get('nome', '').lower() == 'albumina' for e in exames_list
        )
        
        linha_resumo = formatar_saida_gemini(exames_list)
        gasometria = calcular_gasometria(exames_gaso, albumina)
        alterados = [e for e in exames_list if e.get('alterado')]
    else:
        # Fallback para o analisador de expressões regulares (regex) atual
        exames = processar_exames(texto)
        exames_classificados = classificar_exames(exames)
        linha_resumo = formatar_saida(exames_classificados)
        gasometria = calcular_gasometria(exames, albumina)
        alterados = [e for e in exames_classificados.values() if e.get('alterado')]
        exames_list = list(exames_classificados.values())
        albumina_encontrada = 'Albumina' in exames_classificados
        
    grouped_exames = {}
    for ex in exames_list:
        mat = ex.get('material', 'OUTROS').upper().strip()
        if mat not in grouped_exames:
            grouped_exames[mat] = []
        grouped_exames[mat].append(ex)
        
    return render_template('resultado.html', 
                           linha_resumo=linha_resumo, 
                           gasometria=gasometria, 
                           alterados=alterados,
                           exames_list=exames_list,
                           grouped_exames=grouped_exames,
                           albumina_encontrada=albumina_encontrada,
                           albumina=albumina)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
