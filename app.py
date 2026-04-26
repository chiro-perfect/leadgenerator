import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS

# Configuration de la page
st.set_page_config(
    page_title="LeadHunter | Samsung Style",
    page_icon="📱",
    layout="centered" # Plus élégant pour le style Samsung
)

# --- STYLE CSS ONE UI (SAMSUNG) ---
st.markdown("""
    <style>
    /* Importation d'une police proche de Samsung Sharp Sans */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f4f7f9;
    }

    /* Mode sombre doux de Samsung */
    .stApp {
        background: #f4f7f9;
    }

    /* Conteneur principal arrondi */
    .block-container {
        padding-top: 2rem;
        max-width: 800px;
    }

    /* Titre style Samsung */
    h1 {
        color: #000000;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    /* Champs de saisie arrondis (Samsung Style) */
    .stTextInput input {
        border-radius: 20px !important;
        border: 1px solid #e0e0e0 !important;
        padding: 15px 25px !important;
        background-color: white !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }

    /* Bouton principal arrondi et bleu Samsung */
    .stButton button {
        background-color: #037ffc !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100%;
        transition: transform 0.2s ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(3, 127, 252, 0.2) !important;
    }

    /* Sidebar élégante */
    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #f0f0f0;
    }

    /* Card pour les résultats */
    .prospect-card {
        background: white;
        padding: 20px;
        border-radius: 24px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }

    /* Bouton Stripe style Samsung */
    .stripe-button {
        display: block;
        background: #000000;
        color: white !important;
        padding: 15px;
        text-align: center;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* Bouton téléchargement */
    .stDownloadButton button {
        background-color: #f0f0f0 !important;
        color: #333 !important;
        border-radius: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #000;'>Paramètres</h2>", unsafe_allow_html=True)
    st.write("---")
    
    plan = st.selectbox("Votre compte", ["Version Gratuite", "Version Premium ✨"])
    
    if "Gratuite" in plan:
        st.markdown("""
            <div style="background:#f9f9f9; padding:20px; border-radius:20px; border:1px solid #eee;">
                <p style="color:#666; font-size:14px;">Passez à la vitesse supérieure pour débloquer tous les prospects.</p>
                <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="stripe-button" target="_blank">Acheter Premium</a>
            </div>
        """, unsafe_allow_html=True)
        limit = 3
    else:
        password = st.text_input("Code d'activation", type="password")
        if password == "LEAD2026":
            st.success("Accès Premium activé")
            limit = 50
        else:
            st.error("Code invalide")
            limit = 3

# --- CONTENU PRINCIPAL ---
st.markdown("<h1>LeadHunter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-bottom:40px;'>Trouvez vos clients avec la précision d'un Galaxy.</p>", unsafe_allow_html=True)

# Barre de recherche centrée
query = st.text_input("", placeholder="Rechercher un métier ou une ville...", label_visibility="collapsed")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_clicked = st.button("Rechercher maintenant")

if search_clicked:
    if query:
        with st.spinner('Analyse des données...'):
            try:
                results = []
                with DDGS() as ddgs:
                    # Recherche optimisée
                    search_results = ddgs.text(f"{query} (contact OR email OR phone)", max_results=limit)
                    for r in search_results:
                        results.append({
                            "Nom": r['title'],
                            "Lien": r['href'],
                            "Description": r['body']
                        })
                
                if results:
                    st.write(f"### {len(results)} résultats trouvés")
                    for res in results:
                        st.markdown(f"""
                            <div class="prospect-card">
                                <h4 style="margin:0; color:#037ffc;">{res['Nom']}</h4>
                                <p style="font-size:13px; color:#666; margin:10px 0;">{res['Description'][:200]}...</p>
                                <a href="{res['Lien']}" target="_blank" style="font-size:12px; color:#037ffc; text-decoration:none; font-weight:600;">Voir la source →</a>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Option de téléchargement
                    df = pd.DataFrame(results)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Enregistrer la liste", data=csv, file_name="leads.csv", mime="text/csv")
                else:
                    st.info("Aucun résultat. Essayez d'être plus spécifique.")
            except:
                st.error("Erreur de connexion. Réessayez.")
    else:
        st.warning("Entrez une recherche d'abord.")

# Footer
st.markdown("<br><p style='text-align: center; color: #aaa; font-size: 11px;'>Conçu avec soin pour une expérience fluide.</p>", unsafe_allow_html=True)
