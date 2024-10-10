import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Cricket dataset", page_icon="🎬")
st.title("🎬 Cricket dataset")
st.write(
    """
    This app visualizes data from [The Movie Database (TMDB)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
    It shows which movie genre performed best at the box office over the years. Just 
    click on the widgets below to explore!
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/CrickInfo_New - Test_Bat.csv")
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
genres = st.multiselect(
    "Team",
    df.Team.unique(),
    ["ENG", "WI", "AUS", "NZ", "IND", "SA", "SL", "PAK", "ZIM", "BAN", "IRE", "AFG"],
)

# Show a slider widget with the years using `st.slider`.
years = st.slider("Matches", 1, 200, (1, 16))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["Team"].isin(genres)) & (df["Mat"].between(years[0], years[1]))]
df_reshaped = df_filtered.pivot_table(
    index="StartYear", columns="Team", values="Runs", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="StartYear", ascending=False)
cop = len(pd.unique(df_filtered['PlayerName']))
print(cop)
st.metric(label="CountOfPlayers",value=cop)
st.table(df_filtered)

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"StartYear": st.column_config.TextColumn("StartYear")},
)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="StartYear", var_name="Team", value_name="Runs"
)
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("StartYear:N", title="Year"),
        y=alt.Y("Runs:Q", title="Gross earnings ($)"),
        color="Team:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
