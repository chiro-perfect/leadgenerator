import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
import base64

st.set_page_config(page_title="LeadGenerator Pro", page_icon="🚀")

st.title("🚀 Extracteur de Prospects B2B")
st.write("Trouvez vos futurs clients en un clic.")

# Système de forfait (Simulation simple)
st.sidebar.header("Mon Forfait")
plan = st.sidebar.selectbox("Choisir une option", ["Gratuit (3 résultats)", "Premium (Illimité)"])

if plan == "Premium (Illimité)":
    st.sidebar.success("✅ Accès Premium activé")
    limit = 50
else:
    st.sidebar.warning("⚠️ Mode Gratuit")
    st.sidebar.button("Passer au Premium (29€/mois)")
    limit = 3

# Interface de recherche
query = st.text_input("Quel type d'entreprise cherchez-vous ?", placeholder="ex: Agence immobilière Lyon")

if st.button("Lancer l'extraction"):
    if query:
        with st.spinner('Recherche en cours...'):
            results = []
            with DDGS() as ddgs:
                search_results = ddgs.text(f"{query} contact info", max_results=limit)
                for r in search_results:
                    results.append({"Nom": r['title'], "Lien": r['href'], "Extrait": r['body']})
            
            df = pd.DataFrame(results)
            st.table(df)

            # Bouton de téléchargement
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger le fichier Excel/CSV", data=csv, file_name="prospects.csv", mime="text/csv")
    else:
        st.error("Veuillez entrer une recherche.")