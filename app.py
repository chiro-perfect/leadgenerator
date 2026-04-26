import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
import stripe

# --- CONFIGURATION STRIPE ---
# Ta clé API Live Stripe
stripe.api_key = "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"

def verifier_paiement_stripe(checkout_id):
    """Vérifie si l'ID de session Stripe est valide et payé"""
    if not checkout_id or not checkout_id.startswith("cs_"):
        return False
    try:
        session = stripe.checkout.Session.retrieve(checkout_id)
        return session.payment_status == "paid"
    except Exception:
        return False

# Configuration de la page
st.set_page_config(
    page_title="LeadHunter | Dashboard",
    page_icon="🟢",
    layout="wide"
)

# --- STYLE CSS (LE PREMIER STYLE PLUS SOBRE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Circular:wght@400;700&display=swap');

    .stApp {
        background: linear-gradient(180deg, #121212 0%, #000000 100%);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #282828;
    }

    .spotify-green { color: #1DB954; }

    .stButton button {
        background-color: #1DB954 !important;
        color: white !important;
        border-radius: 500px !important;
        padding: 12px 35px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.3s;
    }
    
    .stButton button:hover { transform: scale(1.05); background-color: #1ed760 !important; }

    .prospect-card {
        background: #181818;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #282828;
    }
    
    .stripe-button {
        display: block;
        background-color: #ffffff;
        color: #000000 !important;
        padding: 12px;
        text-align: center;
        border-radius: 500px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13px;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LE PREMIER POP-UP (RETOUR AUX SOURCES) ---
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
            <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="stripe-button" target="_blank">OBTENIR UN CODE MAINTENANT</a>
        </div>
    """, unsafe_allow_html=True)

if 'popup_shown' not in st.session_state:
    welcome_modal()
    st.session_state.popup_shown = True

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='spotify-green'>LeadHunter</h2>", unsafe_allow_html=True)
    st.write(" ")
    
    if 'premium_active' not in st.session_state:
        st.session_state.premium_active = False

    user_code = st.text_input("Code Premium (Reçu par mail)", type="password", placeholder="cs_live_...")
    
    if user_code:
        if verifier_paiement_stripe(user_code):
            st.session_state.premium_active = True
            st.success("Mode Premium Actif ✅")
        else:
            st.error("Code invalide ou expiré")

    if not st.session_state.premium_active:
        st.markdown("""
            <div style="background:#282828; padding:15px; border-radius:10px; margin-top:10px;">
                <p style="font-size:12px; font-weight:700; color:white; margin:0;">DÉBLOQUER L'ILLIMITÉ</p>
                <p style="font-size:11px; color:#b3b3b3;">Accédez à 50 leads et export CSV.</p>
                <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="stripe-button" target="_blank">PASSER PREMIUM</a>
            </div>
        """, unsafe_allow_html=True)

    limit = 50 if st.session_state.premium_active else 3

# --- CONTENU PRINCIPAL ---
st.markdown("<h1>Rechercher vos <span class='spotify-green'>Leads</span></h1>", unsafe_allow_html=True)

query = st.text_input("", placeholder="Niche + Ville (ex: Plombier Bordeaux)", label_visibility="collapsed")

if st.button("GÉNÉRER LA LISTE"):
    if query:
        with st.spinner('Recherche en cours...'):
            try:
                results = []
                with DDGS() as ddgs:
                    search_results = ddgs.text(f"{query} contact email business", max_results=limit)
                    for r in search_results:
                        results.append({"Nom": r['title'], "Lien": r['href'], "Détails": r['body']})
                
                if results:
                    st.write(f"### {len(results)} Prospects trouvés")
                    for res in results:
                        st.markdown(f"""
                            <div class="prospect-card">
                                <h4 style="margin:0; color:#1DB954;">{res['Nom']}</h4>
                                <p style="font-size:13px; color:#b3b3b3;">{res['Détails'][:200]}...</p>
                                <a href="{res['Lien']}" target="_blank" style="color:white; text-decoration:none;">Lien vers le site 🔗</a>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    if st.session_state.premium_active:
                        csv = pd.DataFrame(results).to_csv(index=False).encode('utf-8')
                        st.download_button("📥 TÉLÉCHARGER LE CSV", data=csv, file_name="leads_pro.csv", mime="text/csv")
                    else:
                        st.warning("💡 Limite gratuite de 3 résultats. Passez Premium pour voir 50 résultats et télécharger le fichier CSV.")
                else:
                    st.warning("Aucun résultat pour cette recherche.")
            except:
                st.error("Erreur de recherche. Réessayez.")
    else:
        st.info("Entrez une thématique pour commencer.")
