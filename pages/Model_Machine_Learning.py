import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px

# Import des modules de Machine Learning
from src.actuariat import calculer_prime_pure_sante, calculer_prime_commerciale
from src.ml_model import preparer_et_entrainer, detecter_personas

st.set_page_config(
    page_title="PredictAssure - Simulateur IA & Actuariat",
    page_icon="🤖",
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

    div[data-testid="stAlert"] * {
        color: #0F172A !important;
    }

    .stForm {
        background-color: #FFFFFF !important;
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

    div[data-testid="stSelectbox"] label p,
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
        margin=dict(l=20, r=20, t=45, b=20)
    )
    return fig

with st.sidebar:
    st.markdown("## 🔮 **PredictAssure**")
    st.caption("Module : IA & Tarification Actuarielle")
    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.write("""
    Ce module combine :
    - **Machine Learning (Random Forest)** pour estimer la conversion digitale.
    - **Science Actuarielle** pour simuler le calcule de la prime pure et la prime commerciale sur-mesure.
    """)
    st.markdown("---")
    st.success("🟢 Modèles IA & Actuariat")

st.markdown("""
    <div class="hero-box">
        <div class="hero-title">🤖 Simulateur IA & Tarification Actuarielle</div>
        <div class="hero-sub">Prédiction personnalisée de l'appétence digitale et tarification scientifique du risque santé.</div>
    </div>
""", unsafe_allow_html=True)

chemin_csv = "data/raw/sondage_assurance.csv"

if not os.path.exists(chemin_csv):
    st.error("⚠️ Fichier de données introuvable. Veuillez d'abord alimenter le registre.")
else:
    df = pd.read_csv(chemin_csv)
    
    if len(df) < 15:
        st.warning("⚠️ L'échantillon de données actuel est trop restreint pour entraîner les modèles IA (minimum 15 profils requis).")
    else:
        # Chargement du modèle et détection des Personas
        modele_rf, encoders, features = preparer_et_entrainer(df)
        meilleurs_personas, pires_personas = detecter_personas(df)
        
        # PERSONAS ET OPPORTUNITÉS STRATÉGIQUES
        if meilleurs_personas and pires_personas:
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">💡 Opportunités Stratégiques Identifiées par l\'IA</div>', unsafe_allow_html=True)
            st.markdown("<p style='color:#475569; margin-bottom: 1.2rem;'>Profils clés déterminés d'après l'analyse prédictive de la base.</p>", unsafe_allow_html=True)
            
            c_miser, c_effort = st.columns(2)
            
            with c_miser:
                st.markdown("<h4 style='color:#059669; font-weight:500; margin-bottom: 0.7rem;'>✅ SUR QUI MISER (Canaux Digitaux 100% Mobile)</h4>", unsafe_allow_html=True)
                for p in meilleurs_personas:
                    st.markdown(f"""
                        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-left: 5px solid #059669; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.9rem; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                            <div style="font-weight: 700; color: #0F172A; font-size: 1.05rem;">🎯 {p['Tranche_Age']} ans | {p['Secteur_Activite']}</div>
                            <div style="color: #334155; font-size: 0.9rem; margin-top: 0.4rem; line-height: 1.5;">
                                <b>Score Digital Moyen :</b> <span style="color: #059669; font-weight: 700;">{p['mean']:.1f}/10</span> <br>
                                <b>Canal privilégié :</b> <span style="color: #1E1B4B; font-weight: 600;">{p['Canal_Prefere']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
            with c_effort:
                st.markdown("<h4 style='color:#DC2626; font-weight:500; margin-bottom: 0.7rem;'>⚠️ SUR QUI FAIRE UN EFFORT (Approche Phygitale / Réseau)</h4>", unsafe_allow_html=True)
                for p in pires_personas:
                    st.markdown(f"""
                        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-left: 5px solid #DC2626; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.9rem; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                            <div style="font-weight: 700; color: #0F172A; font-size: 1.05rem;">👤 {p['Tranche_Age']} ans | {p['Secteur_Activite']}</div>
                            <div style="color: #334155; font-size: 0.9rem; margin-top: 0.4rem; line-height: 1.5;">
                                <b>Score Digital Moyen :</b> <span style="color: #DC2626; font-weight: 700;">{p['mean']:.1f}/10</span> <br>
                                <b>Canal privilégié :</b> <span style="color: #1E1B4B; font-weight: 600;">{p['Canal_Prefere']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#1E1B4B;'>📊 Comparaison Visuelle des Segments</h4>", unsafe_allow_html=True)
            
            df_miser = pd.DataFrame(meilleurs_personas)
            df_miser['Catégorie'] = 'À Miser (Digital)'
            df_effort = pd.DataFrame(pires_personas)
            df_effort['Catégorie'] = 'Effort Requis (Phygital)'
            
            df_visu = pd.concat([df_miser, df_effort])
            df_visu['Libellé'] = df_visu['Tranche_Age'].astype(str) + " - " + df_visu['Secteur_Activite']
            
            col_bar, col_pie = st.columns(2)
            
            with col_bar:
                fig_personas = px.bar(
                    df_visu, 
                    x='mean', 
                    y='Libellé', 
                    color='Catégorie',
                    orientation='h',
                    title="<b>Score Digital Moyen par Persona</b>",
                    labels={'mean': 'Score Digital Moyen (/10)', 'Libellé': 'Segment Persona'},
                    color_discrete_map={'À Miser (Digital)': '#059669', 'Effort Requis (Phygital)': '#DC2626'}
                )
                st.plotly_chart(style_figure(fig_personas, height=380), use_container_width=True)
                
            with col_pie:
                fig_pie_strat = px.pie(
                    df_visu,
                    names='Catégorie',
                    title="<b>Répartition Stratégique des Segments</b>",
                    color='Catégorie',
                    color_discrete_map={'À Miser (Digital)': '#059669', 'Effort Requis (Phygital)': '#DC2626'},
                    hole=0.4
                )
                st.plotly_chart(style_figure(fig_pie_strat, height=380), use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # FORMULAIRE DE SIMULATION PROSPECT

        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">🎯 Tester un Nouveau Profil Prospect</div>', unsafe_allow_html=True)
        st.markdown("<p style='color:#475569;'>Renseignez les critères du prospect pour obtenir son score d'appétence et sa prime d'assurance.</p>", unsafe_allow_html=True)

        with st.form("simulateur_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                age_input = st.slider("Âge du prospect", 18, 80, 30)
                sexe_input = st.selectbox("Sexe", df["Sexe"].dropna().unique())
            
            with col2:
                region_input = st.selectbox("Région de résidence", df["Région"].dropna().unique())
                secteur_input = st.selectbox("Secteur d'Activité", df["Secteur_Activite"].dropna().unique())
                
            with col3:
                revenu_input = st.selectbox("Revenu Mensuel Estimé", df["Revenu_Mensuel"].dropna().unique())
                confiance_input = st.slider("Niveau de Confiance (0 = Nulle, 10 = Totale)", 1, 10, 5)
                
            st.markdown("---")
            submit = st.form_submit_button("🚀 Lancer l'Analyse Globale & Tarification", type="primary", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # SECTION 3 : RÉSULTATS DE L'ANALYSE ET EXPORT
        
        if submit:
            def safe_encode(encoder, valeur):
                if valeur in encoder.classes_:
                    return encoder.transform([valeur])[0]
                return 0

            input_data = pd.DataFrame([{
                "Âge": age_input,
                "Sexe": safe_encode(encoders["Sexe"], sexe_input),
                "Région": safe_encode(encoders["Région"], region_input),
                "Secteur_Activite": safe_encode(encoders["Secteur_Activite"], secteur_input),
                "Revenu_Mensuel": safe_encode(encoders["Revenu_Mensuel"], revenu_input),
                "Niveau_Confiance": confiance_input
            }])

            # Prédiction ML
            proba_succes = modele_rf.predict_proba(input_data)[0][1] * 100
            
            # Calcul Actuariel
            prime_pure = calculer_prime_pure_sante(age_input, region_input)
            prime_ttc = calculer_prime_commerciale(prime_pure)
            frais = prime_ttc - prime_pure

            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 Synthèse de la Simulation</div>', unsafe_allow_html=True)
            
            # Génération du rapport texte
            rapport_txt = f"""PREDICTASSURE - RAPPORT D'ANALYSE PROSPECT
=====================================================
PROFIL DU PROSPECT :
- Âge : {age_input} ans
- Sexe : {sexe_input}
- Région : {region_input}
- Secteur d'activité : {secteur_input}
- Revenu Mensuel : {revenu_input}
- Niveau de Confiance : {confiance_input}/10

PRÉDICTION INTELLIGENCE ARTIFICIELLE :
- Probabilité de conversion digitale : {proba_succes:.1f}%

TARIFICATION ACTUARIELLE (SANTÉ) :
- Prime Pure (Risque) : {int(prime_pure):,} FCFA
- Frais de Gestion & Taxes : {int(frais):,} FCFA
- Prime Commerciale TTC : {int(prime_ttc):,} FCFA
""".replace(",", " ")

            st.download_button(
                label="📥 Télécharger le Devis & Rapport d'Analyse (TXT)",
                data=rapport_txt,
                file_name=f"rapport_prospect_{age_input}ans_{secteur_input.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            st.markdown("<br>", unsafe_allow_html=True)

            tab1, tab2 = st.tabs(["🤖 Prédiction IA (Conversion)", "💰 Actuariat (Tarification)"])
            
            with tab1:
                c_gauge, c_text = st.columns([1, 1.4])
                
                with c_gauge:
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=proba_succes,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "<b>Probabilité de Conversion</b>", 'font': {'size': 16, 'color': '#1E1B4B'}},
                        number={'suffix': "%", 'font': {'color': '#1E1B4B', 'size': 36}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickcolor': "#0F172A"},
                            'bar': {'color': "#4F46E5"},
                            'bgcolor': "#FFFFFF",
                            'bordercolor': "#E2E8F0",
                            'steps': [
                                {'range': [0, 40], 'color': "#FEE2E2"},
                                {'range': [40, 70], 'color': "#FEF3C7"},
                                {'range': [70, 100], 'color': "#D1FAE5"}
                            ],
                        }
                    ))
                    fig_gauge.update_layout(
                        paper_bgcolor='#FFFFFF',
                        plot_bgcolor='#FFFFFF',
                        height=320,
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True)

                with c_text:
                    st.markdown("<h4 style='color:#1E1B4B;'>💡 Recommandation Stratégique</h4>", unsafe_allow_html=True)
                    if proba_succes >= 70:
                        st.success("🟢 **PROFIL À FORTE APPÉTENCE DIGITALE**\n\n**Action préconisée :** Pousser un parcours 100% autonome via l'application mobile ou Mobile Money. Aucun besoin d'agent physique.")
                    elif proba_succes >= 40:
                        st.warning("🟠 **PROFIL MODÉRÉ (Zone Phygitale)**\n\n**Action préconisée :** Parcours hybride. Engager une prise de contact téléphonique ou WhatsApp pour rassurer avant la clôture en ligne.")
                    else:
                        st.error("🔴 **PROFIL PRÉFÉRANT LE CONTACT HUMAIN**\n\n**Action préconisée :** Orienter vers une agence de proximité ou mandater un courtier terrain pour formaliser le sous-seing.")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<h4 style='color:#1E1B4B;'>🧠 Facteurs explicatifs du score IA</h4>", unsafe_allow_html=True)
                
                importances = modele_rf.feature_importances_
                df_imp = pd.DataFrame({'Critère': features, 'Importance': importances}).sort_values('Importance', ascending=True)
                
                fig_bar_ia = px.bar(
                    df_imp, 
                    x='Importance', 
                    y='Critère', 
                    orientation='h', 
                    title="<b>Poids relatif des critères dans la décision du modèle</b>",
                    labels={'Importance': 'Poids (%)', 'Critère': 'Variables'},
                    color_discrete_sequence=['#4F46E5']
                )
                fig_bar_ia.update_layout(xaxis=dict(tickformat=".1%"))
                st.plotly_chart(style_figure(fig_bar_ia, height=350), use_container_width=True)
            
            with tab2:
                st.markdown("<h4 style='color:#1E1B4B;'>Devis d'Assurance Santé Sur-Mesure</h4>", unsafe_allow_html=True)
                st.write(f"Tarification dynamique calculée pour un profil de **{age_input} ans** résidant en région **{region_input}**.")
                
                str_prime_pure = f"{int(prime_pure):,} FCFA".replace(",", " ")
                str_frais = f"{int(frais):,} FCFA".replace(",", " ")
                str_prime_ttc = f"{int(prime_ttc):,} FCFA".replace(",", " ")
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-val">{str_prime_pure}</div>
                            <div class="metric-lbl">Prime Pure (Risque Pur)</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m2:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-val" style="color:#D97706;">{str_frais}</div>
                            <div class="metric-lbl">Frais de Gestion & Taxes</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-val" style="color:#059669;">{str_prime_ttc}</div>
                            <div class="metric-lbl">Prime Commerciale TTC</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<h4 style='color:#1E1B4B;'>🥧 Structure et Décomposition de la Prime</h4>", unsafe_allow_html=True)
                
                fig_pie_prime = go.Figure(data=[go.Pie(
                    labels=['Prime Pure (Couverture du Risque)', 'Frais de Gestion & Taxes'],
                    values=[prime_pure, frais],
                    hole=.4,
                    marker_colors=['#059669', '#F59E0B'],
                    textfont=dict(color='#FFFFFF', size=13)
                )])
                st.plotly_chart(style_figure(fig_pie_prime, height=380), use_container_width=True)

                st.info("💡 **Transparence Actuarielle :** La Prime Pure repose sur le modèle de fréquence/coût moyen selon les facteurs de risque régionaux et démographiques du Cameroun. Les frais incluent le chargement commercial et la réglementation fiscale.")
            
            st.markdown('</div>', unsafe_allow_html=True)