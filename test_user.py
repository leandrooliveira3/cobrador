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
Leucócitos: 10480
Neutrófilos: 7980
Eosinófilos: 40
Basófilos: 0
Monócitos: 610
Linfócitos: 1850
Hemácias: 4.84
Hb: 13.9
Ht: 40.2%
VCM: 83.1
HCM: 28.8
CHCM: 34.6
RDW: 14.0%
PLQ: 210000
"""
exames = processar_exames_geral(texto)
print(formatar_saida(exames))

texto2 = """
Material: SANGUE
Ur: 25.0
Cr: 0.91
Na: 137.0
K: 4.5
Cálcio Iônico: 1.16
PCR: <5.00
AST: 23.0
ALT: 20.0
FA: 51.0
GGT: 28.0
BT: 0.5
BD: 0.09
BI: 0.41
TEMPO E ATIVIDADE DE PROTROMBINA: <1,25
ATIVIDADE: 122.0%
RNI: 0.95
Leucócitos: 7340
Neutrófilos: 5580
Eosinófilos: 50
Basófilos: 0
Monócitos: 520
Linfócitos: 1190
Hemácias: 4.51
Hb: 12.9
Ht: 38.3%
VCM: 84.9
HCM: 28.6
CHCM: 33.7
RDW: 17.8%
PLQ: 266000
"""
exames2 = processar_exames_geral(texto2)
print(formatar_saida(exames2))
