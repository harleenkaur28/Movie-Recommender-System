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
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
    recommended = []
    recommended_movies_poster = []
    for x in movie_list:
        movie_id = movies.iloc[x[0]].movie_id
        recommended.append(movies.iloc[x[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended, recommended_movies_poster


def recommend_genre(genre, movies_df):

    filtered_movies = movies_df[movies_df['tags'].apply(lambda tags: genre in tags)]
    sampled_movies = filtered_movies.sample(n=min(9, len(filtered_movies)), random_state=42)

    recommended = []
    recommended_movies_poster = []

    for index, row in sampled_movies.iterrows():
        movie_id = row['movie_id']
        recommended.append(row['title'])
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended, recommended_movies_poster


movies_dict = joblib.load('movies.pkl')
movies = pd.DataFrame(movies_dict)
movies_list = movies['title'].values.tolist()
similarity = joblib.load('similarity.pkl')

st.title('Movie Recommendation System')
st.text('Choose for your favorite genre or find movies similar to the ones you like!')

genre_list = ['Action', 'Fantasy', 'Crime', 'Adventure', 'Mystery', 'ScienceFiction', 'Thriller', 'Comedy', 'Romance', 'Drama', 'Horror']
for i in genre_list:
    movies_list.append(i)
selected_option = st.selectbox('Choose a Movie or Genre', movies_list)


if st.button('Recommend'):
    if selected_option in genre_list:
        names, posters = recommend_genre(selected_option.lower(), movies)
        st.text('Genre Chosen')
        for i in range(0, 9, 3):
            cols = st.columns(3)
            for idx, col in enumerate(cols):
                if i + idx < len(names):
                    with col:
                        st.text(names[i + idx])
                        st.image(posters[i + idx])

    else:
        names, posters = recommend(selected_option)
        for i in range(0, 9, 3):
            cols = st.columns(3)
            for idx, col in enumerate(cols):
                if i + idx < len(names):
                    with col:
                        st.text(names[i + idx])
                        st.image(posters[i + idx])

