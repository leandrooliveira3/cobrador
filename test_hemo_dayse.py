import re
from parser import processar_exames_geral, formatar_saida, extrair_gasometria
from gasometria import calcular_gasometria

texto = """
HOSPITAL DAS CLÍNICAS DA UNIVERSIDADE FEDERAL DE MINAS GERAIS
UNIDADE LABORATORIAL DE ANÁLISES CLÍNICAS
Emissão: 14/07/2026 às 07:50 Fl.: 1
Cliente: DAYSE MARIA COELHO NASCIMENTO (2309904) NPF: 230260
Dt. Nasc: 29/01/1971 RG: MG 6.350.815
Médico.: ANA PAULA CAMARGOS DE FIGUEIREDO NEVES
Clínica: 3 ANDAR - LESTE - CTI ADULTO
Origem.: COLETA HOSPITALAR HC - Leito NPF 230260/0308-L Pedido: 38698048
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:26
URÉIA
Material: SANGUE
Método: COLORIMÉTRICO
RESULTADO: 51 mg/dL
VALORES DE REFERÊNCIA:
0 a 12 meses: 4 a 34 mg/dL
1 ano a 19 anos e 11 meses: 11 a 45 mg/dL
Homem maior de 19 anos: 19 a 43 mg/dL
Mulher maior de 19 anos: 15 a 36 mg/dL
Liberado por: ANTONIO FELIPE SILVA CARVALHO - CRF-MG-41590
 ---------------------------------------------------------------------------
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:12
CREATININA
Material: SANGUE
Método : CINÉTICO ENZIMÁTICO
RESULTADO: 1,05 mg/dL Valores de Referência:
0,52 a 1,04 mg/dl
- O uso recente de dipirona pode ocasionar discreta redução nos níveis
 de creatinina dosada.
RITMO DE FILTRAÇÃO GLOMERULAR - CALCULADO PELA FÓRMULA CKD-EPI
Resultado Afrodescendente : 65,95 mL/min/1,73 m²
Resultado Não Afrodescendente : 54,41 mL/min/1,73 m²
Valor de Referência: Adulto maior de 18 anos: Superior a 90 mL/min/1,73 m²
Nota: Não usar a estimativa de ritmo de filtração glomerular pelo CKD-EPI para ajustar dose
de medicamento. Interpretar com cautela os valores obtidos em indivíduos com concentrações
flutuantes de creatinina sérica, pacientes hospitalizados, especialmente com insuficiência
renal aguda, gestantes, pessoas com extremos de massa muscular como paraplégicos, obesos
fisioculturistas, desnutridos e outros.
Referência bibliográfica: Levey, AS et al. A New Equation to Estimate Glomerular Filtration
Rate. Ann Intern Med 150:60-612,2009.
Liberado por: SHINFAY MAXIMILIAN LIU - CRM-MG 43.316
RESPONSÁVEIS TÉCNICOS
Dra. Denise Carceroni Cotta Iwashima CRM-MG 41.113 | Dr. Shinfay Maximilian Liu CRM-MG 43.316
HOSPITAL DAS CLÍNICAS DA UFMG - CRM-MG 2.946. Av. Prof. Alfredo Balena, 110 - Santa Efigênia, Belo Horizonte - MG
CEP: 30.130-100 - Fones: (31) 3307-9600 | 9601 - CNPJ: 17217985003472 - CNES: 0027049
HOSPITAL DAS CLÍNICAS DA UNIVERSIDADE FEDERAL DE MINAS GERAIS
UNIDADE LABORATORIAL DE ANÁLISES CLÍNICAS
Emissão: 14/07/2026 às 07:50 Fl.: 2
Cliente: DAYSE MARIA COELHO NASCIMENTO (2309904) NPF: 230260
Dt. Nasc: 29/01/1971 RG: MG 6.350.815
Médico.: ANA PAULA CAMARGOS DE FIGUEIREDO NEVES
Clínica: 3 ANDAR - LESTE - CTI ADULTO
Origem.: COLETA HOSPITALAR HC - Leito NPF 230260/0308-L Pedido: 38698048
 Coleta confirmada: 14/07/2026 04:57 Liberação:14/07/2026 05:20
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
Liberado por: GUSTAVO HENRIQUE CASTANHEIRA PEREIRA - CRF-MG-13849
RESPONSÁVEIS TÉCNICOS
Dra. Denise Carceroni Cotta Iwashima CRM-MG 41.113 | Dr. Shinfay Maximilian Liu CRM-MG 43.316
HOSPITAL DAS CLÍNICAS DA UFMG - CRM-MG 2.946. Av. Prof. Alfredo Balena, 110 - Santa Efigênia, Belo Horizonte - MG
CEP: 30.130-100 - Fones: (31) 3307-9600 | 9601 - CNPJ: 17217985003472 - CNES: 0027049
HOSPITAL DAS CLÍNICAS DA UNIVERSIDADE FEDERAL DE MINAS GERAIS
UNIDADE LABORATORIAL DE ANÁLISES CLÍNICAS
Emissão: 14/07/2026 às 07:50 Fl.: 3
Cliente: DAYSE MARIA COELHO NASCIMENTO (2309904) NPF: 230260
Dt. Nasc: 29/01/1971 RG: MG 6.350.815
Médico.: ANA PAULA CAMARGOS DE FIGUEIREDO NEVES
Clínica: 3 ANDAR - LESTE - CTI ADULTO
Origem.: COLETA HOSPITALAR HC - Leito NPF 230260/0308-L Pedido: 38698048
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:31
PROTEÍNA C REATIVA (PCR)
Material: SANGUE
Método: IMUNOTURBIDIMETRIA
RESULTADO: 124,5 mg/L
VALOR DE REFERÊNCIA: < 5,00 mg/L
Uma medida inicial e isolada da PCR pode ajudar no diagnóstico de
condições inflamatórias agudas e crônicas porém, medidas repetidas, com
intervalos de tempo baseados na condição clínica do paciente, são úteis
para o acompanhamento da evolução da doença e/ou da resposta ao
tratamento.
Liberado por: ANTONIO FELIPE SILVA CARVALHO - CRF-MG-41590
 ---------------------------------------------------------------------------
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:27
MAGNÉSIO
Material: SANGUE
Método: COLORIMÉTRICO
RESULTADO: 2,2 mg/dL V.R.: 1,6 a 2,3 mg/dL
Liberado por: SHINFAY MAXIMILIAN LIU - CRM-MG 43.316
 ---------------------------------------------------------------------------
RESPONSÁVEIS TÉCNICOS
Dra. Denise Carceroni Cotta Iwashima CRM-MG 41.113 | Dr. Shinfay Maximilian Liu CRM-MG 43.316
HOSPITAL DAS CLÍNICAS DA UFMG - CRM-MG 2.946. Av. Prof. Alfredo Balena, 110 - Santa Efigênia, Belo Horizonte - MG
CEP: 30.130-100 - Fones: (31) 3307-9600 | 9601 - CNPJ: 17217985003472 - CNES: 0027049
HOSPITAL DAS CLÍNICAS DA UNIVERSIDADE FEDERAL DE MINAS GERAIS
UNIDADE LABORATORIAL DE ANÁLISES CLÍNICAS
Emissão: 14/07/2026 às 07:50 Fl.: 4
Cliente: DAYSE MARIA COELHO NASCIMENTO (2309904) NPF: 230260
Dt. Nasc: 29/01/1971 RG: MG 6.350.815
Médico.: ANA PAULA CAMARGOS DE FIGUEIREDO NEVES
Clínica: 3 ANDAR - LESTE - CTI ADULTO
Origem.: COLETA HOSPITALAR HC - Leito NPF 230260/0308-L Pedido: 38698048
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:27
TRIGLICÉRIDES
Material: SANGUE
Método: COLORIMÉTRICO
TEMPO DE JEJUM:
RESULTADO: 196 mg/dL
Valores de referência:
Com jejum de 12 horas: < 150 mg/dL
Sem jejum de 12 horas: < 175 mg/dL
Observação: valores recomendados pelo Consenso Brasileiro para a Normatização
da Determinação Laboratorial do Perfil Lipídico
Liberado por: SHINFAY MAXIMILIAN LIU - CRM-MG 43.316
 ---------------------------------------------------------------------------
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:26
ALBUMINA
Material: SANGUE
Método: COLORIMÉTRICO
RESULTADO: 2.2 g/dL V.R.: 3,5 a 5,0 g/dL
Liberado por: ANTONIO FELIPE SILVA CARVALHO - CRF-MG-41590
 ---------------------------------------------------------------------------
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:31
FÓSFORO
Material: SANGUE
Método: COLORIMÉTRICO
RESULTADO: 2.63 mg/dL V.R.: 2,5 a 4,5 mg/dL
Liberado por: ANTONIO FELIPE SILVA CARVALHO - CRF-MG-41590
RESPONSÁVEIS TÉCNICOS
Dra. Denise Carceroni Cotta Iwashima CRM-MG 41.113 | Dr. Shinfay Maximilian Liu CRM-MG 43.316
HOSPITAL DAS CLÍNICAS DA UFMG - CRM-MG 2.946. Av. Prof. Alfredo Balena, 110 - Santa Efigênia, Belo Horizonte - MG
CEP: 30.130-100 - Fones: (31) 3307-9600 | 9601 - CNPJ: 17217985003472 - CNES: 0027049
HOSPITAL DAS CLÍNICAS DA UNIVERSIDADE FEDERAL DE MINAS GERAIS
UNIDADE LABORATORIAL DE ANÁLISES CLÍNICAS
Emissão: 14/07/2026 às 07:50 Fl.: 5
Cliente: DAYSE MARIA COELHO NASCIMENTO (2309904) NPF: 230260
Dt. Nasc: 29/01/1971 RG: MG 6.350.815
Médico.: ANA PAULA CAMARGOS DE FIGUEIREDO NEVES
Clínica: 3 ANDAR - LESTE - CTI ADULTO
Origem.: COLETA HOSPITALAR HC - Leito NPF 230260/0308-L Pedido: 38698048
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:26
ALANINO AMINOTRANSFERASE (ALT)
Material: SANGUE
Método: CINÉTICO ENZIMÁTICO
RESULTADO: 18 U/L V.R.: < 35 U/L
Liberado por: ANTONIO FELIPE SILVA CARVALHO - CRF-MG-41590
 ---------------------------------------------------------------------------
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:31
ASPARTATO AMINOTRANSFERASE (AST)
Material: SANGUE
Método: CINÉTICO ENZIMÁTICO
RESULTADO: 59 U/L V.R.: 15 a 46 U/L
Liberado por: ANTONIO FELIPE SILVA CARVALHO - CRF-MG-41590
 ---------------------------------------------------------------------------
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:31
FOSFATASE ALCALINA
Material: SANGUE
Método: CINÉTICO ENZIMÁTICO
RESULTADO: 134 U/L VALORES DE REFERÊNCIA:
0 a 9 anos: 55 a 425 U/L
10 a 15 anos: 130 a 560 U/L
15 a 19 anos: 70 a 525 U/L
Adultos: 38 a 126 U/L
Liberado por: ANTONIO FELIPE SILVA CARVALHO - CRF-MG-41590
RESPONSÁVEIS TÉCNICOS
Dra. Denise Carceroni Cotta Iwashima CRM-MG 41.113 | Dr. Shinfay Maximilian Liu CRM-MG 43.316
HOSPITAL DAS CLÍNICAS DA UFMG - CRM-MG 2.946. Av. Prof. Alfredo Balena, 110 - Santa Efigênia, Belo Horizonte - MG
CEP: 30.130-100 - Fones: (31) 3307-9600 | 9601 - CNPJ: 17217985003472 - CNES: 0027049
HOSPITAL DAS CLÍNICAS DA UNIVERSIDADE FEDERAL DE MINAS GERAIS
UNIDADE LABORATORIAL DE ANÁLISES CLÍNICAS
Emissão: 14/07/2026 às 07:50 Fl.: 6
Cliente: DAYSE MARIA COELHO NASCIMENTO (2309904) NPF: 230260
Dt. Nasc: 29/01/1971 RG: MG 6.350.815
Médico.: ANA PAULA CAMARGOS DE FIGUEIREDO NEVES
Clínica: 3 ANDAR - LESTE - CTI ADULTO
Origem.: COLETA HOSPITALAR HC - Leito NPF 230260/0308-L Pedido: 38698048
 Coleta confirmada: 14/07/2026 05:01 Liberação:14/07/2026 07:12
GAMA-GLUTAMILTRANSFERASE (GGT)
Material: SANGUE
Método: CINÉTICO ENZIMÁTICO
RESULTADO: 40 U/L
VALORES DE REFERÊNCIA:
0 a 6 meses: 10 a 183 U/L
7 meses a 19 anos e 11 meses: 6 a 44 U/L
Homens maiores de 19 anos: 15 a 73 U/L
Mulheres maiores de 19 anos: 12 a 43 U/L
Liberado por: DENISE CARCERONI COTTA IWASHIMA - CRM-MG-41113
 ---------------------------------------------------------------------------
 Coleta confirmada: 14/07/2026 05:02 Liberação:14/07/2026 06:35
BILIRRUBINAS
Material: SANGUE
Método: COLORIMÉTRICO
Bilirrubina total: 1.07 mg/dL V.R.: 0,2 a 1,3 mg/dL
Bilirrubina direta: 0.60 mg/dL V.R.: 0,0 a 0,3 mg/dL
Bilirrubina indireta: 0.47 mg/dL V.R.: 0,0 a 1,1 mg/dL
Liberado por: GUSTAVO HENRIQUE CASTANHEIRA PEREIRA - CRF-MG-13849
 ---------------------------------------------------------------------------
RESPONSÁVEIS TÉCNICOS
Dra. Denise Carceroni Cotta Iwashima CRM-MG 41.113 | Dr. Shinfay Maximilian Liu CRM-MG 43.316
HOSPITAL DAS CLÍNICAS DA UFMG - CRM-MG 2.946. Av. Prof. Alfredo Balena, 110 - Santa Efigênia, Belo Horizonte - MG
CEP: 30.130-100 - Fones: (31) 3307-9600 | 9601 - CNPJ: 17217985003472 - CNES: 0027049
HOSPITAL DAS CLÍNICAS DA UNIVERSIDADE FEDERAL DE MINAS GERAIS
UNIDADE LABORATORIAL DE ANÁLISES CLÍNICAS
Emissão: 14/07/2026 às 07:50 Fl.: 7
Cliente: DAYSE MARIA COELHO NASCIMENTO (2309904) NPF: 230260
Dt. Nasc: 29/01/1971 RG: MG 6.350.815
Médico.: ANA PAULA CAMARGOS DE FIGUEIREDO NEVES
Clínica: 3 ANDAR - LESTE - CTI ADULTO
Origem.: COLETA HOSPITALAR HC - Leito NPF 230260/0308-L Pedido: 38698048
 Coleta confirmada: 14/07/2026 04:59 Liberação:14/07/2026 06:35
HEMOGRAMA
Material: SANGUE
Método: AUTOMATIZADO
V.R. P/ IDADE E SEXO INFORMADOS
 52,03 x 10³/µL Leucócitos: V.R.: 4,0 a 11,0 x 10³/µL
 47,82 x 10³/µL 91,9 % Neutrófilos: V.R.: 2,0 a 7,0 x 10³/µL
 0,0 % 0,00 x 10³/µL Eosinófilos: V.R.: 0,1 a 0,5 x 10³/µL
 0,2 % 0,10 x 10³/µL Basófilos: V.R.: 0,0 a 0,2 x 10³/µL
 2,24 x 10³/µL 4,3 % Monócitos: V.R.: 0,2 a 1,0 x 10³/µL
 1,87 x 10³/µL 3,6 % Linfócitos: V.R.: 1,0 a 3,5 x 10³/µL
 2,35 milhões/µL Hemácias: V.R.: 3,8 a 4,8 milhões/µL
 6,0 g/dL Hemoglobina: V.R.: 12,0 a 16,0 g/dL
 18,5 % Hematócrito: V.R.: 36,0 a 46,0%
 78,7 fL VCM: V.R.: 80,0 a 100,0 fL
 25,5 pg HCM: V.R.: 26,0 a 32,0 pg
 32,4 g/dL CHCM: V.R.: 32,0 a 36,0 g/dL
 18.4 % RDW-CV: V.R.: 11,5 a 14,5%
 531 x 10³/µL Plaquetas: V.R.: 150 a 450 x 10³/µL
 11,7 fL VPM: V.R.: 7,4 a 12,0 fL
 % IPF:
Liberado por: GUSTAVO HENRIQUE CASTANHEIRA PEREIRA - CRF-MG-13849
RESPONSÁVEIS TÉCNICOS
Dra. Denise Carceroni Cotta Iwashima CRM-MG 41.113 | Dr. Shinfay Maximilian Liu CRM-MG 43.316
HOSPITAL DAS CLÍNICAS DA UFMG - CRM-MG 2.946. Av. Prof. Alfredo Balena, 110 - Santa Efigênia, Belo Horizonte - MG
CEP: 30.130-100 - Fones: (31) 3307-9600 | 9601 - CNPJ: 17217985003472 - CNES: 0027049
HOSPITAL DAS CLÍNICAS DA UNIVERSIDADE FEDERAL DE MINAS GERAIS
UNIDADE LABORATORIAL DE ANÁLISES CLÍNICAS
Emissão: 14/07/2026 às 07:50 Fl.: 8
Cliente: DAYSE MARIA COELHO NASCIMENTO (2309904) NPF: 230260
Dt. Nasc: 29/01/1971 RG: MG 6.350.815
Médico.: ANA PAULA CAMARGOS DE FIGUEIREDO NEVES
Clínica: 3 ANDAR - LESTE - CTI ADULTO
Origem.: COLETA HOSPITALAR HC - Leito NPF 230260/0308-L Pedido: 38698048
 Coleta confirmada: 14/07/2026 05:00 Liberação:14/07/2026 06:19
TEMPO DE PROTROMBINA
Material: Plasma Citratado
Método: Coagulométrico Automatizado
Valores de referência
Paciente: 20,2 segundos 9,4 a 12,5 segundos
RNI : 1,75 0,9 até 1,1
Controle: 11.5 segundos
Nota: A Atividade de protrombina não se correlaciona de forma linear com o
tempo de coagulação do ensaio. As variações da atividade, portanto, não se
comportam da mesma forma em indivíduos não anticoagulados e em pacientes
em uso de antagonistas da vitamina K (AVKs). Desta forma, sugerimos o uso
do RNI para monitorização dos pacientes anticoagulados com AVK e tempo de
coagulação para avaliação das demais indicações.
Liberado por: TALLES GUILHERME ALMEIDA CASTRO - CRM-MG-63865
RESPONSÁVEIS TÉCNICOS
Dra. Denise Carceroni Cotta Iwashima CRM-MG 41.113 | Dr. Shinfay Maximilian Liu CRM-MG 43.316
HOSPITAL DAS CLÍNICAS DA UFMG - CRM-MG 2.946. Av. Prof. Alfredo Balena, 110 - Santa Efigênia, Belo Horizonte - MG
CEP: 30.130-100 - Fones: (31) 3307-9600 | 9601 - CNPJ: 17217985003472 - CNES: 0027049
"""
exames = processar_exames_geral(texto)
print(formatar_saida(exames))
