import os
import streamlit as st
from PIL import Image

try:
    from recommender import get_recommendations
except ImportError:
    st.error("Could not import get_recommendations from recommender.py")
    st.stop()

LOGO_PATH = "logo.png"
has_logo = os.path.exists(LOGO_PATH)
logo_img = Image.open(LOGO_PATH) if has_logo else None

st.set_page_config(page_title="AI Movie Recommendation System", page_icon=logo_img if has_logo else "🎬", layout="centered")

if has_logo:
    st.image(logo_img, width=150)

st.title("AI Movie Recommendation System")
st.write("Find movies that match your taste!")

genre = st.selectbox("🎭 Select Genre", ["Sci-Fi", "Comedy", "Sports", "Thriller", "Romance", "Drama", "Action", "Adventure", "Fantasy", "Mystery", "Crime"])
language = st.selectbox("🌐 Select Language", ["English", "Hindi", "Malayalam", "Tamil", "Telugu", "Kannada", "Japanese", "Korean", "Spanish", "Italian", "Chinese"])
mood = st.selectbox("😊 Select Mood", ["Emotional", "Thriller", "Inspirational", "Adventure", "Suspense", "Feel Good", "Dark", "Spiritual", "Action"])
search_movie = st.text_input("🔍 Search Movie", placeholder="Enter movie name...").strip()

if st.button("🔍 Get Recommendations", type="primary", use_container_width=True):
    recommendations = get_recommendations(genre, language, mood)
    if search_movie:
        recommendations = recommendations[recommendations["Title"].astype(str).str.contains(search_movie, case=False, na=False)]

    st.subheader("⭐ Recommended Movies")
    if recommendations is None or recommendations.empty:
        st.warning("No recommendations found.")
    else:
        for _, movie in recommendations.iterrows():
            col1, col2 = st.columns([1, 2.5])
            with col1:
                poster = movie.get("poster_url")
                if poster:
                    st.image(poster, width=130)
                else:
                    st.write("🎬 No Poster")
            with col2:
                st.subheader(f"🎬 {movie['Title']}")
                st.write(f"🎭 Genre: {movie['genre']}")
                st.write(f"🌐 Language: {movie['language']}")
                st.write(f"😊 Mood: {movie['mood']}")
                st.write(f"⭐ Match Score: {movie['similarity_score']}%")

st.markdown("---")
with st.expander("ℹ️ About This Project"):
    st.markdown("""### 🎬 AI Movie Recommendation System
This project recommends movies based on genre, language and mood.

### 🤖 How It Works
The system uses CountVectorizer and cosine similarity to compare user preferences with movie features.

### 🛠️ Technologies
Python, Streamlit, Pandas, Scikit-learn and a movie dataset.""")
