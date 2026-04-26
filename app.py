import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
import base64

# Configuration de la page
st.set_page_config(
    page_title="LeadHunter Pro | Machine à Prospects",
    page_icon="🚀",
    layout="wide"
)

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    /* Background général */
    .main {
        background-color: #0e1117;
    }
    
    /* Titre principal */
    h1 {
        color: #00d4ff;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Style des boutons de téléchargement */
    .stDownloadButton button {
        background-color: #00d4ff !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100%;
    }

    /* Sidebar stylisée */
    .css-1d391kg {
        background-color: #161b22;
    }

    /* Cartes de résultats */
    .result-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
        margin-bottom: 15px;
    }
    
    /* Bouton Stripe personnalisé */
    .stripe-button {
        display: inline-block;
        background: linear-gradient(90deg, #6772E5, #7795f8);
        color: white;
        padding: 12px 24px;
        font-weight: bold;
        text-decoration: none;
        border-radius: 8px;
        text-align: center;
        width: 100%;
        box-shadow: 0 4px 15px rgba(103, 114, 229, 0.3);
    }
    .stripe-button:hover {
        background: linear-gradient(90deg, #7795f8, #6772E5);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & ABONNEMENT ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1055/1055644.png", width=100)
st.sidebar.title("💎 Mon Forfait")

plan = st.sidebar.selectbox("Choisir votre accès", ["Gratuit (3 résultats)", "Premium (Illimité)"])

if plan == "Gratuit (3 résultats)":
    st.sidebar.info("Limite actuelle : 3 résultats par recherche.")
    st.sidebar.markdown(f"""
        <a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" class="stripe-button" target="_blank">
            🔥 DEVENIR PREMIUM (29€)
        </a>
    """, unsafe_allow_html=True)
    limit = 3
else:
    # Système de verrouillage
    st.sidebar.subheader("Débloquer l'accès")
    password = st.sidebar.text_input("Entrez votre code reçu par mail", type="password")
    
    if password == "LEAD2026": # Ton code secret
        st.sidebar.success("✅ Accès Illimité activé !")
        limit = 50
    else:
        st.sidebar.error("Code requis pour l'illimité")
        st.sidebar.markdown(f'<a href="https://buy.stripe.com/00w5kD1JWedb9DId082Ji00" style="color:#00d4ff;">Cliquez ici pour obtenir votre code</a>', unsafe_allow_html=True)
        limit = 3

# --- CORPS DE L'APPLICATION ---
st.title("🚀 LeadHunter Pro")
st.markdown("<p style='text-align: center; color: #8b949e;'>L'outil ultime pour extraire vos futurs clients instantanément.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    search_query = st.text_input("🔍 Que cherchez-vous ?", placeholder="ex: Agence immobilière Lyon, Restaurant Paris...")

with col2:
    st.write("##") # Espace
    run_btn = st.button("Lancer l'extraction")

if run_btn:
    if search_query:
        with st.spinner('🛠 Recherche et extraction des données en cours...'):
            try:
                results = []
                with DDGS() as ddgs:
                    # On ajoute "contact info" pour forcer des résultats pro
                    search_results = ddgs.text(f"{search_query} site:linkedin.com OR site:facebook.com OR contact", max_results=limit)
                    
                    for r in search_results:
                        results.append({
                            "🚀 Nom / Société": r['title'],
                            "🔗 Source": r['href'],
                            "📄 Détails": r['body'][:150] + "..."
                        })
                
                if results:
                    df = pd.DataFrame(results)
                    
                    st.subheader(f"✅ {len(results)} Prospects trouvés")
                    
                    # Affichage stylé sous forme de tableau
                    st.dataframe(df, use_container_width=True)

                    # Export Excel
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger la liste (Excel/CSV)",
                        data=csv,
                        file_name=f"leads_{search_query.replace(' ', '_')}.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("Aucun résultat trouvé. Essayez de changer les mots-clés.")
            except Exception as e:
                st.error(f"Une erreur est survenue. Veuillez réessayer. {e}")
    else:
        st.error("⚠️ Veuillez entrer une recherche (ex: Plombier Nice)")

# Pied de page
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #555;'>LeadHunter Pro - Tous droits réservés © 2026. <br> Support : ton-email@gmail.com</p>", unsafe_allow_html=True)
