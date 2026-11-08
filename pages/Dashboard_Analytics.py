import streamlit as st
import pandas as pd
import plotly.express as px
import os
from fpdf import FPDF
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

st.set_page_config(
    page_title="PredictAssure - Dashboard",
    page_icon="📈",
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

    .section-header {
        color: #1E1B4B;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .chart-caption {
        font-size: 0.85rem;
        color: #475569;
        background-color: #F1F5F9;
        padding: 0.6rem 0.9rem;
        border-radius: 8px;
        border-left: 3px solid #4F46E5;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
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

# 3. HELPER : APPLICATION DU THÈME CLAIR & TEXTE SOMBRE AUX GRAPHIQUES PLOTLY
def style_figure(fig, height=360):
    fig.update_layout(
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(color="#0F172A", size=12),
        title=dict(font=dict(color="#1E1B4B", size=14, family="Arial")),
        xaxis=dict(
            tickfont=dict(color="#0F172A", size=11),
            title=dict(font=dict(color="#0F172A", size=12)),
            showgrid=True,
            gridcolor="#E2E8F0"
        ),
        yaxis=dict(
            tickfont=dict(color="#0F172A", size=11),
            title=dict(font=dict(color="#0F172A", size=12)),
            showgrid=True,
            gridcolor="#E2E8F0"
        ),
        legend=dict(font=dict(color="#0F172A", size=11)),
        height=height,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

# RAPPORT PDF
def clean_txt(text):
    return str(text).encode('latin-1', 'replace').decode('latin-1')

def generer_rapport_pdf(df_pdf):
    try:
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(0, 10, clean_txt("RAPPORT STRATEGIQUE : MARCHE DE L'ASSURANCE"), ln=True, align='C')
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, clean_txt(f"Rapport généré automatiquement - Base de {len(df_pdf)} répondants"), ln=True, align='C')
        pdf.ln(10)
        
        age_moyen = round(df_pdf["Âge"].mean(), 1)
        confiance_moy = round(df_pdf["Niveau_Confiance"].mean(), 1)
        digital_moy = round(df_pdf["Pret_Digital_Score"].mean(), 1)
        top_frein = df_pdf["Barriere_Principale"].mode()[0] if not df_pdf["Barriere_Principale"].empty else "N/A"
        top_canal = df_pdf["Canal_Prefere"].mode()[0] if not df_pdf["Canal_Prefere"].empty else "N/A"
        top_secteur = df_pdf["Secteur_Activite"].mode()[0] if not df_pdf["Secteur_Activite"].empty else "N/A"
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, clean_txt("1. RESUME EXECUTIF & CHIFFRES CLES"), ln=True)
        pdf.set_font("Arial", '', 11)
        intro = (f"L'echantillon etudie comprend {len(df_pdf)} profils, avec un age moyen de {age_moyen} ans. "
                 f"Le score moyen de confiance envers le secteur de l'assurance est de {confiance_moy}/10, "
                 f"tandis que l'appetence pour une gestion 100% digitale s'eleve a {digital_moy}/10.")
        pdf.multi_cell(0, 7, clean_txt(intro))
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, clean_txt("2. PROFIL DEMOGRAPHIQUE ET PROFESSIONNEL"), ln=True)
        pdf.set_font("Arial", '', 11)
        demo_txt = (f"Le secteur d'activite le plus represente dans cette cohorte est : '{top_secteur}'. "
                    f"Cette donnee est cruciale car elle determine la capacite contributive et la nature des risques a couvrir.")
        pdf.multi_cell(0, 7, clean_txt(demo_txt))
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, clean_txt("3. FREINS A LA SOUSCRIPTION & PERCEPTION"), ln=True)
        pdf.set_font("Arial", '', 11)
        freins_txt = (f"Le principal obstacle a la souscription identifie est : '{top_frein}'. "
                      f"Pour surmonter cette barriere, les offres devront integrer des mecanismes de rassurance ou d'adaptation financiere.")
        pdf.multi_cell(0, 7, clean_txt(freins_txt))
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, clean_txt("4. STRATEGIE DE DISTRIBUTION ET DIGITALISATION"), ln=True)
        pdf.set_font("Arial", '', 11)
        digi_txt = (f"Le canal d'acquisition preferé est : '{top_canal}'. "
                    f"Avec un score digital moyen de {digital_moy}/10, la strategie de distribution doit s'aligner sur cette preference.")
        pdf.multi_cell(0, 7, clean_txt(digi_txt))
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, clean_txt("5. RECOMMANDATIONS STRATEGIQUES POUR LE LANCEMENT"), border=1, ln=True, fill=True)
        pdf.set_font("Arial", '', 11)
        reco = ("- Produit : Concevoir des offres modulables adaptees aux revenus.\n"
                "- Distribution : Pousser l'integration avec les telcos (Mobile Money).\n"
                "- Communication : Axer les campagnes marketing sur la levee du frein principal.\n"
                "- Experience Client : Garantir un remboursement express pour ameliorer la confiance.")
        pdf.multi_cell(0, 7, clean_txt(reco))
        
        return pdf.output(dest='S').encode('latin-1')
    except Exception:
        return None

