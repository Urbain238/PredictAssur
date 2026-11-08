import math

def calculer_prime_pure_sante(age: int, region: str) -> float:
    """
    Calcule la prime pure annuelle (en FCFA) pour une assurance santé de base.
    Prime Pure = Fréquence de base * Coût moyen de base * Facteurs de risque
    """
    # 1. Hypothèses de base (statistiques fictives pour l'exemple)
    frequence_base = 0.35  # Probabilité d'avoir recours aux soins dans l'année (35%)
    cout_moyen_base = 150000  # Coût moyen d'un sinistre santé de base en FCFA

    # 2. Facteur de risque lié à l'âge
    # Exemple : On considère que le risque optimal est autour de 20-25 ans. 
    # Pour chaque année au-dessus de 25 ans, le risque augmente de 1.5%.
    if age <= 25:
        facteur_age = 1.0
    else:
        facteur_age = 1.0 + ((age - 25) * 0.015)
        
    # Majoration supplémentaire pour les seniors (+ de 60 ans)
    if age >= 60:
        facteur_age += 0.20

    # 3. Facteur de risque lié à la région (Coût de la vie et des infrastructures médicales)
    # Yaoundé (Centre) et Douala (Littoral) ont des cliniques plus chères.
    facteurs_region = {
        "Littoral": 1.25,   # +25% de coût
        "Centre": 1.20,     # +20% de coût
        "Ouest": 1.10,
        "Sud-Ouest": 1.10,
        "Nord-Ouest": 1.10,
        "Sud": 1.05,
        "Est": 1.0,
        "Adamaoua": 1.0,
        "Nord": 0.95,       # Infrastructures moins coûteuses
        "Extrême-Nord": 0.95
    }
    
    # Récupérer le facteur de la région (1.0 par défaut si région inconnue)
    facteur_region = facteurs_region.get(region, 1.0)

    # 4. Calcul final de la prime pure
    prime_pure = frequence_base * cout_moyen_base * facteur_age * facteur_region
    
    # Arrondir à la centaine de FCFA supérieure pour des montants commerciaux "propres"
    prime_pure_arrondie = math.ceil(prime_pure / 100) * 100

    return prime_pure_arrondie

def calculer_prime_commerciale(prime_pure: float, taux_chargement: float = 0.25, taxe_assurance: float = 0.1925) -> float:
    """
    Calcule la prime commerciale TTC (ce que le client paie réellement).
    - taux_chargement : Frais de gestion, commissions des courtiers, marge bénéficiaire.
    - taxe_assurance : TVA ou Taxe Spéciale sur les Contrats d'Assurance (TSCA).
    """
    prime_nette = prime_pure * (1 + taux_chargement)
    prime_ttc = prime_nette * (1 + taxe_assurance)
    
    return round(prime_ttc, 0)