import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Football Match Analysis", page_icon="⚽", layout="wide")
sns.set_theme(style="whitegrid")

@st.cache_data
def load_data():
    return pd.read_csv("matches.csv")

df = load_data()
df["Season"] = df["Season"].astype(str).str.zfill(4)

st.title("⚽ Premier League : ce qui fait gagner un match")
st.caption("Données : football-data.co.uk, saisons 2015-16 à 2024-25")

# Barre latérale : les filtres
st.sidebar.header("Filtres")
seasons = sorted(df["Season"].unique())
season = st.sidebar.selectbox(
    "Saison", seasons, format_func=lambda s: f"20{s[:2]}-{s[2:]}"
)
indicators = {
    "Tirs": "shots_diff",
    "Tirs cadrés": "sot_diff",
    "Corners": "corners_diff",
    "Fautes": "fouls_diff",
}
label = st.sidebar.selectbox("Indicateur", list(indicators.keys()))
metric = indicators[label]

d = df[df["Season"] == season]

# Chiffres clés
share = d["FTR"].value_counts(normalize=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Matchs", len(d))
c2.metric("Victoires domicile", f"{share.get('H', 0):.0%}")
c3.metric("Nuls", f"{share.get('D', 0):.0%}")
c4.metric("Victoires extérieur", f"{share.get('A', 0):.0%}")

# Deux onglets
tab1, tab2 = st.tabs(["📊 Indicateur par résultat", "📋 Données"])

with tab1:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=d, x="FTR", y=metric, order=["H", "D", "A"],
                showfliers=False, palette=["#1DB954", "#B0B0B0", "#E4572E"], ax=ax)
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel("Résultat (H = domicile, D = nul, A = extérieur)")
    ax.set_ylabel(f"{label} (domicile - extérieur)")
    ax.set_title(f"{label} selon le résultat du match")
    st.pyplot(fig)
    st.info("Au-dessus de la ligne noire, l'équipe à domicile a fait plus que l'adversaire.")

with tab2:
    st.dataframe(d[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]],
                 use_container_width=True)
