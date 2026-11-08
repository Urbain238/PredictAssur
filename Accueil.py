import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(
    page_title="PredictAssure - Accueil",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Fond global clair */
    .stApp {
        background-color: #F8FAFC;
    }
    
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] h6 {
        color: #1E1B4B !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMarkdownContainer"] p {
        color: #0F172A !important;
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
        color: #FFFFFF !important;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.25);
        margin-bottom: 1.8rem;
    }
    .hero-box * {
        color: #FFFFFF !important;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 0.3rem;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #E0E7FF !important;
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
    .metric-tag {
        font-size: 0.78rem;
        font-weight: 600;
        color: #059669;
        margin-top: 0.3rem;
    }
    
    .nav-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #4F46E5;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
        margin-bottom: 1rem;
        height: 100%;
    }

    .survey-banner {
        background-color: #FFFFFF;
        border-left: 5px solid #059669;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem;
    }

    div.stButton > button[kind="primary"],
    div[data-testid="stPageLink"] a {
        background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1rem !important;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25) !important;
        transition: all 0.25s ease-in-out !important;
        text-decoration: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stPageLink"] a:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(79, 70, 229, 0.4) !important;
        background: linear-gradient(135deg, #4338CA 0%, #1E1B4B 100%) !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Taux de pénétration
def est_assure(val):
    if pd.isna(val): return 0
    if str(val).strip().lower() in ['aucune', 'aucun', 'none', '', 'nan']: return 0
    return 1

with st.sidebar:
    st.markdown("## 🔮 **PredictAssure**")
    st.caption("Plateforme d'analyse du taux de pénétration de l'assurance au Cameroun")
    st.markdown("---")
    st.markdown("### ℹ️ À propos du Projet")
    st.write("""
    **PredictAssure** Est mon projet personnel et scolaire qui combine mes deux domaines d'études et mes ambitions professionels et académiques.
    Avec mes humbles compétences en innformatique que j'obtiens à l'Université de Yaoundé I et mes competences en Techiques d'assurances et gestion des 
    risques que j'obtient à l'istitut international des assurances, j'ai decidé de tester et consilier mes connaissances dans ce projet d'analyses du taux de pénétration de l'assurance aux Cameroun et les raisons qui freinent le dévéloppement de l'assurance au Cameroun. 
    """)
    st.markdown("---")
    st.success("🟢 Version de test opérationnelle")

st.markdown("""
    <div class="hero-box">
        <div class="hero-title">🔮 PredictAssure - Accueil</div>
        <div class="hero-sub">Plateforme décisionnelle d'analyse du taux de pénétration dans le marché de l'assurance et de tarification dynamique au Cameroun.</div>
    </div>
""", unsafe_allow_html=True)

# Chargement du fichier csv
chemin_csv = "data/raw/sondage_assurance.csv"

dash_path = "pages/Dashboard_Analytics.py" if os.path.exists("pages/Dashboard_Analytics.py") else None
sim_path = "pages/Model_Machine_Learning.py" if os.path.exists("pages/Model_Machine_Learning.py") else None
form_path = "pages/Collecte_et_Registre_de_Donnees.py" if os.path.exists("pages/Collecte_et_Registre_de_Donnees.py") else None

try:
    from src.data_generator import charger_donnees, generer_donnees_initiales
except ImportError:
    try:
        from src.data_generator import generer_donnees
        generer_donnees_initiales = lambda path, n=200: generer_donnees(nb_lignes=n)
        charger_donnees = lambda chemin_fichier: pd.read_csv(chemin_fichier)
    except ImportError:
        charger_donnees = lambda chemin_fichier: pd.read_csv(chemin_fichier) if os.path.exists(chemin_fichier) else pd.DataFrame()
        generer_donnees_initiales = None

if not os.path.exists(chemin_csv):
    st.warning("⚠️ Aucune donnée disponible pour le moment. Cliquez ci-dessous pour générer l'échantillon initial.")
    if st.button("🚀 Initialiser la base avec 200 profils fictifs", type="primary", key="btn_init_base_first"):
        os.makedirs(os.path.dirname(chemin_csv), exist_ok=True)
        if generer_donnees_initiales:
            generer_donnees_initiales(chemin_csv)
        st.rerun()
else:
    df = charger_donnees(chemin_csv)
    
    if df.empty:
        st.warning("⚠️ La base de données est vide.")
    else:
        df['Est_Assure'] = df['Assurances_Possedees'].apply(est_assure)

        # Chargement des 5 premieres valeures
        col_title_data, col_btn_data = st.columns([3, 1])
        with col_title_data:
            st.subheader("📋 Aperçu de la Base de Données (5 Premiers Profils de +100)")
        with col_btn_data:
            st.write("")
            if st.button("🔄 Régénérer les données", type="primary", use_container_width=True, key="btn_regen_data"):
                if os.path.exists(chemin_csv):
                    os.remove(chemin_csv)
                if generer_donnees_initiales:
                    generer_donnees_initiales(chemin_csv)
                st.rerun()

        st.dataframe(df.head(5), use_container_width=True)

        st.markdown("---")

        c_nav1, c_nav2, c_nav3 = st.columns(3)

        with c_nav1:
            st.markdown("""
                <div class="nav-card">
                    <h4 style="color:#1E1B4B; margin-top:0;">📈 Dashboard Expert</h4>
                    <p style="color:#64748B; font-size:0.9rem;">Visualisation multi-graphiques approfondie, filtres régionaux et export du rapport stratégique PDF, Visualisation du taux de pénétration par secteur.</p>
                </div>
            """, unsafe_allow_html=True)
            if dash_path:
                st.page_link(dash_path, label="Accéder au Dashboard 📊", use_container_width=True)
            else:
                st.button("Dashboard indisponible", disabled=True, use_container_width=True, key="btn_dash_disabled_nav")

        with c_nav2:
            st.markdown("""
                <div class="nav-card">
                    <h4 style="color:#1E1B4B; margin-top:0;">🤖 Modèle Machine Learning</h4>
                    <p style="color:#64748B; font-size:0.9rem;">Détection des personas, prédiction du score digital par IA et devis d'assurance santé instantané.</p>
                </div>
            """, unsafe_allow_html=True)
            if sim_path:
                st.page_link(sim_path, label="Lancer le Modèle IA 🤖", use_container_width=True)
            else:
                st.button("Modèle ML indisponible", disabled=True, use_container_width=True, key="btn_sim_disabled_nav")

        with c_nav3:
            st.markdown("""
                <div class="nav-card">
                    <h4 style="color:#1E1B4B; margin-top:0;">📝 Collecte & Registre</h4>
                    <p style="color:#64748B; font-size:0.9rem;">Formulaire de collecte terrain et consultation/export de l'intégralité du registre. Ajout de données pour participer à l'analyse et faciliter la prise de décision.</p>
                </div>
            """, unsafe_allow_html=True)
            if form_path:
                st.page_link(form_path, label="Accéder au Registre 📝", use_container_width=True)
            else:
                st.button("Registre indisponible", disabled=True, use_container_width=True, key="btn_form_disabled_nav")

        st.markdown("---")

        # Donnees clés
        total_repondants = len(df)
        taux_penetration = round((df['Est_Assure'].mean() * 100), 1)
        confiance_moyenne = round(df['Niveau_Confiance'].mean(), 1)
        
        secteur_pen = df.groupby('Secteur_Activite')['Est_Assure'].mean().reset_index()
        secteur_pen['Taux'] = secteur_pen['Est_Assure'] * 100
        secteur_top = secteur_pen.sort_values(by='Taux', ascending=False).iloc[0]

        st.subheader("📌 Indicateurs Clés du Marché")
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        
        with col_k1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">👥 {total_repondants}</div>
                    <div class="metric-lbl">Répondants Enregistrés</div>
                    <div class="metric-tag">Taille de la cohorte</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_k2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val" style="color:#059669;">🛡️ {taux_penetration}%</div>
                    <div class="metric-lbl">Taux de Pénétration</div>
                    <div class="metric-tag">Taux d'équipement global</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_k3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val" style="color:#4F46E5;">⭐ {confiance_moyenne}/10</div>
                    <div class="metric-lbl">Indice de Confiance</div>
                    <div class="metric-tag">Perception secteur</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_k4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val" style="color:#D97706;">🏛️ {secteur_top['Taux']:.0f}%</div>
                    <div class="metric-lbl">Secteur Plus Émancipé</div>
                    <div class="metric-tag">{secteur_top['Secteur_Activite']}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c_text_survey, c_btn_survey = st.columns([3, 1])
        with c_text_survey:
            st.markdown("""
                <div class="survey-banner">
                    <h4 style="margin:0; color:#1E1B4B; font-weight:700;">📝 Alimenter ou Consulter le Registre</h4>
                    <p style="margin:0.3rem 0 0 0; color:#475569; font-size:0.95rem;">
                        Enregistrez un nouveau profil terrain ou téléchargez l'ensemble des données aux formats CSV, Excel et PDF.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_btn_survey:
            st.write("")
            if form_path:
                st.page_link(form_path, label="👉 Aller au Registre", use_container_width=True)
            else:
                st.button("Registre indisponible", disabled=True, use_container_width=True, key="btn_form_disabled_survey")

        st.markdown("---")

        # GRAPHIQUES STRATÉGIQUES
        
        st.subheader("📊 Émancipation & Pénétration de l'Assurance par Secteur")
        col_fig1, col_fig2 = st.columns(2)
        
        with col_fig1:
            df_sec = df.groupby('Secteur_Activite')['Est_Assure'].agg(['mean', 'count']).reset_index()
            df_sec['Taux_Penetration'] = round(df_sec['mean'] * 100, 1)
            df_sec = df_sec.sort_values(by='Taux_Penetration', ascending=True)
            
            fig_sec = px.bar(
                df_sec,
                x='Taux_Penetration',
                y='Secteur_Activite',
                orientation='h',
                title="<b>1. Pénétration par Secteur d'Activité (%)</b>",
                text='Taux_Penetration',
                color='Taux_Penetration',
                color_continuous_scale='Purples'
            )
            fig_sec.update_layout(
                paper_bgcolor='#FFFFFF',
                plot_bgcolor='#FFFFFF',
                font=dict(color="#0F172A", size=13),
                title=dict(font=dict(color="#1E1B4B", size=15)),
                xaxis=dict(
                    tickfont=dict(color="#0F172A", size=12),
                    title=dict(text="Taux de Pénétration (%)", font=dict(color="#0F172A", size=13)),
                    showgrid=True,
                    gridcolor="#E2E8F0"
                ),
                yaxis=dict(
                    tickfont=dict(color="#0F172A", size=12),
                    title=dict(text="Secteur d'Activité", font=dict(color="#0F172A", size=13))
                ),
                height=350,
                coloraxis_showscale=False,
                margin=dict(l=10, r=35, t=40, b=10)
            )
            fig_sec.update_traces(
                texttemplate='%{text}%',
                textposition='outside',
                textfont=dict(color="#0F172A", size=12, family="Arial")
            )
            st.plotly_chart(fig_sec, use_container_width=True)

        with col_fig2:
            df_dig = df.groupby('Secteur_Activite')['Pret_Digital_Score'].mean().reset_index()
            df_dig['Pret_Digital_Score'] = round(df_dig['Pret_Digital_Score'], 1)
            
            fig_dig = px.bar(
                df_dig,
                x='Secteur_Activite',
                y='Pret_Digital_Score',
                title="<b>2. Appétence Digitale Moyenne (Score 0-10)</b>",
                text='Pret_Digital_Score',
                color_discrete_sequence=['#4F46E5']
            )
            fig_dig.update_layout(
                paper_bgcolor='#FFFFFF',
                plot_bgcolor='#FFFFFF',
                font=dict(color="#0F172A", size=13),
                title=dict(font=dict(color="#1E1B4B", size=15)),
                xaxis=dict(
                    tickfont=dict(color="#0F172A", size=12),
                    title=dict(text="Secteur d'Activité", font=dict(color="#0F172A", size=13))
                ),
                yaxis=dict(
                    range=[0, 10.5],
                    tickfont=dict(color="#0F172A", size=12),
                    title=dict(text="Score Digital Moyen (/10)", font=dict(color="#0F172A", size=13)),
                    showgrid=True,
                    gridcolor="#E2E8F0"
                ),
                height=350,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            fig_dig.update_traces(
                textposition='outside',
                textfont=dict(color="#0F172A", size=12, family="Arial")
            )
            st.plotly_chart(fig_dig, use_container_width=True)