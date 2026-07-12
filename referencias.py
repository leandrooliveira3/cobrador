
REFERENCIAS = {
    'Ur': {'min': 15, 'max': 45, 'material': 'SANGUE', 'ref_str': '15.0 - 45.0'},
    'Cr': {'min': 0.66, 'max': 1.25, 'material': 'SANGUE', 'ref_str': '0.66 - 1.25'},
    'PCR': {'min': 0, 'max': 5.0, 'material': 'SANGUE', 'ref_str': '< 5.0'},
    'AST': {'min': 15, 'max': 46, 'material': 'SANGUE', 'ref_str': '15 - 46'},
    'ALT': {'min': 0, 'max': 35, 'material': 'SANGUE', 'ref_str': '< 35'},
    'IST': {'min': 20, 'max': 50, 'material': 'SANGUE', 'ref_str': '20 - 50'},
    'TIBC': {'min': 265, 'max': 497, 'material': 'SANGUE', 'ref_str': '265 - 497'},
    'Ferro': {'min': 37, 'max': 170, 'material': 'SANGUE', 'ref_str': '37 - 170'},
    'VitD': {'min': 30, 'max': 100, 'material': 'SANGUE', 'ref_str': '30 - 100'},
    'C3': {'min': 88, 'max': 165, 'material': 'SANGUE', 'ref_str': '88 - 165'},
    'C4': {'min': 14, 'max': 44, 'material': 'SANGUE', 'ref_str': '14 - 44'},
    'Ferritina': {'min': 11, 'max': 264, 'material': 'SANGUE', 'ref_str': '11 - 264'},
    'Mg': {'min': 1.6, 'max': 2.3, 'material': 'SANGUE', 'ref_str': '1.6 - 2.3'},
    'P': {'min': 2.5, 'max': 4.5, 'material': 'SANGUE', 'ref_str': '2.5 - 4.5'},
    
    'Leucócitos': {'min': 4000, 'max': 11000, 'material': 'SANGUE', 'ref_str': '4000 - 11000'},
    'Neutrófilos': {'min': 2000, 'max': 7000, 'material': 'SANGUE', 'ref_str': '2000 - 7000'},
    'Eosinófilos': {'min': 100, 'max': 500, 'material': 'SANGUE', 'ref_str': '100 - 500'},
    'Basófilos': {'min': 0, 'max': 200, 'material': 'SANGUE', 'ref_str': '0 - 200'},
    'Monócitos': {'min': 200, 'max': 1000, 'material': 'SANGUE', 'ref_str': '200 - 1000'},
    'Linfócitos': {'min': 1000, 'max': 3500, 'material': 'SANGUE', 'ref_str': '1000 - 3500'},
    
    'Hemácias': {'min': 4.5, 'max': 5.5, 'material': 'SANGUE', 'ref_str': '4.5 - 5.5'},
    'Hb': {'min': 13.0, 'max': 17.5, 'material': 'SANGUE', 'ref_str': '13.0 - 17.5'},
    'Ht': {'min': 40.0, 'max': 50.0, 'material': 'SANGUE', 'ref_str': '40.0 - 50.0'},
    'VCM': {'min': 80.0, 'max': 100.0, 'material': 'SANGUE', 'ref_str': '80.0 - 100.0'},
    'HCM': {'min': 26.0, 'max': 32.0, 'material': 'SANGUE', 'ref_str': '26.0 - 32.0'},
    'CHCM': {'min': 32.0, 'max': 36.0, 'material': 'SANGUE', 'ref_str': '32.0 - 36.0'},
    'RDW': {'min': 11.5, 'max': 14.5, 'material': 'SANGUE', 'ref_str': '11.5 - 14.5'},
    'PLQ': {'min': 150000, 'max': 450000, 'material': 'SANGUE', 'ref_str': '150000 - 450000'},
    'Ret': {'min': 0.5, 'max': 1.8, 'material': 'SANGUE', 'ref_str': '0.5 - 1.8'},
    
    'pH': {'min': 7.35, 'max': 7.45, 'material': 'SANGUE ARTERIAL', 'ref_str': '7.35 - 7.45'},
    'pO2': {'min': 83, 'max': 108, 'material': 'SANGUE ARTERIAL', 'ref_str': '83 - 108'},
    'pCO2': {'min': 32, 'max': 48, 'material': 'SANGUE ARTERIAL', 'ref_str': '32 - 48'},
    'HCO3': {'min': 21.0, 'max': 28.0, 'material': 'SANGUE ARTERIAL', 'ref_str': '21.0 - 28.0'},
    'BE': {'min': -2.0, 'max': 2.0, 'material': 'SANGUE ARTERIAL', 'ref_str': '-2.0 a 2.0'},
    'Sat O2': {'min': 95.0, 'max': 99.0, 'material': 'SANGUE ARTERIAL', 'ref_str': '95.0 - 99.0'},
    'K (gaso)': {'min': 3.4, 'max': 4.5, 'material': 'SANGUE ARTERIAL', 'ref_str': '3.4 - 4.5'},
    'Na (gaso)': {'min': 136, 'max': 146, 'material': 'SANGUE ARTERIAL', 'ref_str': '136 - 146'},
    'Ca++': {'min': 1.15, 'max': 1.29, 'material': 'SANGUE ARTERIAL', 'ref_str': '1.15 - 1.29'},
    'Cl': {'min': 98, 'max': 106, 'material': 'SANGUE ARTERIAL', 'ref_str': '98 - 106'},
    'Glicose': {'min': 70, 'max': 105, 'material': 'SANGUE ARTERIAL', 'ref_str': '70 - 105'},
    'Lactato': {'min': 0, 'max': 1.3, 'material': 'SANGUE ARTERIAL', 'ref_str': '< 1.3'},
}

def classificar_exames(exames):
    resultado = {}
    for exame, valor in exames.items():
        ref = REFERENCIAS.get(exame)
        alterado = False
        ref_str = ""
        material = ""
        
        if ref:
            if valor < ref['min'] or valor > ref['max']:
                alterado = True
            ref_str = ref['ref_str']
            material = ref['material']
            
        resultado[exame] = {
            'nome': exame,
            'valor': valor,
            'alterado': alterado,
            'referencia': ref_str,
            'material': material
        }
    return resultado
