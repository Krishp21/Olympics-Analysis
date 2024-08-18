import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        # Overall performance of a specific country
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['total'] = x['Gold'] + x['Silver'] +  x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    return x


#def medal_tally(df):
    #medal_tally =df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    #medal_tally= medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    #medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] +  medal_tally['Bronze']
    #medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    #medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    #medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    #return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years, country


def data_over_time(df, col):

    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values("Year")
    nations_over_time.rename(columns={'Year':'Edition','count':'No of countries'},inplace=True)
    return nations_over_time

def most_successful(df, sport):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if not 'Overall'
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count the number of medals won by each athlete
    athlete_medals = temp_df['Name'].value_counts().reset_index()

     # Rename columns for clarity
    athlete_medals.columns = ['Name', 'Medals']

    # Get the top 15 athletes with the most medals
    top_15 = athlete_medals.nlargest(15, 'Medals')

    # Merge with the original DataFrame to get additional details like 'Sport' and 'region'
    athlete_details = top_15.merge(temp_df, left_on='Name', right_on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']]

    # Drop duplicates to avoid repetitive information
    athlete_details = athlete_details.drop_duplicates(subset=['Name'])

    return athlete_details


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'Medals']

    x = x.merge(temp_df, left_on='Name', right_on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    return x