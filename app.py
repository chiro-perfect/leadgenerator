import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
import stripe

# --- CONFIGURATION STRIPE ---
# Ta clé Live pour la vérification réelle
stripe.api_key = "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"

def verifier_paiement_stripe(checkout_id):
    """Vérifie si l'ID de session Stripe est valide et payé"""
    # Sécurité de base sur le format
    if not checkout_id or not checkout_id.startswith("cs_"):
        return False
    try:
        # On interroge l'API Stripe
        session = stripe.checkout.Session.retrieve(checkout_id)
        if session.payment_status == "paid":
            return True
        return False
    except Exception:
        # En cas d'ID inexistant ou erreur réseau
        return False

# Configuration de la page
st.set_page_config(
    page_title="LeadHunter | Dashboard Premium",
    page_icon="🟢",
    layout="wide"
)

# --- STYLE CSS SPOTIFY PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Circular:wght@400;700&family=Inter:wght@400;700&display=swap');

    .stApp {
        background: linear-gradient(180deg, #121212 0%, #000000 100%);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #282828;
    }

    .spotify-green { color: #1DB954; }

    /* Boutons et inputs style Spotify */
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

    .stTextInput input {
        background-color: #2a2a2a !important;
        color: white !important;
        border-radius: 500px !important;
        border: 1px solid transparent !important;
    }

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
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='spotify-green'>LeadHunter</h2>", unsafe_allow_html=True)
    st.write(" ")
    
    # Gestion du verrouillage Premium
    st.markdown("🔒 **STATUT DU COMPTE**")
    
    # On initialise l'état premium
    if 'premium_active' not in st.session_state:
        st.session_state.premium_active = False

    user_code = st.text_input("Code Premium (Reçu par mail)", type="password", placeholder="cs_live_...")
    
    if user_code:
        if verifier_paiement_stripe(user_code):
            st.session_state.premium_active = True
            st.success("Mode Premium Actif ✅")
        else:
            st.session_state.premium_active = False
            st.error("Code invalide ou expiré")

    if not st.session_state.premium_active:
        st.markdown("""
            <div style="background:#282828; padding:15px; border-radius:10px; margin-top:10px;">
                <p style="font-size:12px; font-weight:700;">PASSEZ À L'ILLIMITÉ</p>
                <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="stripe-button" target="_blank">OBTENIR UN CODE</a>
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
                    # Recherche optimisée pour trouver des contacts
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
                    st.warning("Aucun résultat pour cette recherche.")
            except:
                st.error("Erreur de recherche. Réessayez.")
    else:
        st.info("Entrez une thématique pour commencer.")