with st.sidebar:
    st.markdown("## 🔮 **PredictAssure**")
    st.caption("Module : Dashboard Expert & Machine Learning")
    st.markdown("---")
    st.markdown("### 🔍 Affiner l'analyse")

chemin_csv = "data/raw/sondage_assurance.csv"

st.markdown("""
    <div class="hero-box">
        <div class="hero-title">📈 Tableau de Bord Expert & Analytics</div>
        <div class="hero-sub">Analyse approfondie des comportements, de la confiance, du taux d'équipement et modélisation IA.</div>
    </div>
""", unsafe_allow_html=True)

if not os.path.exists(chemin_csv):
    st.warning("⚠️ Aucune donnée disponible. Veuillez initialiser la base depuis la page d'Accueil.")
else:
    df = pd.read_csv(chemin_csv)

    if df.empty:
        st.warning("⚠️ La base de données est vide.")
    else:
        df['Tranche_Age'] = pd.cut(df['Âge'], bins=[17, 25, 35, 45, 55, 100], labels=['18-25', '26-35', '36-45', '46-55', '55+'])

        def est_assure(x):
            if pd.isna(x): return 0
            if str(x).strip().lower() in ['aucune', 'aucun', 'none', '', 'nan']: return 0
            return 1
            
        df['Est_Assure_Num'] = df['Assurances_Possedees'].apply(est_assure)

        with st.sidebar:
            region_f = st.selectbox("Région", ["Toutes"] + list(df["Région"].dropna().unique()))
            secteur_f = st.selectbox("Secteur d'Activité", ["Tous"] + list(df["Secteur_Activite"].dropna().unique()))
            
            min_a, max_a = int(df["Âge"].min()), int(df["Âge"].max())
            if min_a == max_a: max_a += 1
            age_f = st.slider("Tranche d'Âge", min_a, max_a, (min_a, max_a))
            
            st.markdown("---")
            st.info("🟢 Données temps réel réactives")

        # Filtrage du jeu de données
        df_filtered = df.copy()
        if region_f != "Toutes": df_filtered = df_filtered[df_filtered["Région"] == region_f]
        if secteur_f != "Tous": df_filtered = df_filtered[df_filtered["Secteur_Activite"] == secteur_f]
        df_filtered = df_filtered[(df_filtered["Âge"] >= age_f[0]) & (df_filtered["Âge"] <= age_f[1])]

        # Calcul des KPIs
        kpis = {
            "age": round(df_filtered["Âge"].mean(), 1) if not df_filtered.empty else 0,
            "confiance": round(df_filtered["Niveau_Confiance"].mean(), 1) if not df_filtered.empty else 0,
            "digital": round(df_filtered["Pret_Digital_Score"].mean(), 1) if not df_filtered.empty else 0,
            "penetration": round(df_filtered["Est_Assure_Num"].mean() * 100, 1) if not df_filtered.empty else 0
        }
        
        # Affichage des Cartes KPIs
        st.subheader("📌 Indicateurs Synthétiques de la Cohorte")
        col_k1, col_k2, col_k3, col_k4, col_k5, col_pdf = st.columns([1, 1, 1, 1, 1, 1.6])
        
        with col_k1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">👥 {len(df_filtered)}</div>
                    <div class="metric-lbl">Répondants au sondage en temps réel dans la plateforme</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_k2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">🎂 {kpis['age']} ans</div>
                    <div class="metric-lbl">Âge Moyen de la population</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_k3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val" style="color:#4F46E5;">⭐ {kpis['confiance']}/10</div>
                    <div class="metric-lbl">Confiance Secteur</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_k4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val" style="color:#D97706;">📱 {kpis['digital']}/10</div>
                    <div class="metric-lbl">Appétence Digitale</div>
                </div>
            """, unsafe_allow_html=True)

        with col_k5:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val" style="color:#059669;">🛡️ {kpis['penetration']}%</div>
                    <div class="metric-lbl">Taux d'Équipement</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_pdf:
            st.write("")
            pdf_bytes = generer_rapport_pdf(df_filtered)
            if pdf_bytes:
                st.download_button("📑 Générer Rapport PDF", data=pdf_bytes, file_name="Rapport_Complet_Assurance.pdf", mime="application/pdf", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if df_filtered.empty:
            st.error("⚠️ Aucune donnée ne correspond aux filtres sélectionnés.")
        else:

            # SECTION 1 : PROFIL SOCIODÉMOGRAPHIQUE
            
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">1️⃣ Profil Sociodémographique</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                fig_pyr = px.histogram(df_filtered, x="Âge", color="Sexe", nbins=20, title="<b>1. Pyramide des Âges et Sexe</b>", marginal="box", color_discrete_sequence=['#4F46E5', '#EC4899'])
                st.plotly_chart(style_figure(fig_pyr), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Permet d\'identifier le cœur de cible démographique actuel. La répartition guide le ton des futures communications.</div>', unsafe_allow_html=True)
            with c2:
                fig_sect = px.pie(df_filtered, names="Secteur_Activite", title="<b>2. Répartition par Secteur d'Activité</b>", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(style_figure(fig_sect), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Identifie la stabilité des revenus potentiels des cibles (informel vs formel, privé vs public) pour calibrer le risque.</div>', unsafe_allow_html=True)
            
            c3, c4 = st.columns(2)
            with c3:
                fig_reg = px.bar(df_filtered["Région"].value_counts().reset_index(), x="Région", y="count", title="<b>3. Volume par Région</b>", text_auto=True, color_discrete_sequence=['#312E81'])
                st.plotly_chart(style_figure(fig_reg), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Met en lumière les zones géographiques d\'où proviennent les données pour prioriser les déploiements.</div>', unsafe_allow_html=True)
            with c4:
                fig_rev = px.histogram(df_filtered, x="Revenu_Mensuel", color="Secteur_Activite", barmode="stack", title="<b>4. Structure des Revenus par Secteur</b>", color_discrete_sequence=px.colors.qualitative.Bold)
                st.plotly_chart(style_figure(fig_rev), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Croise la capacité financière et l\'emploi. Indispensable pour la tarification modulable.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


            # TAUX DE PÉNÉTRATION DE L'ASSURANCE

            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">2️⃣ Taux de Pénétration de l\'Assurance</div>', unsafe_allow_html=True)
            st.markdown("<p style='color:#475569;'>Proportion de répondants détenant au moins un produit d'assurance.</p>", unsafe_allow_html=True)
            
            c_pen1, c_pen2 = st.columns(2)
            with c_pen1:
                pen_reg = df_filtered.groupby("Région")["Est_Assure_Num"].mean().reset_index()
                pen_reg["Taux (%)"] = pen_reg["Est_Assure_Num"] * 100
                fig_pen_reg = px.bar(pen_reg, x="Région", y="Taux (%)", title="<b>5. Pénétration par Région</b>", text_auto='.1f', color="Taux (%)", color_continuous_scale="Purples")
                st.plotly_chart(style_figure(fig_pen_reg), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Détecte instantanément les régions sous-équipées qui représentent des relais de croissance massifs.</div>', unsafe_allow_html=True)

            with c_pen2:
                pen_age = df_filtered.groupby("Tranche_Age")["Est_Assure_Num"].mean().reset_index()
                pen_age["Taux (%)"] = pen_age["Est_Assure_Num"] * 100
                fig_pen_age = px.bar(pen_age, x="Tranche_Age", y="Taux (%)", title="<b>6. Pénétration par Tranche d'Âge</b>", text_auto='.1f', color="Taux (%)", color_continuous_scale="Viridis")
                st.plotly_chart(style_figure(fig_pen_age), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Illustre la vulnérabilité des différentes générations. Les jeunes sont souvent non assurés, offrant une opportunité pour des produits d\'appel.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

           
            # ÉQUIPEMENT ET MARCHÉ
       
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">3️⃣ Équipement et Rapport au Marché</div>', unsafe_allow_html=True)
            
            c5, c6 = st.columns(2)
            assurances_list = df_filtered["Assurances_Possedees"].str.split(", ").explode().value_counts().reset_index()
            assurances_list.columns = ["Type_Assurance", "Nombre"]
            with c5:
                fig_ass = px.bar(assurances_list, x="Type_Assurance", y="Nombre", title="<b>7. Types d'assurances actuellement possédées</b>", color="Type_Assurance", color_discrete_sequence=px.colors.qualitative.Vivid)
                st.plotly_chart(style_figure(fig_ass), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Montre les produits leaders du marché (souvent l\'auto par obligation, puis la santé).</div>', unsafe_allow_html=True)
            with c6:
                fig_sinistre = px.pie(df_filtered, names="Sinistre_Non_Rembourse", title="<b>8. Expérience de sinistre non remboursé</b>", color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(style_figure(fig_sinistre), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Évalue la "traumatologie" du marché. Un taux élevé de "Oui" exige de redoubler de transparence.</div>', unsafe_allow_html=True)
            
            c7, c8 = st.columns(2)
            with c7:
                fig_conn = px.histogram(df_filtered, x="Niveau_Connaissance", category_orders={"Niveau_Connaissance": ["Nulle", "Faible", "Moyenne", "Bonne", "Expert"]}, title="<b>9. Auto-évaluation des connaissances en assurance</b>", color_discrete_sequence=['#6366F1'])
                st.plotly_chart(style_figure(fig_conn), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Jauge le niveau d\'éducation financière. Si la connaissance est "Faible/Nulle", simplifiez le vocabulaire marketing.</div>', unsafe_allow_html=True)
            with c8:
                fig_perc = px.pie(df_filtered, names="Perception_Assurance", title="<b>10. L'assurance perçue comme...</b>", hole=0.3, color_discrete_sequence=px.colors.qualitative.Safe)
                st.plotly_chart(style_figure(fig_perc), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Mesure le sentiment profond (Obligation vs Protection).</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # SECTION 4 : FREINS & CONFIANCE
            
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">4️⃣ Analyse des Barrières et de la Confiance</div>', unsafe_allow_html=True)
            
            c9, c10 = st.columns(2)
            with c9:
                fig_freins = px.histogram(df_filtered, y="Barriere_Principale", color="Tranche_Age", orientation="h", barmode="group", title="<b>11. Principaux Freins par Tranche d'Âge</b>", color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(style_figure(fig_freins), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Oriente les arbitrages. Si le "Prix" domine, proposez de la micro-assurance ; si c\'est la "Méfiance", renforcez la preuve sociale.</div>', unsafe_allow_html=True)
            with c10:
                fig_conf_rev = px.box(df_filtered, x="Revenu_Mensuel", y="Niveau_Confiance", color="Revenu_Mensuel", title="<b>12. Niveau de Confiance selon le Revenu</b>", color_discrete_sequence=px.colors.qualitative.Dark2)
                st.plotly_chart(style_figure(fig_conf_rev), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Boxplot révélant la variabilité de la confiance au sein de chaque tranche de revenus.</div>', unsafe_allow_html=True)
            
            c11, c12 = st.columns(2)
            with c11:
                conf_reg = df_filtered.groupby("Région")["Niveau_Confiance"].mean().reset_index().sort_values(by="Niveau_Confiance")
                fig_conf_reg = px.bar(conf_reg, x="Région", y="Niveau_Confiance", text_auto='.1f', title="<b>13. Indice de Confiance Moyen par Région</b>", color_discrete_sequence=['#059669'])
                st.plotly_chart(style_figure(fig_conf_reg), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Cartographie le climat de confiance local. Une zone méfiante demandera plus de relais terrain.</div>', unsafe_allow_html=True)
            with c12:
                fig_conf_sin = px.box(df_filtered, x="Sinistre_Non_Rembourse", y="Niveau_Confiance", color="Sinistre_Non_Rembourse", title="<b>14. Impact d'un sinistre non remboursé sur la confiance</b>", color_discrete_sequence=['#EF4444', '#10B981', '#F59E0B'])
                st.plotly_chart(style_figure(fig_conf_sin), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Visualise la dégradation de la confiance causée par l\'insatisfaction d\'un sinistre non indemnisé.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # DIGITALISATION ET DISTRIBUTION

            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">5️⃣ Appétence Digitale et Distribution</div>', unsafe_allow_html=True)
            
            c13, c14 = st.columns(2)
            with c13:
                fig_canal = px.histogram(df_filtered, x="Canal_Prefere", color="Secteur_Activite", barmode="stack", title="<b>15. Canal de Souscription par Secteur</b>", color_discrete_sequence=px.colors.qualitative.Pastel1)
                st.plotly_chart(style_figure(fig_canal), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Oriente les arbitrages entre agences physiques, courtiers et applications mobiles.</div>', unsafe_allow_html=True)
            with c14:
                fig_momo = px.pie(df_filtered, names="Utilisation_Mobile_Money", title="<b>16. Fréquence d'utilisation du Mobile Money</b>", color_discrete_sequence=px.colors.qualitative.Prism)
                st.plotly_chart(style_figure(fig_momo), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Indicateur d\'adoption des paiements digitaux pour le prélèvement des primes.</div>', unsafe_allow_html=True)
            
            c15, c16 = st.columns(2)
            with c15:
                fig_corr = px.scatter(df_filtered, x="Âge", y="Pret_Digital_Score", color="Canal_Prefere", trendline="ols", title="<b>17. Corrélation : Âge vs Appétence Digitale</b>", color_discrete_sequence=px.colors.qualitative.Bold)
                st.plotly_chart(style_figure(fig_corr), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Analyse la pente (trendline) entre l\'âge et l\'appétence pour le 100% mobile.</div>', unsafe_allow_html=True)
            with c16:
                fig_digi_momo = px.box(df_filtered, x="Utilisation_Mobile_Money", y="Pret_Digital_Score", color="Utilisation_Mobile_Money", title="<b>18. Score Digital selon l'usage du Mobile Money</b>", color_discrete_sequence=px.colors.qualitative.Antique)
                st.plotly_chart(style_figure(fig_digi_momo), use_container_width=True)
                st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Démontre la passerelle naturelle entre usagers du Mobile Money et l\'Insurtech.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # INTELLIGENCE ARTIFICIELLE & MACHINE LEARNING

            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">6️⃣ Modélisation Multidimensionnelle & IA</div>', unsafe_allow_html=True)
            
            fig_sunburst = px.sunburst(df_filtered, path=['Région', 'Secteur_Activite', 'Canal_Prefere'], color='Pret_Digital_Score', color_continuous_scale='Purples', title="<b>19. Matrice de Ciblage Globale (Sunburst)</b>")
            st.plotly_chart(style_figure(fig_sunburst, height=450), use_container_width=True)
            st.markdown('<div class="chart-caption">ℹ️ <b>Détail :</b> Graphique exploratoire interactif. Cliquez sur les tranches pour naviguer dans les sous-segments.</div>', unsafe_allow_html=True)
            
            if len(df_filtered) >= 15:
                # K-Means Clustering
                X_cluster = df_filtered[["Âge", "Niveau_Confiance", "Pret_Digital_Score"]].dropna()
                kmeans = KMeans(n_clusters=3, random_state=42)
                df_filtered.loc[X_cluster.index, 'Cluster'] = kmeans.fit_predict(X_cluster)
                df_filtered['Cluster'] = df_filtered['Cluster'].map({0: 'Groupe A', 1: 'Groupe B', 2: 'Groupe C'})
                
                c_ml1, c_ml2 = st.columns(2)
                
                with c_ml1:
                    fig_3d = px.scatter_3d(df_filtered, x='Âge', y='Niveau_Confiance', z='Pret_Digital_Score', color='Cluster', symbol='Canal_Prefere', title="<b>20. Segments Clients 3D (K-Means)</b>", color_discrete_sequence=['#4F46E5', '#059669', '#D97706'])
                    fig_3d.update_layout(
                        paper_bgcolor='#FFFFFF',
                        plot_bgcolor='#FFFFFF',
                        font=dict(color="#0F172A", size=11),
                        scene=dict(
                            xaxis=dict(backgroundcolor="#F8FAFC", gridcolor="#E2E8F0"),
                            yaxis=dict(backgroundcolor="#F8FAFC", gridcolor="#E2E8F0"),
                            zaxis=dict(backgroundcolor="#F8FAFC", gridcolor="#E2E8F0")
                        ),
                        height=420,
                        margin=dict(l=10, r=10, t=40, b=10)
                    )
                    st.plotly_chart(fig_3d, use_container_width=True)
                    st.markdown('<div class="chart-caption">ℹ️ <b>IA Non Supervisée :</b> Découverte automatique de 3 typologies de clients basées sur l\'âge, la confiance et l\'usage du digital.</div>', unsafe_allow_html=True)
                
                # Random Forest
                with c_ml2:
                    df_ml = df_filtered.copy().dropna(subset=["Âge", "Sexe", "Région", "Secteur_Activite", "Revenu_Mensuel", "Niveau_Confiance", "Pret_Digital_Score"])
                    le = LabelEncoder()
                    y = (df_ml["Pret_Digital_Score"] >= 7).astype(int)
                    features = ["Âge", "Sexe", "Région", "Secteur_Activite", "Revenu_Mensuel", "Niveau_Confiance"]
                    X = df_ml[features].copy()
                    for col in ["Sexe", "Région", "Secteur_Activite", "Revenu_Mensuel"]:
                        X[col] = le.fit_transform(X[col])
                    
                    rf = RandomForestClassifier(n_estimators=100, random_state=42)
                    rf.fit(X, y)
                    importance_df = pd.DataFrame({'Critère': features, 'Impact (%)': rf.feature_importances_ * 100}).sort_values(by='Impact (%)', ascending=True)
                    
                    fig_rf = px.bar(importance_df, x='Impact (%)', y='Critère', orientation='h', title="<b>21. Facteurs d'Appétence Digitale (Random Forest)</b>", color='Impact (%)', color_continuous_scale="Purples")
                    st.plotly_chart(style_figure(fig_rf, height=420), use_container_width=True)
                    st.markdown('<div class="chart-caption">ℹ️ <b>IA Supervisée :</b> Identifie l\'importance relative de chaque variable dans la prédiction d\'un score digital élevé.</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ L'échantillon actuel comprend moins de 15 profils. Filtrez de manière plus large pour afficher les algorithmes d'IA (K-Means & Random Forest).")
            
            st.markdown('</div>', unsafe_allow_html=True)