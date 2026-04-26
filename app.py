import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
import stripe

# --- CONFIGURATION STRIPE ---
stripe.api_key = "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"

def verifier_paiement_stripe(checkout_id):
    if not checkout_id or not checkout_id.startswith("cs_"):
        return False
    try:
        session = stripe.checkout.Session.retrieve(checkout_id)
        return session.payment_status == "paid"
    except:
        return False

# Configuration
st.set_page_config(page_title="LeadHunter Pro", page_icon="🟢", layout="wide")

# --- DESIGN DU SITE (MEILLEUR FOND ET SIDEBAR) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    /* Fond de page avec dégradé radial pro */
    .stApp {
        background: radial-gradient(circle at top center, #1a1a1a 0%, #000000 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar stylisée */
    section[data-testid="stSidebar"] {
        background-color: rgba(0,0,0,0.8) !important;
        border-right: 1px solid #333;
    }

    /* Bloc Premium Sidebar amélioré */
    .sidebar-premium-card {
        background: linear-gradient(145deg, #181818, #111);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #1DB954;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    .spotify-green { color: #1DB954; font-weight: 800; }

    /* Boutons */
    .stButton button {
        background-color: #1DB954 !important;
        color: white !important;
        border-radius: 500px !important;
        padding: 10px 30px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.4s;
        width: 100%;
    }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(29, 185, 84, 0.4); }

    /* Cartes de résultats */
    .result-card {
        background: rgba(255,255,255,0.03);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #222;
        margin-bottom: 15px;
    }

    /* Lien style bouton blanc */
    .white-btn {
        display: block;
        background: white;
        color: black !important;
        text-align: center;
        padding: 12px;
        border-radius: 500px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ANCIEN POP-UP (GARDE COMME DEMANDÉ) ---
@st.dialog("🚀 OFFRE DE LANCEMENT")
def welcome_modal():
    st.markdown("""
        <div style='text-align:center;'>
            <h2 style='color:white;'>Passez à l'illimité</h2>
            <p style='font-size:16px; color:#b3b3b3;'>Ne vous contentez pas de 3 résultats. Extrayez des listes massives de clients potentiels pour votre business.</p>
            <div style='background:#1DB95422; padding:20px; border-radius:15px; border:1px solid #1DB954; margin: 20px 0;'>
                <h3 style='margin:0; color:#1DB954;'>29€ / mois</h3>
                <ul style='text-align:left; font-size:14px; margin-top:15px; color:white;'>
                    <li>✅ 50+ prospects par recherche</li>
                    <li>✅ Export CSV (Excel) en 1 clic</li>
                    <li>✅ Accès complet aux algorithmes</li>
                </ul>
            </div>
            <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="white-btn" target="_blank">OBTENIR MON CODE</a>
        </div>
    """, unsafe_allow_html=True)

if 'popup_shown' not in st.session_state:
    welcome_modal()
    st.session_state.popup_shown = True

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='spotify-green' style='font-size:32px;'>LeadHunter</h2>", unsafe_allow_html=True)
    
    if 'premium_active' not in st.session_state:
        st.session_state.premium_active = False

    user_code = st.text_input("Activation Premium", type="password", placeholder="cs_live_...")
    
    if user_code:
        if verifier_paiement_stripe(user_code):
            st.session_state.premium_active = True
            st.success("Accès Premium Actif")
        else:
            st.error("Code invalide")

    # Nouveau design du bloc Premium à gauche
    if not st.session_state.premium_active:
        st.markdown("""
            <div class="sidebar-premium-card">
                <span style="font-size:10px; color:#1DB954; font-weight:800; letter-spacing:1px;">VERSION LIMITÉE</span>
                <h3 style="margin:10px 0; color:white;">29€ / mois</h3>
                <p style="font-size:12px; color:#888;">Libérez la puissance totale de l'IA.</p>
                <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="white-btn" target="_blank">DEVENIR PREMIUM</a>
            </div>
        """, unsafe_allow_html=True)

# --- MAIN ---
st.markdown("<h1 style='font-size:50px; font-weight:800;'>Trouvez vos <span class='spotify-green'>Clients.</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#888; margin-top:-20px;'>L'outil ultime pour extraire des leads B2B en quelques secondes.</p>", unsafe_allow_html=True)

query = st.text_input("", placeholder="Ex: Agence immobilière Paris", label_visibility="collapsed")
limit = 50 if st.session_state.premium_active else 3

if st.button("LANCER LA RECHERCHE"):
    if query:
        with st.spinner('Extraction des données...'):
            try:
                results = []
                with DDGS() as ddgs:
                    search_results = ddgs.text(f"{query} business contact", max_results=limit)
                    for r in search_results:
                        results.append({"Nom": r['title'], "Lien": r['href'], "Détails": r['body']})
                
                if results:
                    st.write(f"### {len(results)} Prospects identifiés")
                    for res in results:
                        st.markdown(f"""
                            <div class="result-card">
                                <h4 style="margin:0; color:#1DB954;">{res['Nom']}</h4>
                                <p style="font-size:13px; color:#bbb; margin:10px 0;">{res['Détails'][:200]}...</p>
                                <a href="{res['Lien']}" target="_blank" style="color:white; font-size:12px; text-decoration:none;">Visiter le site 🔗</a>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    if st.session_state.premium_active:
                        csv = pd.DataFrame(results).to_csv(index=False).encode('utf-8')
                        st.download_button("📥 EXPORTER EN CSV", data=csv, file_name="leads.csv", mime="text/csv")
                    else:
                        st.info("💡 Vous êtes limité à 3 résultats. Passez Premium pour voir les 50 prospects et exporter le fichier.")
            except:
                st.error("Erreur. Veuillez réessayer.")
