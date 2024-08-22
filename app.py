import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import streamlit as st

st.markdown(
    """
    <style>
    .dark-text {
        color: #000000; /* Dark color for text */
    }
    </style>
    """,
    unsafe_allow_html=True
)


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')



df = preprocessor.preprocess(df,region_df)
if 'page' not in st.session_state:
    st.session_state.page = 'intro'

def set_page(page_name):
    st.session_state.page = page_name

def show_intro():
    st.markdown(
        "<h1 class='dark-text' style='text-align: center; font-weight: bold;'>Olympics - Analysis</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p class='dark-text' style='text-align: center;'>"
        "This project is a comprehensive web application developed using Streamlit to analyze and visualize Olympic Games data. It provides users with insights into medal tallies, overall statistics, country-wise performance, and athlete details."
        "Users can explore data visualizations such as line charts, heatmaps, and distribution plots to understand patterns in medal counts, participation trends, and athlete statistics. The application aims to offer a user-friendly interface for exploring historical Olympic data, highlighting key statistics and trends across various dimensions."
        "</p>",
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <style>
        .intro-button {
            display: flex;
            justify-content: center;
            margin-top: 50px;
            
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button('Explore Analysis', key='explore_button', on_click=lambda: set_page('main')):
        pass

def show_main_app():
    st.sidebar.title("Olympics - Analysis")
    st.sidebar.image('https://wallpaperaccess.com/full/317531.jpg')

    if st.sidebar.button('Back to Intro', key='back_button', on_click=lambda: set_page('intro')):
        pass

    user_menu = st.sidebar.radio(
        'Select an Option:',
        ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete Wise Analysis')
    )
    main_gradient = 'linear-gradient(to right, #B2EBF2, #80DEEA);'


    sidebar_color = '#2C3E50'

    st.markdown(
        f"""
        <style>
        .main {{
            background: {main_gradient};
            background-attachment: fixed;
            color: #333333; 
        }}
        .css-1d391kg {{
            background-color: {sidebar_color};
        }}
        .css-1v3fvcr .css-1d391kg {{
            color: #333333;  
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    #st.dataframe(df)

    if user_menu == 'Medal Tally':
        st.sidebar.header("Medal Tally")
        years, country = helper.country_year_list(df)
        selected_year = st.sidebar.selectbox("Select Year", years)
        selected_country = st.sidebar.selectbox("Select Country", country)
        medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
        if selected_year == 'Overall' and selected_country == 'Overall':
            st.title("Overall Tally")
        if selected_year != 'Overall' and selected_country == 'Overall':
            st.title("Medal Tally in " + str(selected_year) + " Olympics")
        if selected_year == 'Overall' and selected_country != 'Overall' :
            st.title(selected_country + " overall performance")
        if selected_year != 'Overall' and selected_country != 'Overall':
            st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

        st.table(medal_tally)


    if user_menu == 'Overall Analysis':
        editions = df['Year'].unique().shape[0] - 1
        cities = df['City'].unique().shape[0]
        sports = df['Sport'].unique().shape[0]
        events = df['Event'].unique().shape[0]
        athletes = df['Name'].unique().shape[0]
        nations = df['region'].unique().shape[0]

        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions)
        with col2:
            st.header("Hosts")
            st.title(cities)
        with col3:
            st.header("Sports")
            st.title(sports)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Events")
            st.title(events)
        with col2:
            st.header("Nations")
            st.title(nations)
        with col3:
            st.header("Athletes")
            st.title(athletes)

        nations_over_time = helper.data_over_time(df, 'region')
        fig = px.line(nations_over_time, x="Edition", y="No of countries")
        st.title("Participating Nations over the years")
        st.plotly_chart(fig)

        events_over_time = helper.data_over_time(df, 'Event')
        events_over_time.rename(columns={"No of countries": "No of events"}, inplace=True)
        fig = px.line(events_over_time, x="Edition", y="No of events")
        st.title("Events over the years")
        st.plotly_chart(fig)

        athlete_over_time = helper.data_over_time(df, 'Name')
        athlete_over_time.rename(columns={"No of countries": "No of athletes"}, inplace=True)
        fig = px.line(athlete_over_time, x="Edition", y="No of athletes")
        st.title("Athletes over the years")
        st.plotly_chart(fig)

        st.title("Number of Events over time (Every Sport)")
        fig, ax = plt.subplots(figsize=(20, 20))
        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                    annot=True)
        st.pyplot(fig)

        st.title("Most successful Athletes")
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')
        selected_sport = st.selectbox('Select a Sport', sport_list)
        x = helper.most_successful(df, selected_sport)
        st.table(x)


    if user_menu == 'Country-Wise Analysis':

        st.sidebar.title('Country-Wise Analysis')

        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country = st.sidebar.selectbox('Select a Country', country_list)
        country_df = helper.yearwise_medal_tally(df, selected_country)
        fig = px.line(country_df, x="Year", y="Medal")
        st.title(selected_country + " Medal Tally over the years")
        st.plotly_chart(fig)

        st.title(selected_country + " excels in the following sports")
        pt = helper.country_event_heatmap(df,selected_country)
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)

        st.title("Top-10 Athletes of " + selected_country)
        top10_df = helper.most_successful_countrywise(df,selected_country)
        st.table(top10_df)


    if user_menu == 'Athlete Wise Analysis':
        athlete_df = df.drop_duplicates(subset=['Name', 'region'])

        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                           show_hist=False, show_rug=False)

        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Distribution of Age")
        st.plotly_chart(fig)

        x = []
        name = []
        famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                         'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                         'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                         'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                         'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                         'Tennis', 'Golf', 'Softball', 'Archery',
                         'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                         'Rhythmic Gymnastics', 'Rugby Sevens',
                         'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Distribution of Age with respect to Sports (Gold Medalist)")
        st.plotly_chart(fig)

        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')

        st.title('Height vs Weight')
        selected_sport = st.selectbox('Select a Sport', sport_list)

        temp_df = helper.weight_vs_height(df, selected_sport)
        fig,ax = plt.subplots()
        ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
        st.pyplot(fig)


        st.title("Men vs Women Participation over the Years")
        final = helper.men_vs_women(df)
        fig = px.line(final, x="Year", y=["Male", "Female"])
        fig.update_layout(autosize=False, width=1000, height=600)
        st.plotly_chart(fig)

if st.session_state.page == 'intro':
    show_intro()
else:
    show_main_app()
