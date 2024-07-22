import streamlit as st
import joblib
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=411f9b0c61c1c42ce56826e05e8fc9ab&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
    recommended = []
    recommended_movies_poster = []
    for x in movie_list:
        movie_id = movies.iloc[x[0]].movie_id
        recommended.append(movies.iloc[x[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended, recommended_movies_poster


movies_dict = joblib.load('/Users/harleen/Desktop/Codes/Python/Movie Recommender System/movies.pkl')
movies = pd.DataFrame(movies_dict)
movies_list = movies['title'].values
similarity = joblib.load('/Users/harleen/Desktop/Codes/Python/Movie Recommender System/similarity.pkl')

st.title('Movie Recommendation System')

selected_option = st.selectbox('Select a Movie', movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_option)
    for i in range(0, 6, 3):
        cols = st.columns(3)
        for idx, col in enumerate(cols):
            if i + idx < len(names):  # Ensure index is within bounds
                with col:
                    st.text(names[i + idx])
                    st.image(posters[i + idx])

