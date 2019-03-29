import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from machine_learning import topic_extraction

# Set up the app
app = dash.Dash()
reddit_post_df = pd.read_csv('resource/topics.csv')
sorted_reddit_post_df = reddit_post_df.sort_values(by=['comms_num'],ascending=False)
final_reddit_post_df = sorted_reddit_post_df.head(5)
final_reddit_topic_df = topic_extraction(sorted_reddit_post_df)
app.layout = html.Div([
    html.H1('Auto Generated FAQ'),
    dcc.Graph(id='top_post',
              figure={
                  'data':[go.Bar(
                    y= final_reddit_post_df.id,
                    x= final_reddit_post_df.comms_num,
                    orientation='h'
                    )],
                  'layout':{
                      'title':'Top posts from forum'
                  }
              }),
    dcc.Graph(id='top_topics',
              figure={
                  'data':[go.Bar(
                    y= final_reddit_topic_df.dominanttopic.value_counts().index,
                    x= final_reddit_topic_df.dominanttopic.value_counts().values,
                    orientation='h'
                    )],
                  'layout':{
                      'title':'Top topics from forum'
                  }
              })
])

if __name__ == '__main__':
    app.run_server()

