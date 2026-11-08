import streamlit as st
import pandas as pd
import os
import io

st.set_page_config(
    page_title="PredictAssure - Collecte & Registre",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] * {
        color: #1E1B4B !important;
    }
    
    .hero-box {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4F46E5 100%);
        padding: 2.2rem;
        border-radius: 16px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.25);
        margin-bottom: 1.8rem;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 0.3rem;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #E0E7FF;
        font-weight: 300;
        margin-bottom: 0.5rem;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        text-align: center;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1E1B4B;
    }
    .metric-lbl {
        font-size: 0.88rem;
        color: #64748B;
        font-weight: 500;
        margin-top: 0.2rem;
    }

    .content-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.8rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem;
    }

    .stForm {
        background-color: #FFFFFF !important;
    }
    
    .stForm h4 {
        color: #1E1B4B !important;
        font-weight: 700 !important;
        margin-top: 1rem !important;
        margin-bottom: 0.8rem !important;
    }

    label[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] span,
    .stForm label,
    .stForm p,
    .stForm legend {
        color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stMultiSelect"] label p,
    div[data-testid="stSlider"] label p {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    div[data-testid="stSlider"] div {
        color: #1E1B4B !important;
    }

    button[data-baseweb="tab"] {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #64748B !important;
        padding: 0.8rem 1.5rem !important;
    }
    button[aria-selected="true"] {
        color: #4F46E5 !important;
        border-bottom-color: #4F46E5 !important;
    }
    
    div.stButton > button[kind="primary"],
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.2rem !important;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25) !important;
        transition: all 0.25s ease-in-out !important;
    }
    
    div.stButton > button[kind="primary"]:hover,
    div.stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(79, 70, 229, 0.4) !important;
        background: linear-gradient(135deg, #4338CA 0%, #1E1B4B 100%) !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🔮 **PredictAssure**")
    st.caption("Module : Collecte & Registre de Données")
    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.write("""
    Ce module permet de :
    - Saisir de nouveaux profils répondants sur le terrain.
    - Consulter l'intégralité du registre de données.
    - Exporter la base aux formats CSV, Excel et PDF.
    """)
    st.markdown("---")
    st.success("🟢 Base de données connectée")

st.markdown("""
    <div class="hero-box">
        <div class="hero-title">📋 Collecte & Registre des Données</div>
        <div class="hero-sub">Observatoire terrain et centralisation des réponses d'enquête sur le marché de l'assurance au Cameroun.</div>
    </div>
""", unsafe_allow_html=True)

chemin_csv = "data/raw/sondage_assurance.csv"

# FONCTION D'EXPORT PDF
def generer_pdf(dataframe):
    try:
        from fpdf import FPDF
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "PREDICTASSURE - REGISTRE COMPLET DES DONNEES", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", size=8)
        cols_pdf = ["Âge", "Sexe", "Région", "Secteur_Activite", "Canal_Prefere", "Pret_Digital_Score"]
        
        for col in cols_pdf:
            pdf.cell(45, 8, str(col), border=1, align='C')
        pdf.ln()
        
        # Lignes
        pdf.set_font("Arial", size=7)
        for index, row in dataframe.iterrows():
            for col in cols_pdf:
                valeur = str(row[col])[:25]
                valeur = valeur.encode('latin-1', 'replace').decode('latin-1') 
                pdf.cell(45, 8, valeur, border=1)
            pdf.ln()
            
        return pdf.output(dest='S').encode('latin-1')
    except ImportError:
        return None

tab_formulaire, tab_registre = st.tabs(["📝 Formulaire de Collecte", "📊 Registre & Base de Données"])

# FORMULAIRE DE COLLECTE TERRAIN

with tab_formulaire:
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#1E1B4B; margin-top:0;'>📝 Renseigner un nouveau profil répondant</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#475569;'>Merci de compléter l'ensemble des sections pour alimenter la base de données actuarielles.</p>", unsafe_allow_html=True)

    regions = ["Littoral", "Centre", "Ouest", "Sud", "Nord", "Est", "Adamaoua", "Extrême-Nord", "Nord-Ouest", "Sud-Ouest"]
    secteurs = ["Public", "Privé Formel", "Informel (Commerçant/Artisan)", "Agriculteur", "Étudiant", "Libéral", "Sans emploi"]
    revenus = ["Moins de 50 000 FCFA", "50 000 - 150 000 FCFA", "150 000 - 300 000 FCFA", "Plus de 300 000 FCFA"]

    with st.form("formulaire_assurance", clear_on_submit=True):
        st.markdown("#### 👤 1. Profil et Localisation")
        col1, col2 = st.columns(2)
        with col1:
            sexe = st.selectbox("Sexe", ["Masculin", "Féminin"])
            region = st.selectbox("Région de résidence", regions)
        with col2:
            age = st.number_input("Âge", min_value=18, max_value=100, value=30, step=1)
            ville = st.text_input("Ville de résidence")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 💼 2. Situation Professionnelle & Financière")
        secteur = st.selectbox("Secteur d'activité", secteurs)
        revenu = st.selectbox("Revenu mensuel estimé", revenus)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🧠 3. Perception & Confiance envers le Secteur")
        connaissance = st.select_slider("Niveau de connaissance en assurance", options=["Nulle", "Faible", "Moyenne", "Bonne", "Expert"])
        confiance = st.slider("Niveau de confiance envers les assureurs (0 = Aucune, 10 = Totale)", 0, 10, 5)
        
        col3, col4 = st.columns(2)
        with col3:
            perception = st.radio("Pour vous, l'assurance est avant tout :", ["Une charge", "Une obligation", "Nécessaire"])
        with col4:
            barriere = st.selectbox("Principal frein à la souscription", ["Coût élevé", "Méfiance", "Lenteur administrative", "Manque d'info", "Religion"])

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🛡️ 4. Habitudes & Digitalisation")
        assurances_possedees = st.multiselect("Assurances actuellement possédées", ["Santé", "Auto", "Vie/Décès", "Habitation", "Agricole"])
        canal = st.selectbox("Par quel canal préférez-vous souscrire ?", ["Agent physique", "Courtier", "Banque", "App mobile"])
        sinistre = st.radio("Avez-vous déjà eu un sinistre non remboursé ?", ["Jamais eu de sinistre", "Non", "Oui"])
        
        pret_digital = st.slider("Êtes-vous prêt à gérer vos assurances 100% sur mobile ? (0 = Pas du tout, 10 = Totalement)", 0, 10, 5)
        mobile_money = st.radio("Fréquence d'utilisation du Mobile Money", ["Régulier (Orange/MTN Money)", "Occasionnel", "Jamais"])

        st.markdown("---")
        submitted = st.form_submit_button("💾 Enregistrer dans le Registre", type="primary", use_container_width=True)

        if submitted:
            if not ville.strip():
                st.error("⚠️ Veuillez renseigner votre ville avant de valider.")
            else:
                assurances_str = ", ".join(assurances_possedees) if assurances_possedees else "Aucune"

                nouvelle_entree = {
                    "Sexe": sexe, "Âge": age, "Région": region, "Ville": ville.capitalize(),
                    "Secteur_Activite": secteur, "Revenu_Mensuel": revenu,
                    "Perception_Assurance": perception, "Niveau_Connaissance": connaissance,
                    "Niveau_Confiance": confiance, "Barriere_Principale": barriere,
                    "Assurances_Possedees": assurances_str, "Canal_Prefere": canal,
                    "Sinistre_Non_Rembourse": sinistre, "Pret_Digital_Score": pret_digital,
                    "Utilisation_Mobile_Money": mobile_money
                }

                df_new = pd.DataFrame([nouvelle_entree])
                
                if os.path.exists(chemin_csv):
                    df_new.to_csv(chemin_csv, mode='a', header=False, index=False)
                else:
                    os.makedirs(os.path.dirname(chemin_csv), exist_ok=True)
                    df_new.to_csv(chemin_csv, index=False)

                st.success("✅ Nouveau profil enregistré avec succès dans le registre PredictAssure !")
    st.markdown('</div>', unsafe_allow_html=True)

# REGISTRE INTÉGRAL & EXPORTS

with tab_registre:
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#1E1B4B; margin-top:0;'>📊 Consultation du Registre & Exports</h3>", unsafe_allow_html=True)
    
    if os.path.exists(chemin_csv):
        df_actuel = pd.read_csv(chemin_csv)
        
        if df_actuel.empty:
            st.warning("⚠️ La base de données est actuellement vide.")
        else:

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-val">👥 {len(df_actuel)}</div>
                        <div class="metric-lbl">Profils Registrés</div>
                    </div>
                """, unsafe_allow_html=True)
            with c2:
                score_moy = round(df_actuel['Pret_Digital_Score'].mean(), 1)
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-val" style="color:#4F46E5;">📱 {score_moy}/10</div>
                        <div class="metric-lbl">Appétence Digitale Moyenne</div>
                    </div>
                """, unsafe_allow_html=True)
            with c3:
                conf_moy = round(df_actuel['Niveau_Confiance'].mean(), 1)
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-val" style="color:#059669;">⭐ {conf_moy}/10</div>
                        <div class="metric-lbl">Indice de Confiance Moyen</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#1E1B4B;'>📋 Registre Intégral des Données</h4>", unsafe_allow_html=True)
            st.dataframe(df_actuel, use_container_width=True, height=400)

            st.markdown("---")
            st.markdown("<h4 style='color:#1E1B4B;'>📥 Exporter la Base de Données</h4>", unsafe_allow_html=True)
            colA, colB, colC = st.columns(3)
            

            with colA:
                csv_data = df_actuel.to_csv(index=False).encode('utf-8')
                st.download_button("📄 Exporter en CSV", data=csv_data, file_name="registre_predictassure.csv", mime="text/csv", use_container_width=True)
                

            with colB:
                buffer = io.BytesIO()
                try:
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df_actuel.to_excel(writer, index=False, sheet_name='Registre_Données')
                    st.download_button("📊 Exporter en Excel", data=buffer.getvalue(), file_name="registre_predictassure.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
                except ImportError:
                    st.error("⚠️ Installez openpyxl (pip install openpyxl)")
                    

            with colC:
                pdf_data = generer_pdf(df_actuel)
                if pdf_data:
                    st.download_button("📑 Exporter en PDF", data=pdf_data, file_name="registre_predictassure.pdf", mime="application/pdf", use_container_width=True)
                else:
                    st.error("⚠️ Installez fpdf (pip install fpdf)")
    else:
        st.info("ℹ️ Aucun registre détecté. Veuillez effectuer une première saisie dans le volet Formulaire.")
    
    st.markdown('</div>', unsafe_allow_html=True)