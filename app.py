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

# Configuration de la page
st.set_page_config(page_title="LeadHunter | Dashboard", page_icon="🟢", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Circular:wght@400;700&display=swap');
    .stApp { background: linear-gradient(180deg, #121212 0%, #000000 100%); color: white; }
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #282828; }
    .spotify-green { color: #1DB954; }
    
    .stButton button { 
        background-color: #1DB954 !important; color: white !important; 
        border-radius: 500px !important; padding: 10px 30px !important;
        font-weight: 700 !important; border: none !important; transition: 0.3s;
        width: 100%;
    }
    .stButton button:hover { transform: scale(1.02); background-color: #1ed760 !important; }

    .premium-box {
        background: #181818; padding: 20px; border-radius: 15px;
        border: 1px solid #1DB954; margin-bottom: 20px;
    }
    .price-tag { font-size: 24px; font-weight: 800; color: #1DB954; margin-bottom: 10px; }
    .benefit-item { font-size: 14px; margin-bottom: 8px; color: #b3b3b3; }
    
    .stripe-link {
        display: block; background-color: #ffffff; color: #000000 !important;
        text-align: center; padding: 14px; border-radius: 500px;
        text-decoration: none; font-weight: 800; margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- POP-UP D'ACCUEIL ---
@st.dialog("🔥 PASSEZ AU NIVEAU SUPÉRIEUR")
def welcome_modal():
    st.markdown("""
        <div style='text-align:center;'>
            <h2 class='spotify-green'>LeadHunter Premium</h2>
            <p style='font-size:16px;'>Arrêtez de chercher vos clients à la main. Laissez l'IA le faire pour vous en illimité.</p>
            <hr style='border: 0.5px solid #282828;'>
            <div style='text-align:left; background:#181818; padding:15px; border-radius:10px;'>
                <p>✅ <b>Volume Massif :</b> 50+ prospects par recherche (vs 3 en gratuit).</p>
                <p>✅ <b>Export CSV :</b> Téléchargez vos listes pour Excel ou vos CRM.</p>
                <p>✅ <b>Filtres Business :</b> Extraction ciblée des emails et numéros.</p>
            </div>
            <h3 style='margin-top:20px;'>29€ <span style='font-size:14px; color:#b3b3b3;'>/ mois</span></h3>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("DÉBLOQUER L'ACCÈS ILLIMITÉ", "https://buy.stripe.com/00w5kD1JWedb9DId082Ji00")

if 'popup_shown' not in st.session_state:
    welcome_modal()
    st.session_state.popup_shown = True

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='spotify-green'>LeadHunter</h2>", unsafe_allow_html=True)
    
    if 'premium_active' not in st.session_state:
        st.session_state.premium_active = False

    # Zone de Code
    user_code = st.text_input("🔑 Code d'activation", type="password", placeholder="cs_live_...")
    if user_code:
        if verifier_paiement_stripe(user_code):
            st.session_state.premium_active = True
            st.success("Abonnement Actif ✅")
        else:
            st.error("Code invalide")

    # Présentation des Avantages si non-Premium
    if not st.session_state.premium_active:
        st.markdown("""
            <div class="premium-box">
                <p style="font-size:10px; font-weight:800; color:#1DB954; letter-spacing:1px;">OFFRE EXCLUSIVE</p>
                <div class="price-tag">29€ / mois</div>
                <div class="benefit-item">🚀 <b>50 résultats</b> par clic</div>
                <div class="benefit-item">📂 <b>Export CSV</b> illimité</div>
                <div class="benefit-item">🎯 <b>Leads qualifiés</b> B2B</div>
                <div class="benefit-item">🛠 <b>Support</b> 24/7</div>
                <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="stripe-link" target="_blank">S'ABONNER</a>
            </div>
        """, unsafe_allow_html=True)
    
    limit = 50 if st.session_state.premium_active else 3

# --- CONTENU PRINCIPAL ---
st.markdown("<h1>Générez des <span class='spotify-green'>Ventes</span></h1>", unsafe_allow_html=True)

query = st.text_input("", placeholder="Niche + Ville (ex: Agence Web Lyon)", label_visibility="collapsed")

if st.button("LANCER L'EXTRACTION"):
    if query:
        with st.spinner('Recherche des meilleures opportunités...'):
            try:
                results = []
                with DDGS() as ddgs:
                    search_results = ddgs.text(f"{query} contact business info", max_results=limit)
                    for r in search_results:
                        results.append({"Nom": r['title'], "Lien": r['href'], "Détails": r['body']})
                
                if results:
                    st.write(f"### {len(results)} Prospects trouvés")
                    for res in results:
                        st.markdown(f"""
                            <div style="background:#181818; padding:15px; border-radius:10px; margin-bottom:10px; border:1px solid #282828;">
                                <h4 style="margin:0; color:#1DB954;">{res['Nom']}</h4>
                                <p style="font-size:12px; color:#b3b3b3;">{res['Détails'][:200]}...</p>
                                <a href="{res['Lien']}" target="_blank" style="color:white; font-size:12px; text-decoration:none;">Voir
