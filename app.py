from flask import Flask, render_template, request, jsonify
import urllib.parse
from parser import processar_exames_geral, extrair_gasometria, formatar_saida
from gasometria import calcular_gasometria

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
        
    exames_list = processar_exames_geral(texto)
    linha_resumo = formatar_saida(exames_list)
    
    # Check if albumina is in the parsed exams to suggest replacing
    albumina_encontrada = any('albumina' in e.get('nome', '').lower() for e in exames_list)
    if albumina_encontrada and albumina_str == '4.0':
        for ex in exames_list:
            if 'albumina' in ex.get('nome', '').lower():
                try:
                    albumina = float(str(ex.get('valor')).split()[0].replace(',', '.'))
                except:
                    pass
    
    # Recalcular gasometria
    gaso = extrair_gasometria(texto)
    exames_gaso = {
        'pH': gaso.get('pH'),
        'pCO2': gaso.get('pCO2'),
        'HCO3': gaso.get('HCO3'),
        'Na (gaso)': gaso.get('Na'),
        'K (gaso)': gaso.get('K'),
        'Cl': gaso.get('Cl'),
        'Glicose': gaso.get('Glicose'),
        'Ur': gaso.get('Ur'),
    }
    gasometria = calcular_gasometria(exames_gaso, albumina)
    
    alterados = [e for e in exames_list if e.get('alterado')]
    
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
