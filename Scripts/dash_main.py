import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

# Set up the app
app = dash.Dash()
reddit_post_df = pd.read_csv('topics.csv')
sorted_reddit_post_df = reddit_post_df.sort_values(by=['comms_num'],ascending=False)
final_reddit_post_df = sorted_reddit_post_df.head(5)
app.layout = html.Div([
    html.H1('Auto Generated FAQ'),
    dcc.Graph(id='top_post',
              figure={
                  'data':[go.Bar(
                    y= final_reddit_post_df.id,
                    x= final_reddit_post_df.comms_num,
                    orientation='v'
                    )],
                  'layout':{
                      'title':'Top posts from forum'
                  }
              })
])

if __name__ == '__main__':
    reddit_post_df = pd.read_csv('topics.csv')
    print(reddit_post_df.head())
    print(reddit_post_df.id)
    print(reddit_post_df.comms_num)
    app.run_server()