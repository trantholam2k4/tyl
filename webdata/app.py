import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def format_option(value):
    return f"{value:.2f}"

# Load the movies dataset
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")
st.set_page_config(page_title = "Movies analysis",layout = 'wide')
st.header("Interactive Dashboard")
st.subheader("Interact with this dashboard using the widgets on the sidebar")
# Remove commas from the "year" column
movies_data["year"] = movies_data["year"].astype(str).str.replace(",", "")

# Sidebar widgets
st.sidebar.write("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range")
selected_score = st.sidebar.slider(label="Choose a value:",
                                   min_value=1.0,
                                   max_value=10.0,
                                   value=(3.0, 4.0))
score_info = (movies_data['score'].between(*selected_score))
selected_genres = st.sidebar.multiselect("Choose Genre:", movies_data["genre"].unique())
selected_year = st.sidebar.selectbox("Choose a Year", movies_data["year"].unique())


filtered_df = movies_data[(movies_data["genre"].isin(selected_genres)) & (movies_data["year"] == selected_year)]


col1, col2 = st.columns([2,3])
with col1:
    
    st.write("Lists of movies filtered by year and Genre")
    display_df=filtered_df[["name", "genre","year"]].reset_index(drop=True)
    st.dataframe(display_df,width=450)


with col2:
    st.write("""#### User score of movies and their genre """)
    score_filtered_df = movies_data[(movies_data["score"] >= selected_score[0]) & (movies_data["score"] <= selected_score[1])]
    rating_count_year = score_filtered_df.groupby('genre')['score'].count().reset_index()
    figpx = px.line(rating_count_year, x='genre', y='score')
    figpx.update_layout(xaxis=dict(title='Genre', showgrid=True), yaxis=dict(title='Number of Movies', showgrid=True))
    st.plotly_chart(figpx)

st.write("Average Movie Budget, Grouped by Genre")
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']
fig = plt.figure(figsize=(19, 10))
plt.bar(genre, avg_bud, color='maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing the Average Budget of Movies in Each Genre')
st.pyplot(fig)
# streamlit run app.py