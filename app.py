"""
    This is the application file which will excute the web requests.
    Streamlit is used to create a webapp.
"""
import streamlit as st
import pickle
import requests
import pandas as pd
from Model_Building.Build_Save_Data import Build_save_Data

#model = Build_save_Data()
#model.executeBuild()





movies = pd.DataFrame(pd.read_pickle("Modeled_Data/movies.pkl"))
similarity = pickle.load(open("Modeled_Data/similarity.pkl",'rb'))


def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
     data = requests.get(url)
     data = data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
     return full_path




def RecommendEngine(movie):
    #print(movies)
    index =movies[movies['title']== movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key= lambda x:x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:

        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.title('Movie Recommendation Portal')

#loding the saved data in pickle file


#extracting movie title from the file

names = movies['title'].values

# Drop down menu
selected_movie = st.selectbox(
     'Please search or select a movie that you like',
     (names))

st.write('You selected:', selected_movie)




if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = RecommendEngine(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


st.text("By Abhishek")