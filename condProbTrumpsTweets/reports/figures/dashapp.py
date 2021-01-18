# coding=utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# read in data
rootDf = pd.read_csv('rootDf.csv')
tweets = pd.read_csv('tweetsDf.csv')
tweets.dropna(how='any', inplace=True)

dashWords = ['fake', 'fraud', 'vote', 'loser', 'impeachment', 'hillary', 'joe', 'bernie',
    'mcconnell', 'illegal', 'usa', 'china', 'xi', 'russia', 'ukraine', 'iran',
    'korea', 'blm', 'floyd', 'police', 'mexico', 'military', 'trudeau',
    'merkel', 'nuclear', 'negotiate', 'wall', 'america', 'maga', 'foxnews',
    'cnn', 'covid', 'vaccine', 'fauci', 'climate', 'protest', 'riot',
    'socialism', 'shooting', 'gun', 'pipeline', 'separation', 'proud',
    'muslim', 'iraq', 'iran', 'tariff', 'hoax', 'putin', 'pelosi', 'aoc',
    'mattis','flynn','manafort','tax','roger','comey', 'cohen']


# Load Data
df = rootDf
words = sorted(rootDf['word'].unique())
frequenciesDf = tweets.copy()

for dashword in dashWords:
    frequenciesDf[dashword] = frequenciesDf['cleanString'].apply(
        lambda x: dashword in x)

# Build App
app = dash.Dash(__name__)


# Configure Layout
app.layout = html.Div([
    html.H2('DJT Tweets: What else is he talking about'),
    html.
    H3('Select a word to see what other words occur most often with your selection among his tweets'
      ),
    dcc.Dropdown(
        id="dropdown",
        options=[{
            "label": x,
            "value": x
        } for x in words],
        value=words[0],
        clearable=False,
    ),
    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="line-chart")
],
                      id='container')


@app.callback([Output("bar-chart", "figure"),
              Output("line-chart", 'figure')], [Input("dropdown", "value")])

# create both figures to be passed in the return statement
# both figures are updated using the @app.callback path and the word dropdown

def multi_output(word):

    # narrow the pre-assembled dataframe for the word in question
    mask = df["word"] == word

    # generate first figure
    fig1 = px.bar(df[mask].sort_values(by='Percent Co-Occurrence',
                                      ascending=True),
                  y="Co-Occurring Word",
                  x="Percent Co-Occurrence",
                  orientation='h',
                #   height=400,
                #   width=900
                  )

    fig1.update_layout(title='Words most commonly seen given {}'.format(word),
                      showlegend=False,
                      font_size=8)

    fig1.update

    # figure 2: word-in-tweet frequency by day
    # using pre-calculated dataframe with bool cols for each word in dashWords...
    # group df by date and take the sum of the boolean word column
    dailyFrequency = frequenciesDf.groupby(by='date')[word].sum()

    # fig 2: line plot
    fig2 = px.line(dailyFrequency,
                    # height=250,
                    # width=900
                    )

    fig2.update_layout(
        title='Daily Tweets by @realDonaldTrump containing: {}'.format(word),
        xaxis_title='Date',
        yaxis_title='Count of Tweets',
        showlegend=False)

    fig2.update

    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)