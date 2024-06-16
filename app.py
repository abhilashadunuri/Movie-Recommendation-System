import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=1d9fb9a6ce811cc81442a5f6528283ca&language=en-US".format(movie_id)
    retries = 3  # Number of retries
    # for _ in range(retries):
    #     try:
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
        # except requests.exceptions.RequestException as e:
        #     print("Error fetching poster:", e)
        #     print("Retrying...")
            # time.sleep(1)  # Wait for 1 second before retrying
    # print("Max retries exceeded. Unable to fetch poster.")
    # return None

movies = pickle.load(open("movies_list.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))
movies_list=movies['title'].values

st.header("Movie Recommendation System")


value = st.selectbox("Select Movie from the Dropdown", movies_list)



def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movies_id)
        if poster_url:  # Check if poster retrieval was successful
            recommend_poster.append(poster_url)
    return recommend_movie, recommend_poster

if st.button("Show Recommendations"):
    name, movie_poster = recommend(value)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(name[4])
        st.image(movie_poster[4])
    