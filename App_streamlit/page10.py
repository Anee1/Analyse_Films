import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os

# Définition du dossier de sortie
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

st.title("🎬 Analyse Générale des Films et Évaluations")

# Fonction cache pour charger les fichiers parquet
@st.cache_data
def load_parquet_data(file_name):
     file_path = OUTPUT_DIR / file_name
     return pd.read_parquet(file_path)

# Chargement des données
genre_df = load_parquet_data("genre_df.parquet")
movies_by_year = load_parquet_data("movies_by_year.parquet")
top_movies = load_parquet_data("top_movies_by_ratings.parquet")
ratings_df = load_parquet_data("ratings.parquet")

# Graphique 1 : Top 10 genres par nombre de films
fig_genre = px.bar(
    genre_df,
    x="count",
    y="genre",
    title="Top 10 genres par nombre de films",
    labels={"genre": "Genre", "count": "Nombre de films"},
    color="count",
    color_continuous_scale="viridis",
    orientation='h'
)
fig_genre.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    height=350
)

# Graphique 2 (nouveau) : Distribution des notes attribuées par les utilisateurs
fig_ratings_dist = px.histogram(
    ratings_df,
    x="rating",
    nbins=10,
    title="Distribution des notes attribuées par les utilisateurs",
    labels={"rating": "Note", "count": "Nombre d’évaluations"},
    color_discrete_sequence=['#636EFA']
)
fig_ratings_dist.update_layout(
    xaxis=dict(dtick=0.5),
    height=400
)

# Graphique 3 : Top 10 utilisateurs par nombre d’évaluations
ratings_per_user = ratings_df['userId'].value_counts().reset_index()
ratings_per_user.columns = ['userId', 'rating_count']
top_users = ratings_per_user.head(10)
fig_users = px.bar(
    top_users,
    x="rating_count",
    y=top_users["userId"].astype(str),
    orientation="h",
    title="Top 10 des utilisateurs par nombre d’évaluations",
    labels={"userId": "Utilisateur", "rating_count": "Nombre d’évaluations"},
    color="rating_count",
    color_continuous_scale="viridis"
)
fig_users.update_layout(
   yaxis={'categoryorder': 'total ascending'},
   height=350
)
st.write("### Données brutes - Top utilisateurs")
st.dataframe(top_users)

# Graphique 4 : Top 20 des films par nombre d’évaluations
fig_top_movies = px.bar(
    top_movies.sort_values("rating_count", ascending=True),
    x="rating_count",
    y="title",
    color="avg_rating",
    orientation="h",
    title="Top 20 des films par nombre d'évaluations",
    labels={"title": "Titre du film", "rating_count": "Nombre d'évaluations", "avg_rating": "Note moyenne"},
    color_continuous_scale="viridis"
)
fig_top_movies.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    height=700
)

# Graphique 5 : Nombre de films par année
fig_by_year = px.bar(
    movies_by_year,
    x="year",
    y="movie_count",
    title="Nombre total de films par année (basé sur le titre)",
    labels={"year": "Année", "movie_count": "Nombre de films"},
)
fig_by_year.update_layout(
    xaxis_title="Année",
    yaxis_title="Nombre de films",
    height=500
)

# Mise en page Streamlit
col1, col2 = st.columns([1, 2])

with col1:
    st.plotly_chart(fig_genre, use_container_width=True)
    st.plotly_chart(fig_ratings_dist, use_container_width=True)
    st.plotly_chart(fig_users, use_container_width=True)

with col2:
    st.plotly_chart(fig_top_movies, use_container_width=True)

st.divider()

st.plotly_chart(fig_by_year, use_container_width=True)
