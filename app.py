import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv("matches.csv")
st.title("Premier League : ce qui fait gagner un match")

season = st.selectbox("Saison", sorted(df["Season"].unique()))
d = df[df["Season"] == season]

st.write(d["FTR"].value_counts(normalize=True))
metric = st.selectbox("Indicateur", ["shots_diff","sot_diff","corners_diff","fouls_diff"])
fig, ax = plt.subplots()
d.boxplot(column=metric, by="FTR", ax=ax)
st.pyplot(fig)