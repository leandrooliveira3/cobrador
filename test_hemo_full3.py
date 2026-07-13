from parser import processar_exames_geral, formatar_saida
texto = """
URÉIA
Material: SANGUE
Método: COLORIMÉTRICO
RESULTADO: 46 mg/dL
VALORES DE REFERÊNCIA:
0 a 12 meses: 4 a 34 mg/dL
1 ano a 19 anos e 11 meses: 11 a 45 mg/dL
Homem maior de 19 anos: 19 a 43 mg/dL
Mulher maior de 19 anos: 15 a 36 mg/dL

CREATININA
Material: SANGUE
Método : CINÉTICO ENZIMÁTICO
RESULTADO: 0,43 mg/dL Valores de Referência:
0,66 a 1,25 mg/dl

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
98.6 %Sat. O2: 95,0 A 99,0 %
3.1 mmol/LK: 3,4 a 4,5 mmol/L
140 mmol/LNA: 136 a 146 mmol/L
1.16 mmol/LCA+: 1,15 a 1,29 mmol/L
102 mmol/LCL: 98 a 106 mmol/L
102 mg/dLGlicose: 70 a 105 mg/dL
1.1 mmol/LLactato: Menor que 1,3 mmol/L

PROTEÍNA C REATIVA (PCR)
Material: SANGUE
Método: IMUNOTURBIDIMETRIA
RESULTADO: 11,7 mg/L
VALOR DE REFERÊNCIA: < 5,00 mg/L

MAGNÉSIO
Material: SANGUE
Método: COLORIMÉTRICO
RESULTADO: 2,2 mg/dL V.R.: 1,6 a 2,3 mg/dL

FÓSFORO
Material: SANGUE
Método: COLORIMÉTRICO
RESULTADO: 3.05 mg/dL V.R.: 2,5 a 4,5 mg/dL

HEMOGRAMA
Material: SANGUE
Método: AUTOMATIZADO V.R. P/ IDADE E SEXO INFORMADOS
17,86 x 10³/μLLeucócitos: V.R.: 4,0 a 11,0 x 10³/μL
15,36 x 10³/μL 86,0 %Neutrófilos: V.R.: 2,0 a 7,0 x 10³/μL
1,2 %0,21 x 10³/μLEosinófilos: V.R.: 0,1 a 0,5 x 10³/μL
0,1 %0,02 x 10³/μLBasófilos: V.R.: 0,0 a 0,2 x 10³/μL
0,34 x 10³/μL 1,9 %Monócitos: V.R.: 0,2 a 1,0 x 10³/μL
1,93 x 10³/μL 10,8 %Linfócitos: V.R.: 1,0 a 3,5 x 10³/μL
2,71 milhões/μLHemácias: V.R.: 4,5 a 5,5 milhões/μL
8,9 g/dLHemoglobina: V.R.: 13,0 a 17,5 g/dL
26,2 %Hematócrito: V.R.: 40,0 a 50,0%
96,7 fLVCM: V.R.: 80,0 a 100,0 fL
32,8 pgHCM: V.R.: 26,0 a 32,0 pg
34,0 g/dLCHCM: V.R.: 32,0 a 36,0 g/dL
13.3 %RDW-CV: V.R.: 11,5 a 14,5%
360 x 10³/μLPlaquetas: V.R.: 150 a 450 x 10³/μL
10,8 fLVPM: V.R.: 7,4 a 12,0 fL
%IPF:
"""
exames = processar_exames_geral(texto)
print(formatar_saida(exames))
