import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS

# Configuration de la page
st.set_page_config(
    page_title="LeadHunter | Dashboard",
    page_icon="🟢",
    layout="wide"
)

# --- STYLE CSS SPOTIFY PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Circular:wght@400;700&family=Inter:wght@400;700&display=swap');

    /* Fond principal sombre Spotify */
    .stApp {
        background: linear-gradient(180deg, #121212 0%, #000000 100%);
        color: white;
    }

    /* Sidebar noire */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #282828;
    }

    /* Titres */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
    }

    /* Le fameux Vert Spotify */
    .spotify-green {
        color: #1DB954;
    }

    /* Bouton principal (Play Style) */
    .stButton button {
        background-color: #1DB954 !important;
        color: white !important;
        border-radius: 500px !important; /* Très arrondi comme Spotify */
        padding: 12px 35px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #1ed760 !important;
        transform: scale(1.05);
    }

    /* Barre de recherche style Spotify */
    .stTextInput input {
        background-color: #2a2a2a !important;
        color: white !important;
        border-radius: 500px !important;
        border: 1px solid transparent !important;
        padding: 12px 25px !important;
    }
    
    .stTextInput input:focus {
        border: 1px solid #ffffff !important;
    }

    /* Cartes de résultats (Album Style) */
    .prospect-card {
        background: #181818;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        transition: background 0.3s ease;
        border: 1px solid #282828;
    }
    
    .prospect-card:hover {
        background: #282828;
    }

    /* Bouton Stripe Premium */
    .stripe-button {
        display: block;
        background-color: #ffffff;
        color: #000000 !important;
        padding: 14px;
        text-align: center;
        border-radius: 500px;
        text-decoration: none;
        font-weight: 700;
        margin-top: 15px;
        font-size: 14px;
    }

    /* Cacher le menu Streamlit pour plus de pro */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 class='spotify-green'>LeadHunter</h2>", unsafe_allow_html=True)
    st.write(" ")
    st.markdown("🏠 **Accueil**")
    st.markdown("🔍 **Rechercher**")
    st.markdown("📚 **Ma Bibliothèque**")
    st.write("---")
    
    plan = st.radio("Abonnement actuel", ["Standard", "Premium ✨"])
    
    if plan == "Standard":
        st.markdown("""
            <div style="background:#282828; padding:15px; border-radius:10px;">
                <p style="font-size:12px; font-weight:700;">DÉBLOQUEZ TOUT</p>
                <p style="font-size:11px;">Accédez à 50+ prospects et exportez en CSV.</p>
                <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="stripe-button" target="_blank">PASSER AU PREMIUM</a>
            </div>
        """, unsafe_allow_html=True)
        limit = 3
    else:
        password = st.text_input("Code Premium", type="password", placeholder="Entrez votre code")
        if password == "LEAD2026":
            st.success("Mode Premium Actif")
            limit = 50
        else:
            st.error("Code requis")
            limit = 3

# --- CONTENU PRINCIPAL ---
st.markdown("<h1>Rechercher vos <span class='spotify-green'>Leads</span></h1>", unsafe_allow_html=True)

# Barre de recherche type "Spotify Search"
query = st.text_input("", placeholder="Cherchez une niche (ex: Coach sportif Lyon)", label_visibility="collapsed")

if st.button("LANCER LA PLAYLIST"):
    if query:
        with st.spinner('Chargement des meilleurs prospects...'):
            try:
                results = []
                with DDGS() as ddgs:
                    search_results = ddgs.text(f"{query} contact business", max_results=limit)
                    for r in search_results:
                        results.append({
                            "Nom": r['title'],
                            "Lien": r['href'],
                            "Détails": r['body']
                        })
                
                if results:
                    st.write(f"### Résultats pour : {query}")
                    for res in results:
                        st.markdown(f"""
                            <div class="prospect-card">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <div>
                                        <h4 style="margin:0; color:#1DB954;">{res['Nom']}</h4>
                                        <p style="font-size:13px; color:#b3b3b3; margin:5px 0;">{res['Détails'][:180]}...</p>
                                    </div>
                                    <a href="{res['Lien']}" target="_blank" style="color:white; font-size:20px; text-decoration:none;">▶️</a>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Action de fin
                    df = pd.DataFrame(results)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 TÉLÉCHARGER LA PLAYLIST (CSV)", data=csv, file_name="leads_premium.csv", mime="text/csv")
                else:
                    st.info("Aucun prospect trouvé dans cette catégorie.")
            except:
                st.error("Connexion interrompue. Réessayez.")
    else:
        st.warning("Veuillez entrer un nom de domaine ou une ville.")

# Pied de page
st.markdown("<br><br><p style='text-align: center; color: #535353; font-size: 11px;'>LeadHunter Premium © 2026</p>", unsafe_allow_html=True)
