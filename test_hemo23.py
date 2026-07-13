from parser import processar_exames_geral, formatar_saida
texto = """
HEMOGRAMA
Material: SANGUE
Método: AUTOMATIZADO V.R. P/ IDADE E SEXO INFORMADOS
%IPF:
"""
exames = processar_exames_geral(texto)
print(exames)
