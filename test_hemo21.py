from parser import processar_exames_geral, formatar_saida
texto = """
GASOMETRIA ARTERIAL
Material: SANGUE ARTERIAL
Método: ELETRODO SELETIVO
V.R.: Adultos:
98.6 %Sat. O2: 95,0 A 99,0 %
3.1 mmol/LK: 3,4 a 4,5 mmol/L
140 mmol/LNA: 136 a 146 mmol/L
1.16 mmol/LCA+: 1,15 a 1,29 mmol/L
102 mmol/LCL: 98 a 106 mmol/L
102 mg/dLGlicose: 70 a 105 mg/dL
1.1 mmol/LLactato: Menor que 1,3 mmol/L
"""
exames = processar_exames_geral(texto)
print(formatar_saida(exames))
