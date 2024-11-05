import streamlit as st
import pandas as pd

# Sample movie data
movies_data = pd.DataFrame({
    'Movie': ['Inception', 'The Matrix', 'Interstellar', 'The Godfather', 'Parasite'],
    'Rating': [8.8, 8.7, 8.6, 9.2, 8.6],
    'Year': [2010, 1999, 2014, 1972, 2019]
})

# Title of the app
st.title("Movie Ratings")

# Description
st.write("Welcome to the Movie Ratings app! Here you can see ratings and release years of popular movies.")

# Display the movie data in a table format
st.dataframe(movies_data)

# Filter movies by rating
min_rating = st.slider("Filter by minimum rating", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
filtered_data = movies_data[movies_data['Rating'] >= min_rating]

st.write(f"Movies with a rating of at least {min_rating}:")
st.dataframe(filtered_data)

