from parser import processar_exames_geral, formatar_saida
texto = """
HEMOGRAMA
Material: SANGUE
Método: AUTOMATIZADO V.R. P/ IDADE E SEXO INFORMADOS
17,86 x 10³/μLLeucócitos: V.R.: 4,0 a 11,0 x 10³/μL
15,36 x 10³/μL 86,0 %Neutrófilos: V.R.: 2,0 a 7,0 x 10³/μL
1,2 %0,21 x 10³/μLEosinófilos: V.R.: 0,1 a 0,5 x 10³/μL

GASOMETRIA ARTERIAL
Material: SANGUE ARTERIAL
Método: ELETRODO SELETIVO
V.R.: Adultos:
7.44pH: 7,35 a 7,45
103 mmHgpO2: 83 a 108 mmHg
44 mmHgpCO2: 32 a 48 mmHg
29.9 mmol/LHCO3: 21,0 a 28,0 mmol/L
5,7 mmol/LBEecf:
5.2 mmol/LBE: -2,0 a +2,0 mmol/L
"""
exames = processar_exames_geral(texto)
print(formatar_saida(exames))
