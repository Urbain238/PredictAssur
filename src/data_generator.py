import pandas as pd
import random
import os

def generer_donnees_initiales(chemin_fichier, n=100):
    regions_villes = {
        "Littoral": ["Douala", "Edéa", "Nkongsamba"],
        "Centre": ["Yaoundé", "Mbalmayo", "Bafia"],
        "Ouest": ["Bafoussam", "Dschang", "Foumban"],
        "Sud": ["Kribi", "Ebolowa"],
        "Nord": ["Garoua", "Guider"],
        "Est": ["Bertoua", "Batouri"],
        "Adamaoua": ["Ngaoundéré"],
        "Extrême-Nord": ["Maroua", "Yagoua"],
        "Nord-Ouest": ["Bamenda", "Kumbo"],
        "Sud-Ouest": ["Buea", "Limbe"]
    }
    
    secteurs_professions = {
        "Public": ["Enseignant", "Infirmier", "Cadre administratif", "Policier"],
        "Privé Formel": ["Comptable", "Ingénieur", "Technicien", "Chauffeur livreur"],
        "Informel (Commerçant/Artisan)": ["Bayam-sellam", "Call-boxeur", "Menuisier", "Couturier"],
        "Agriculteur": ["Planteur de cacao", "Maraîcher", "Éleveur"],
        "Étudiant": ["Étudiant en droit", "Étudiant en médecine", "Élève ingénieur"],
        "Libéral": ["Avocat", "Médecin", "Consultant"],
        "Sans emploi": ["Chômeur", "Mère au foyer"]
    }

    # Intervalles de revenus exacts
    intervalles_revenus = ["Moins de 50 000 FCFA", "50 000 - 150 000 FCFA", "150 000 - 300 000 FCFA", "Plus de 300 000 FCFA"]

    data = []
    for _ in range(n):
        # --- 👤 Profil & Localisation ---
        sexe = random.choice(["Masculin", "Féminin"])
        age = random.randint(18, 65)
        
        region = random.choices(list(regions_villes.keys()), weights=[0.25, 0.25, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1], k=1)[0]
        ville = random.choice(regions_villes[region])
        secteur = random.choices(list(secteurs_professions.keys()), weights=[0.1, 0.15, 0.4, 0.15, 0.1, 0.05, 0.05], k=1)[0]
        
        # Revenus mensuels par intervalle selon le secteur
        if secteur in ["Public", "Privé Formel", "Libéral"]:
            revenu = random.choices(intervalles_revenus, weights=[0.05, 0.25, 0.4, 0.3], k=1)[0]
        elif secteur in ["Étudiant", "Sans emploi"]:
            revenu = random.choices(intervalles_revenus, weights=[0.8, 0.2, 0.0, 0.0], k=1)[0]
        else:
            revenu = random.choices(intervalles_revenus, weights=[0.4, 0.4, 0.15, 0.05], k=1)[0]

        # --- 🧠 Perception & Confiance ---
        connaissance = random.choices(["Nulle", "Faible", "Moyenne", "Bonne", "Expert"], weights=[0.3, 0.3, 0.2, 0.15, 0.05], k=1)[0]
        confiance = random.randint(0, 10) if connaissance != "Nulle" else random.randint(0, 4)
        
        if connaissance in ["Nulle", "Faible"]:
            perception = random.choices(["Une charge", "Une obligation"], weights=[0.8, 0.2], k=1)[0]
        else:
            perception = random.choices(["Nécessaire", "Une obligation", "Une charge"], weights=[0.6, 0.3, 0.1], k=1)[0]

        choix_barrieres = ["Méfiance", "Coût élevé", "Lenteur administrative", "Manque d'info", "Religion"]
        if perception == "Une charge":
            barriere = random.choices(choix_barrieres, weights=[0.3, 0.4, 0.1, 0.1, 0.1], k=1)[0]
        else:
            barriere = random.choices(choix_barrieres, weights=[0.2, 0.3, 0.3, 0.15, 0.05], k=1)[0]

        # --- 🛡️ Habitudes & Digitalisation ---
        if perception == "Une charge":
            assurances_possedees = "Aucune"
        else:
            assurances_possedees = random.choices(["Aucune", "Santé", "Auto", "Santé, Vie/Décès", "Auto, Santé"], weights=[0.4, 0.2, 0.2, 0.1, 0.1], k=1)[0]
            
        canal = random.choice(["Agent physique", "Courtier", "Banque", "App mobile"])
        
        if assurances_possedees == "Aucune":
            sinistre_non_rembourse = "Jamais eu de sinistre"
        else:
            sinistre_non_rembourse = random.choices(["Jamais eu de sinistre", "Non", "Oui"], weights=[0.6, 0.3, 0.1], k=1)[0]
            
        if age < 30:
            pret_digital = random.randint(6, 10)
        elif age < 45:
            pret_digital = random.randint(3, 8)
        else:
            pret_digital = random.randint(0, 5)
            
        mobile_money = random.choices(["Régulier (Orange/MTN Money)", "Occasionnel", "Jamais"], weights=[0.75, 0.20, 0.05], k=1)[0]

        data.append({
            "Sexe": sexe,
            "Âge": age,
            "Région": region,
            "Ville": ville,
            "Secteur_Activite": secteur,
            "Revenu_Mensuel": revenu,
            "Perception_Assurance": perception,
            "Niveau_Connaissance": connaissance,
            "Niveau_Confiance": confiance,
            "Barriere_Principale": barriere,
            "Assurances_Possedees": assurances_possedees,
            "Canal_Prefere": canal,
            "Sinistre_Non_Rembourse": sinistre_non_rembourse,
            "Pret_Digital_Score": pret_digital,
            "Utilisation_Mobile_Money": mobile_money
        })
    
    df = pd.DataFrame(data)
    df.to_csv(chemin_fichier, index=False)
    return df

def charger_donnees(chemin_fichier="data/raw/sondage_assurance.csv"):
    os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)
    if not os.path.exists(chemin_fichier):
        return generer_donnees_initiales(chemin_fichier, n=200)
    else:
        return pd.read_csv(chemin_fichier)