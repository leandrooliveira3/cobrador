import re
valor = "< 1,25 mEq"
m_val = re.search(r'([<>]?\s*-?\d+[\.,]?\d*)', valor)
if m_val:
    num_val = m_val.group(1).replace(',', '.').replace(' ', '')
    print(num_val)

valor2 = "122.0 %"
m_val2 = re.search(r'([<>]?\s*-?\d+[\.,]?\d*)', valor2)
if m_val2:
    num_val2 = m_val2.group(1).replace(',', '.').replace(' ', '')
    print(num_val2 + "%")
