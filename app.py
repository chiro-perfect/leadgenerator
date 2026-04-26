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
st.set_page_config(page_title="LeadHunter | Premium Dashboard", page_icon="🟢", layout="wide")

# --- STYLE CSS AVANCÉ (LE SECRET DU BEAU SITE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Circular:wght@400;700&family=Inter:wght@400;800&display=swap');
    
    .stApp { background: linear-gradient(180deg, #121212 0%, #000000 100%); color: white; }
    
    /* Animation du bouton */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(29, 185, 84, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(29, 185, 84, 0); }
        100% { box-shadow: 0 0 0 0 rgba(29, 185, 84, 0); }
    }

    /* Le Bouton S'abonner Ultra-Design */
    .cta-premium {
        display: block;
        background-color: #1DB954;
        color: white !important;
        padding: 18px 30px;
        border-radius: 500px;
        text-decoration: none;
        font-weight: 800;
        font-size: 18px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: none;
        animation: pulse-green 2s infinite;
        margin: 20px 0;
        width: 100%;
    }
    .cta-premium:hover {
        background-color: #1ed760;
        transform: scale(1.03);
        box-shadow: 0 10px 25px rgba(29, 185, 84, 0.5);
    }

    /* Carte d'avantages dans le pop-up */
    .benefit-row {
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.05);
        padding: 12px 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 3px solid #1DB954;
    }
    .benefit-icon { font-size: 20px; margin-right: 15px; }

    .price-big {
        font-family: 'Inter', sans-serif;
        font-size: 42px;
        font-weight: 800;
        color: white;
        margin: 10px 0;
    }
    .price-sub { font-size: 14px; color: #b3b3b3; font-weight: 400; }
    
    /* Titres de page */
    .spotify-green { color: #1DB954; }
    h1 { font-weight: 800; letter-spacing: -1px; }
    
    /* Correction du design de la sidebar */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #282828;
    }
    
    /* Correction des cartes de résultats */
    .prospect-card {
        background: #181818;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #282828;
    }
    </style>
    """, unsafe_allow_html=True)

# --- POP-UP DE VENTE (DIALOG) ---
@st.dialog("⚡️ DÉBLOQUE LEADHUNTER FULL ACCÈS")
def premium_modal():
    # C'EST ICI QU'ON UTILISE LE MARKDOWN CORRECTEMENT
    st.markdown("""
        <div style='text-align:center;'>
            <p style='color:#1DB954; font-weight:700; letter-spacing:2px; font-size:12px; margin-bottom:5px;'>OFFRE DE LANCEMENT</p>
            <h1 style='margin-top:0; color:white;'>Prospectez 10x plus vite.</h1>
            
            <div style='margin: 25px 0; text-align: left;'>
                <div class='benefit-row'>
                    <span class='benefit-icon'>🚀</span>
                    <span><b>50+ prospects</b> par recherche (vs 3 en gratuit)</span>
                </div>
                <div class='benefit-row'>
                    <span class='benefit-icon'>📥</span>
                    <span><b>Export CSV Illimité</b> pour Excel et CRM</span>
                </div>
                <div class='benefit-row'>
                    <span class='benefit-icon'>🤖</span>
                    <span><b>Algorithme IA</b> de recherche profonde</span>
                </div>
            </div>

            <div class='price-big'>29€<span class='price-sub'> / mois</span></div>
            <p style='color:#b3b3b3; font-size:13px; margin-bottom:20px;'>Annulable à tout moment • Activation instantanée</p>
            
            <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="cta-premium" target="_blank">S'ABONNER MAINTENANT</a>
            
            <p style='font-size:10px; color:#535353; margin-top:15px;'>Paiement sécurisé crypté par Stripe &copy;</p>
        </div>
    """, unsafe_allow_html=True) # <-- NE SURTOUT PAS OUBLIER ÇA

# Affichage automatique une seule fois
if 'popup_shown' not in st.session_state:
    premium_modal()
    st.session_state.popup_shown = True

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='spotify-green' style='font-size:30px; margin-bottom:10px;'>LeadHunter</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if 'premium_active' not in st.session_state:
        st.session_state.premium_active = False

    user_code = st.text_input("🔑 Code d'activation (reçu par mail)", type="password")
    
    if user_code:
        with st.spinner("Vérification en direct..."):
            if verifier_paiement_stripe(user_code):
                st.session_state.premium_active = True
                st.success("Accès Premium : ACTIF ✅")
            else:
                st.error("Code invalide ou expiré")

    if not st.session_state.premium_active:
        st.markdown("""
            <div style="background:#181818; padding:20px; border-radius:15px; border: 1px solid #1DB954; margin-top:20px; text-align:center;">
                <p style="font-size:11px; font-weight:800; color:#1DB954; letter-spacing:1px; margin-bottom:5px;">MODE LIMITÉ</p>
                <h3 style="margin:5px 0;">29€ / mois</h3>
                <p style="font-size:12px; color:#b3b3b3; margin-bottom:15px;">DÉBLOQUEZ L'ILLIMITÉ</p>
                <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="cta-premium" style="font-size:12px; padding:12px;" target="_blank">PASSER PREMIUM</a>
            </div>
        """, unsafe_allow_html=True)

# --- RECHERCHE ET RÉSULTATS ---
st.markdown("<h1>Explosez vos <span class='spotify-green'>Résultats</span></h1>", unsafe_allow_html=True)

query = st.text_input("", placeholder="Niche + Ville (ex: Plombier Lyon)", label_visibility="collapsed")
limit = 50 if st.session_state.premium_active else 3

if st.button("GÉNÉRER LA LISTE"):
    if query:
        with st.spinner('Extraction des prospects en cours...'):
            try:
                results = []
                with DDGS() as ddgs:
                    # Recherche optimisée
                    search_results = ddgs.text(f"{query} contact email business", max_results=limit)
                    for r in search_results:
                        results.append({"Nom": r['title'], "Lien": r['href'], "Détails": r['body']})
                
                if results:
                    st.write(f"### Résultats ({'Premium' if st.session_state.premium_active else 'Version Gratuite 3/50'})")
                    for res in results:
                        st.markdown(f"""
                            <div class="prospect-card">
                                <h4 style="margin:0; color:#1DB954;">{res['Nom']}</h4>
                                <p style="font-size:13px; color:#b3b3b3; margin:8px 0;">{res['Détails'][:200]}...</p>
                                <a href="{res['Lien']}" target="_blank" style="color:white; font-size:12px;">Visiter le site 🔗</a>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    if st.session_state.premium_active:
                        csv = pd.DataFrame(results).to_csv(index=False).encode('utf-8')
                        st.download_button("📥 TÉLÉCHARGER LE CSV", data=csv, file_name="leads_premium.csv")
                    else:
                        st.info("💡 Limite atteinte. Pour voir 50 résultats et télécharger le fichier CSV, passez Premium pour 29€/mois.")
                else:
                    st.warning("Aucun prospect trouvé. Essayez une autre niche.")
            except:
                st.error("Erreur de connexion. Veuillez réessayer dans quelques instants.")
    else:
        st.warning("Veuillez entrer une recherche.")
