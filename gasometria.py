def calcular_gasometria(exames, albumina=4.0):
    ph = exames.get('pH')
    pco2 = exames.get('pCO2')
    hco3 = exames.get('HCO3')
    na = exames.get('Na (gaso)')
    k = exames.get('K (gaso)')
    cl = exames.get('Cl')
    glicose = exames.get('Glicose')
    ur = exames.get('Ur')
    
    if ph is None or pco2 is None or hco3 is None:
        return None

    # Distúrbio Primário
    disturbio = "Normal"
    if ph < 7.35:
        if pco2 > 45:
            disturbio = "Acidose Respiratória"
        elif hco3 < 22:
            disturbio = "Acidose Metabólica"
    elif ph > 7.45:
        if pco2 < 35:
            disturbio = "Alcalose Respiratória"
        elif hco3 > 26:
            disturbio = "Alcalose Metabólica"
    else:
        # pH normal, pode ser misto se pco2 e hco3 anormais
        if pco2 > 45 and hco3 > 26:
            disturbio = "Distúrbio compensado ou misto"
        elif pco2 < 35 and hco3 < 22:
            disturbio = "Distúrbio compensado ou misto"
            
    # Ânion Gap = Na - (Cl + HCO3)
    anion_gap = None
    anion_gap_corrigido = None
    interpretacao_ag = "-"
    if na is not None and cl is not None and hco3 is not None:
        anion_gap = na - (cl + hco3)
        # Correção pela albumina: AG + 2.5 * (4.0 - albumina)
        anion_gap_corrigido = anion_gap + 2.5 * (4.0 - albumina)
        
        if anion_gap_corrigido > 12:
            interpretacao_ag = "Aumentado"
        elif anion_gap_corrigido < 8:
            interpretacao_ag = "Reduzido"
        else:
            interpretacao_ag = "Normal"

    # Osmolaridade calculada = 2*Na + Glicose/18 + Ur/6
    osmolaridade = None
    interpretacao_osm = "-"
    if na is not None and glicose is not None and ur is not None:
        osmolaridade = 2 * na + (glicose / 18.0) + (ur / 6.0)
        
        if osmolaridade > 295:
            interpretacao_osm = "Hiperosmolaridade"
        elif osmolaridade < 275:
            interpretacao_osm = "Hipo-osmolaridade"
        else:
            interpretacao_osm = "Normal"

    return {
        'disturbio': disturbio,
        'anion_gap': anion_gap,
        'anion_gap_corrigido': anion_gap_corrigido,
        'interpretacao_ag': interpretacao_ag,
        'osmolaridade': osmolaridade,
        'interpretacao_osm': interpretacao_osm
    }
