import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Function to plot africa map showing cause of death
def map_plot(data, color):
    fig = px.choropleth(data, locations="Code",
                        color=color, width=500,
                        title=f'Death by {color} in Africa',
                        hover_name="Entity", 
                        labels={'Terrorism (deaths)': 'Count', 
                                'Drug use disorders': 'Count',
                                "Poisonings": 'Count'},
                        hover_data=[color],
                        color_continuous_scale='Rainbow', 
    )
    fig.update_layout(geo_scope="africa", 
                    #   margin={"r":0,"t":0,"l":0,"b":0}
                      )
    fig.show()
    
# Function to visualize yearly cause of death
def line_plot(data, title):
    trace = px.line(data,
        x=data.columns[0],
        y=data.columns[1],
        title=title,
        width=900,
        markers=True,
    )
    trace.show()
    
# Function to visualize top 5 countries
def top5_barChart(data, title):
    trace = px.bar(data,
        x=data.columns[0],
        y=data.columns[2],
        text_auto='.3s',
        title=title,
        width=900, labels={'Entity':''}
    )
    trace.update_traces(textposition='outside', cliponaxis=False)
    trace.update_yaxes(showticklabels=False)
    trace.show()
  
# Function to reshape health expenditure data
def reshaper(top_data, df):
    country_code = top_data['Code'].unique()
    coutry_health_exp = df[df['Country Code'].isin(country_code)]
    coutry_health_exp.set_index('Country Name', inplace=True)
    long_df = pd.melt(coutry_health_exp, id_vars=['Country Code', 'Indicator Name'], value_name='Health Expenditure(% of GDP)', var_name='Year', ignore_index=False)
    long_df.reset_index(drop=False, inplace=True)
    long_df.groupby('Country Name')['Health Expenditure(% of GDP)'].sum()
    reshaped_df = long_df.pivot_table(index='Year', values='Health Expenditure(% of GDP)', columns='Country Name')
    return reshaped_df  

# Function to reshape age group data
def reshaper1(top_data,df):
    country_code = top_data['Code'].unique()
    coutry_health_exp = df[df['Code'].isin(country_code)]
    long_df = pd.melt(coutry_health_exp, id_vars=['Entity' ,'Code', 'Year'], value_name='Death Count', var_name='Age', ignore_index=False)
    reshaped_df = long_df.groupby(['Entity', 'Age'], as_index=False)['Death Count'].mean()
    return reshaped_df  

# Function to visualize age group death in top 5 country for each cause of death
def group_bar(data, title='Age Group Death'):
    fig = px.bar(
            data,
            x='Entity',
            y='Death Count',
            color='Age', width=1100,
            barmode='group', title=title,
            labels={'Entity':''},
        )
    fig.update_layout(legend=dict(orientation='h'))
    return fig

# Function to merge cause of the column with health expenditure
def subset_merger(column, df1, df2):
    sub = df1[['Entity', 'Code', 'Year', column]]
    melt_health = pd.melt(df2, id_vars=['Country Name', 'Country Code', 'Indicator Name'], value_name='Health Expenditure(% of GDP)', var_name='Year', ignore_index=False)
    sub_melt_health = melt_health[['Country Code', 'Year', 'Health Expenditure(% of GDP)']]
    merged = pd.merge(sub, sub_melt_health, 'inner', left_on=['Code', 'Year'], right_on=['Country Code', 'Year'])
    return merged

# Function to plot relationship between cause and health expenditure
def cause_health_relationship(data):
    fig = px.scatter(data, y=data.columns[3], x='Health Expenditure(% of GDP)', color='Year',
                     hover_name='Entity')
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        title=f'Realtionship between {data.columns[3]} and Health Expenditure', width=850,
        xaxis = dict(
            tickvals = [5, 10, 15, 20],
            ticktext = ['5%', '10%', '15%', '20%']
        )
    )
    return fig.show()