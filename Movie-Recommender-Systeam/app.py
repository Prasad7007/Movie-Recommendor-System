import streamlit as st
import pandas as pd
import pickle
import requests

# Function to fetch the poster of a movie
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4e81ffbd3394792fb9f3de7d59ef418f')
    data = response.json()
    if 'poster_path' in data:
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    else:
        return None

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon=":clapper:",
    layout="wide"
)

# Login credentials
login_credentials = {
    "username": "admin",
    "password": "admin123"
}

# Sidebar for login
with st.sidebar:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == login_credentials["username"] and password == login_credentials["password"]:
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials. Please try again.")

# Main content
st.title('Movie Recommender System')

# Select a movie
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

# Button to trigger recommendation
if st.button('Recommend', key='recommend_button'):
    names, posters = recommend(selected_movie_name)

    # Display recommended movies with posters
    st.subheader('Recommended Movies:')
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        with globals()[f"col{i+1}"]:
            st.markdown(f"<p style='color:#FFFFFF;font-size:20px;font-family:Arial, sans-serif;'>{names[i]}</p>", unsafe_allow_html=True)
            if posters[i] is not None:
                st.image(posters[i], use_column_width=True, output_format='PNG')
            else:
                st.write("No poster available")
