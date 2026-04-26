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

# --- DESIGN DU SITE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background: radial-gradient(circle at top center, #1a1a1a 0%, #000000 100%); color: white; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: rgba(0,0,0,0.8) !important; border-right: 1px solid #333; }
    .sidebar-premium-card { background: linear-gradient(145deg, #181818, #111); padding: 20px; border-radius: 15px; border: 1px solid #1DB954; text-align: center; margin-top: 20px; }
    .spotify-green { color: #1DB954; font-weight: 800; }
    .stButton button { background-color: #1DB954 !important; color: white !important; border-radius: 500px !important; padding: 10px 30px !important; font-weight: 700 !important; border: none !important; width: 100%; }
    .result-card { background: rgba(255,255,255,0.03); padding: 20px; border-radius: 12px; border: 1px solid #222; margin-bottom: 15px; }
    .white-btn { display: block; background: white; color: black !important; text-align: center; padding: 12px; border-radius: 500px; text-decoration: none; font-weight: 700; font-size: 14px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- POP-UP ---
@st.dialog("🚀 OFFRE DE LANCEMENT")
def welcome_modal():
    st.markdown("""
        <div style='text-align:center;'>
            <h2 style='color:white;'>Passez à l'illimité</h2>
            <p style='color:#b3b3b3;'>Extrayez des listes massives de clients potentiels.</p>
            <div style='background:#1DB95422; padding:20px; border-radius:15px; border:1px solid #1DB954; margin: 20px 0;'>
                <h3 style='margin:0; color:#1DB954;'>29€ / mois</h3>
                <ul style='text-align:left; font-size:14px; margin-top:15px; color:white;'>
                    <li>✅ 50+ prospects par recherche</li>
                    <li>✅ Export CSV (Excel) en 1 clic</li>
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

    if not st.session_state.premium_active:
        st.markdown("""
            <div class="sidebar-premium-card">
                <h3 style="margin:10px 0; color:white;">29€ / mois</h3>
                <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="white-btn" target="_blank">DEVENIR PREMIUM</a>
            </div>
        """, unsafe_allow_html=True)

# --- CORRECTION DU BOUTON RECHERCHE ---
st.markdown("<h1 style='font-size:50px; font-weight:800;'>Trouvez vos <span class='spotify-green'>Clients.</span></h1>", unsafe_allow_html=True)
query = st.text_input("Recherche", placeholder="Ex: Agence immobilière Paris", label_visibility="collapsed")

if st.button("LANCER LA RECHERCHE"):
    if not query:
        st.warning("⚠️ Veuillez entrer un mot-clé (ex: Plombier Lyon)")
    else:
        with st.spinner('Extraction des prospects en cours...'):
            try:
                results = []
                limit = 50 if st.session_state.premium_active else 3
                
                # Correction majeure ici : on force l'initialisation de DDGS
                with DDGS() as ddgs:
                    ddgs_gen = ddgs.text(f"{query} business contact info", max_results=limit)
                    for r in ddgs_gen:
                        results.append(r)
                
                if results:
                    st.success(f"✅ {len(results)} Prospects identifiés !")
                    for res in results:
                        st.markdown(f"""
                            <div class="result-card">
                                <h4 style="margin:0; color:#1DB954;">{res.get('title', 'Sans nom')}</h4>
                                <p style="font-size:13px; color:#bbb; margin:10px 0;">{res.get('body', '')[:200]}...</p>
                                <a href="{res.get('href', '#')}" target="_blank" style="color:white; font-size:12px;">Visiter le site 🔗</a>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    if st.session_state.premium_active:
                        df = pd.DataFrame(results)
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 EXPORTER EN CSV", data=csv, file_name="leads.csv", mime="text/csv")
                else:
                    st.error("❌ Aucun résultat trouvé. Essayez avec d'autres mots-clés.")
                    
            except Exception as e:
                # Cela affichera l'erreur exacte si le moteur de recherche bloque
                st.error(f"Une erreur est survenue : {str(e)}")
                st.info("💡 Conseil : Si l'erreur persiste, c'est peut-être que DuckDuckGo bloque temporairement les requêtes trop rapides.")
