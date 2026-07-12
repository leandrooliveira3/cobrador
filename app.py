from flask import Flask, render_template, request, jsonify
import urllib.parse
from parser import processar_exames, formatar_saida
from gasometria import calcular_gasometria
from referencias import classificar_exames

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
        
    exames = processar_exames(texto)
    exames_classificados = classificar_exames(exames)
    linha_resumo = formatar_saida(exames_classificados)
    gasometria = calcular_gasometria(exames, albumina)
    alterados = [e for e in exames_classificados.values() if e.get('alterado')]
    
    return render_template('resultado.html', 
                           linha_resumo=linha_resumo, 
                           gasometria=gasometria, 
                           alterados=alterados,
                           exames_classificados=exames_classificados,
                           albumina=albumina)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
