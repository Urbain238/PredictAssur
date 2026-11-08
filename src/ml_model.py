# src/ml_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def preparer_et_entrainer(df):
    """
    Entraîne le modèle Random Forest sur les données fournies.
    Retourne le modèle, le dictionnaire d'encodeurs et la liste des features.
    """
    features = ["Âge", "Sexe", "Région", "Secteur_Activite", "Revenu_Mensuel", "Niveau_Confiance"]
    df_ml = df.dropna(subset=features + ["Pret_Digital_Score"]).copy()
    
    # Cible : Hautement Digital si score >= 7
    y = (df_ml["Pret_Digital_Score"] >= 7).astype(int)
    
    encoders = {}
    X = df_ml[features].copy()
    colonnes_categoriques = ["Sexe", "Région", "Secteur_Activite", "Revenu_Mensuel"]
    
    for col in colonnes_categoriques:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le

    modele_rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    modele_rf.fit(X, y)
    
    return modele_rf, encoders, features

def detecter_personas(df):
    """
    Analyse les données pour extraire les profils ayant la plus forte 
    et la plus faible appétence digitale moyenne.
    """
    df_p = df.copy()
    df_p['Tranche_Age'] = pd.cut(df_p['Âge'], bins=[17, 25, 35, 45, 55, 100], labels=['18-25', '26-35', '36-45', '46-55', '55+'])
    
    # On groupe par critères démographiques clés
    segments = df_p.groupby(['Tranche_Age', 'Secteur_Activite', 'Canal_Prefere'], observed=True)['Pret_Digital_Score'].agg(['mean', 'count']).reset_index()
    
    # On filtre pour ne garder que les segments représentatifs (au moins 2 personnes)
    segments = segments[segments['count'] >= 2]
    
    if segments.empty:
        return None, None
        
    segments = segments.sort_values(by='mean', ascending=False)
    
    # Top 2 meilleurs et Top 2 pires
    meilleurs = segments.head(2).to_dict('records')
    a_travailler = segments.tail(2).to_dict('records')
    
    return meilleurs, a_travailler