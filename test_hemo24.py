import re
from parser import processar_exames_geral, formatar_saida

texto = """
GASOMETRIA ARTERIAL
Material: SANGUE ARTERIAL
Método: ELETRODO SELETIVO
V.R.: Adultos:
 7.40 pH: 7,35 a 7,45
 81 mmHg pO2: 83 a 108 mmHg
 39 mmHg pCO2: 32 a 48 mmHg
 24.2 mmol/L HCO3: 21,0 a 28,0 mmol/L
 -0,6 mmol/L BEecf:
 -0.5 mmol/L BE: -2,0 a +2,0 mmol/L
 91.8 % Sat. O2: 95,0 A 99,0 %
 2.8 mmol/L K: 3,4 a 4,5 mmol/L
 140 mmol/L NA: 136 a 146 mmol/L
 1.09 mmol/L CA+: 1,15 a 1,29 mmol/L
 102 mmol/L CL: 98 a 106 mmol/L
 150 mg/dL Glicose: 70 a 105 mg/dL
 2.5 mmol/L Lactato: Menor que 1,3 mmol/L
"""
exames = processar_exames_geral(texto)
print(exames)
print(formatar_saida(exames))
