import re

linhas = """7.44pH: 7,35 a 7,45
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
""".split('\n')

for linha in linhas:
    linha = linha.strip()
    if not linha: continue
    
    m_kv = re.search(r'^([^:]+):\s*(.*)$', linha)
    if m_kv:
        left_part = m_kv.group(1).strip()
        right_part = m_kv.group(2).strip()
        
        # units pattern with possible missing space
        units_pattern = r'x\s*10³[/\\]?[μuµ]L|x\s*10\^3|milhões[/\\]?[μuµ]L|g/dL|mg/dL|mmol/L|mmHg|fL|pg|%|/campo|/mm³|U/L|mg/L'
        
        # Match <NUMBER> [UNIT] [%] [NUMBER] [UNIT] <NAME>
        # To handle missing space, we can specify that the name starts with a capital letter, or we match known names.
        # It's easier to just match the units optionally, and the remainder is the name.
        m_val_name = re.search(rf'^([0-9][\d\,\.\s]*(?:{units_pattern})?(?:[\d\,\.\s]*(?:{units_pattern})?)?)\s*([A-ZÀ-Ÿa-z].*)$', left_part)
        
        if m_val_name:
            valor = m_val_name.group(1).strip()
            nome = m_val_name.group(2).strip()
            print(f"[{valor}] - [{nome}]")
        else:
            print(f"FAILED left_part split: {left_part}")
    else:
        print(f"FAILED: {linha}")
