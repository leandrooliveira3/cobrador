from parser import processar_exames_geral, formatar_saida
texto = """
Material: SANGUE
Ur: 30.0
Cr: 0.99
Na: 139.0
K: 3.9
Cálcio Iônico: 1.2
CaT: 9.2
AST: 24.0
ALT: 17.0
GGT: 49.0
FA: 40.0
Albumina: 4.6
Lactato Desidrogenase: 198.0
PESQUISA DE ANTÍGENO CARCINOEMBRIONÁRIO (CEA): 13.0
CA 15.3: 41.0
FSH: 23.2
ESTRADIOL: 23.6
TEMPO E ATIVIDADE DE PROTROMBINA: <1,25
ATIVIDADE: 122.0%
RNI: 0.95
"""
exames = processar_exames_geral(texto)
print(formatar_saida(exames))
