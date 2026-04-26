import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
import stripe

# --- CONFIGURATION STRIPE ---
# Ta clé Live pour la vérification réelle
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
st.set_page_config(page_title="LeadHunter | Dashboard Premium", page_icon="🟢", layout="wide")

# --- STYLE CSS SPOTIFY PREMIUM ---
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
    .price-tag { font-size: 24px; font-weight: 800; color: #1DB954; margin-bottom: 5px; }
    .benefit-item { font-size: 14px; margin-bottom: 8px; color: #b3b3b3; }
    
    .stripe-link {
        display: block; background-color: #ffffff; color: #000000 !important;
        text-align: center; padding: 14px; border-radius: 500px;
        text-decoration: none; font-weight: 800; margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- POP-UP D'ACCUEIL ---
@st.dialog("🔥 OFFRE LEADHUNTER PREMIUM")
def welcome_modal():
    st.markdown("""
        <div style='text-align:center;'>
            <h2 class='spotify-green'>Passez à la vitesse supérieure</h2>
            <p>Obtenez des listes de clients qualifiés en quelques secondes.</p>
            <div style='text-align:left; background:#181818; padding:15px; border-radius:10px; border:1px solid #282828;'>
                <p>🚀 <b>50+ leads</b> par recherche (vs 3 en gratuit)</p>
                <p>📥 <b>Export CSV</b> illimité pour Excel/CRM</p>
                <p>🎯 <b>Emails & Contacts</b> directs extraits</p>
            </div>
            <h3 style='margin-top:20px;'>29€ <span style='font-size:14px; color:#b3b3b3;'>/ mois</span></h3>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("S'ABONNER MAINTENANT", "https://buy.stripe.com/00w5kD1JWedb9DId082Ji00")

if 'popup_shown' not in st.session_state:
    welcome_modal()
    st.session_state.popup_shown = True

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='spotify-green'>LeadHunter</h2>", unsafe_allow_html=True)
    
    if 'premium_active' not in st.session_state:
        st.session_state.premium_active = False

    user_code = st.text_input("🔑 Code d'activation", type="password", placeholder="cs_live_...")
    if user_code:
        if verifier_paiement_stripe(user_code):
            st.session_state.premium_active = True
            st.success("Abonnement Actif ✅")
        else:
            st.session_state.premium_active = False
            st.error("Code invalide")

    if not st.session_state.premium_active:
        st.markdown("""
            <div class="premium-box">
                <p style="font-size:10px; font-weight:800; color:#1DB954;">OFFRE ILLIMITÉE</p>
                <div class="price-tag">29€ / mois</div>
                <div class="benefit-item">🚀 50 leads par clic</div>
                <div class="benefit-item">📂 Export CSV illimité</div>
                <div class="benefit-item">🎯 Prospection automatisée</div>
                <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="stripe-link" target="_blank">PASSER PREMIUM</a>
            </div>
        """, unsafe_allow_html=True)
    
    limit = 50 if st.session_state.premium_active else 3

# --- CONTENU PRINCIPAL ---
st.markdown("<h1>Générez vos <span class='spotify-green'>Leads</span></h1>", unsafe_allow_html=True)

query = st.text_input("", placeholder="Niche + Ville (ex: Coach sportif Paris)", label_visibility="collapsed")

if st.button("LANCER L'EXTRACTION"):
    if query:
        with st.spinner('Extraction en cours...'):
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
                            <div style="background:#181818; padding:15px; border-radius:10px; margin-bottom:10px; border:1px solid #282828;">
                                <h4 style="margin:0; color:#1DB954;">{res['Nom']}</h4>
                                <p style="font-size:12px; color:#b3b3b3;">{res['Détails'][:200]}...</p>
                                <a href="{res['Lien']}" target="_blank" style="color:white; font-size:12px; text-decoration:none;">Voir le site 🔗</a>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    if st.session_state.premium_active:
                        csv = pd.DataFrame(results).to_csv(index=False).encode('utf-8')
                        st.download_button("📥 TÉLÉCHARGER LE CSV", data=csv, file_name="leads_export.csv", mime="text/csv")
                    else:
                        st.info("💡 Limite gratuite de 3 leads atteinte. Passez Premium (29€/mois) pour débloquer 50+ leads et l'export CSV.")
                else:
                    st.warning("Aucun résultat trouvé.")
            except Exception:
                st.error("Erreur de connexion.")
    else:
        st.warning("Veuillez entrer une recherche.")
