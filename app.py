import pickle
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to download and load pickle files from a URL
def load_pickle_from_url(url, local_path):
    response = requests.get(url)
    with open(local_path, 'wb') as file:
        file.write(response.content)
    return pickle.load(open(local_path, 'rb'))

# Fetch the poster of a movie using TMDB API
def fetch_poster(movie_id):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + os.getenv("API_KEY")
    }

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path', '')
        if poster_path:
            return f"http://image.tmdb.org/t/p/w500/{poster_path}"
    return ""

# Recommend movies based on similarity
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        index = int(index)
    except IndexError:
        st.error("The selected movie was not found in the dataset.")
        return [], []
    
    if index >= similarity.shape[0]:
        st.error(f"Index {index} not found in the similarity matrix.")
        return [], []
    
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies_names = []
    recommended_movies_posters = []
    for i in distances[1:11]:  # Get top 10 recommendations
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_names.append(movies.iloc[i[0]].title)
    
    return recommended_movies_names, recommended_movies_posters

# Streamlit UI
st.header("Movies Recommendation System using ML")

# Option to load pickle files from external URLs
EXTERNAL_PICKLE = False  # Set to True if using external URLs

if EXTERNAL_PICKLE:
    movies_url = "https://drive.google.com/file/d/1fhCrMFy1hZOtJ77hPTrU29HIoIO8NcQl/view?usp=sharing"
    similarity_url = "https://drive.google.com/file/d/1T8Lb9NjyQYInkl4jYnyCyDctlUPNW0b0/view?usp=sharing"
    
    movies = load_pickle_from_url(movies_url, 'movie_list.pkl')
    similarity = load_pickle_from_url(similarity_url, 'similarity.pkl')
else:
    movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendations',
    movie_list
)

# Display the selected movie's poster and title
if selected_movie:
    st.subheader(f"Selected Movie: {selected_movie}")
    selected_movie_id = movies[movies['title'] == selected_movie]['movie_id'].values[0]
    selected_movie_poster = fetch_poster(selected_movie_id)
    if selected_movie_poster:
        st.image(selected_movie_poster, caption=selected_movie)

# Apply custom CSS for consistent title height
st.markdown("""
    <style>
    .movie-title {
        height: 50px;  /* Adjust this value as needed */
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;  /* Limits the title to 2 lines */
        -webkit-box-orient: vertical;
    }
    </style>
    """, unsafe_allow_html=True)

# Display recommended movies
if st.button("Show recommendations"):
    recommended_movies_names, recommended_movies_posters = recommend(selected_movie)
    if recommended_movies_names:
        st.subheader("Recommended Movies")
        cols = st.columns(5)  # 5 columns to show 10 movies, 2 per row
        for i in range(10):
            with cols[i % 5]:
                if recommended_movies_posters[i]:
                    st.image(recommended_movies_posters[i])
                else:
                    st.text("No poster available")
                st.markdown(f"<div class='movie-title'>{recommended_movies_names[i]}</div>", unsafe_allow_html=True)
                st.text("")  # Adds a line break for spacing
