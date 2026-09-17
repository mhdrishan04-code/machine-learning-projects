import os
from functools import lru_cache
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    return pd.read_csv("movies.csv")

def is_real_poster(value):
    if not isinstance(value, str):
        return False
    value = value.strip()
    return value.startswith("http") and "placehold.co" not in value

def fetch_omdb_poster(movie_title):
    api_key = os.getenv("OMDB_API_KEY")
    try:
        import streamlit as st
        api_key = api_key or st.secrets.get("OMDB_API_KEY")
    except Exception:
        pass
    if not api_key:
        return None
    try:
        r = requests.get("https://www.omdbapi.com/", params={"t": movie_title, "apikey": api_key}, timeout=6)
        r.raise_for_status()
        poster = r.json().get("Poster")
        return poster if poster and poster != "N/A" and poster.startswith("http") else None
    except Exception:
        return None

@lru_cache(maxsize=256)
def fetch_wikipedia_poster(movie_title, language=""):
    endpoint = "https://en.wikipedia.org/w/api.php"
    queries = [f'"{movie_title}" film', movie_title]
    for query in queries:
        try:
            r = requests.get(endpoint, params={"action":"query","format":"json","formatversion":"2","generator":"search","gsrsearch":query,"gsrnamespace":0,"gsrlimit":5,"prop":"pageimages","piprop":"thumbnail|original","pithumbsize":600,"pilicense":"any"}, headers={"User-Agent":"AI-Movie-Recommendation-System/2.0"}, timeout=6)
            r.raise_for_status()
            pages = r.json().get("query", {}).get("pages", [])
            for page in pages:
                poster = page.get("thumbnail", {}).get("source") or page.get("original", {}).get("source")
                if poster and poster.startswith("http"):
                    return poster
        except Exception:
            continue
    return None

def fetch_real_poster(movie_title, language="", csv_poster=None):
    if is_real_poster(csv_poster):
        return csv_poster.strip()
    return fetch_omdb_poster(movie_title) or fetch_wikipedia_poster(movie_title, language)

def get_recommendations(genre, language, mood, top_n=5):
    data = load_data()
    for column in ["genre", "language", "mood", "poster_url"]:
        if column not in data.columns:
            data[column] = ""
        data[column] = data[column].fillna("").astype(str)
    data["features"] = data["genre"] + " " + data["language"] + " " + data["mood"]
    vectorizer = CountVectorizer()
    feature_vectors = vectorizer.fit_transform(data["features"])
    user_vector = vectorizer.transform([f"{genre} {language} {mood}"])
    data["similarity_score"] = cosine_similarity(user_vector, feature_vectors).flatten()
    recommendations = data.sort_values("similarity_score", ascending=False).head(top_n).copy()
    recommendations["similarity_score"] = (recommendations["similarity_score"] * 100).round(2)
    recommendations["poster_url"] = recommendations.apply(lambda row: fetch_real_poster(str(row["Title"]), str(row["language"]), row["poster_url"]), axis=1)
    return recommendations[["Title", "genre", "language", "mood", "poster_url", "similarity_score"]]
