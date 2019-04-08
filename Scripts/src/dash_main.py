import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from machine_learning import topic_extraction,create_dict_list_of_topics
import time

global final_reddit_topic_df
global top_post_df
global dict_topics

# Set up the app
app = dash.Dash()
reddit_post_df = pd.read_csv('resource/topics.csv')
sorted_reddit_post_df = reddit_post_df.sort_values(by=['comms_num'],ascending=False)
final_reddit_post_df = sorted_reddit_post_df.head(5)
final_reddit_topic_df = topic_extraction(sorted_reddit_post_df)
top_post_df = final_reddit_topic_df[['title','score','dominanttopic']].sort_values(by=['score'], ascending=False)
# top_post_df = top_post_df.assign(rank=[ 1+i for i in range(len(top_post_df))])[['rank'] + top_post_df.columns.tolist()]
dict_topics = create_dict_list_of_topics(final_reddit_topic_df)



def dict_topic_list(dict_list):
    topic_list = []
    for dict in dict_list:
        topic_list.append(dict.get('value'))
    print(topic_list)
    return topic_list

app.layout = html.Div([
    html.H1('Auto Generated FAQ'),
    html.H4('Select Topics'),
    dcc.Dropdown(
        id='my-dropdown',
        options=dict_topics,
        multi=True,
        value= dict_topic_list(dict_topics)
    ),
    # html.H3('Trending Topics'),
    dcc.Graph(
        id='top_topics'
    ),
    html.H1('FAQ This Week'),
    html.Table(id='my-table')
])


# For the top topics graph
@app.callback(Output('top_topics', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    top_topic_filtered_df = top_post_df.copy()
    top_topic_filtered_df = top_post_filtered(top_topic_filtered_df, selected_dropdown_value)

    figure = {
        'data': [go.Bar(
            y=top_topic_filtered_df.dominant_topic_text.value_counts().index,
            x=top_topic_filtered_df.dominant_topic_text.value_counts().values,
            orientation='h'
        )],
        'layout':go.Layout(
            title= 'Trending Topics',
            yaxis = dict(
                # autorange=True,
                automargin=True
            )
        )
    }
    return figure

@app.callback(Output('my-table', 'children'), [Input('my-dropdown', 'value')])
def generate_table(selected_dropdown_value,max_rows=10):
    top_post_filtered_df= top_post_df.copy()
    top_post_filtered_df= top_post_filtered(top_post_filtered_df,selected_dropdown_value)
    return [html.Tr([html.Th(col) for col in top_post_filtered_df.columns])] + [html.Tr([
        html.Td(html.A('click', href=top_post_filtered_df.iloc[i][col])) if col == 'url' else html.Td(
            top_post_filtered_df.iloc[i][col]) for col in top_post_filtered_df.columns
    ]) for i in range(min(len(top_post_filtered_df), max_rows))]

def convertTuple(tup):
    str =  ','.join(tup)
    return str

def top_post_filtered(top_post_filtered_df,selected_dropdown_value):
    print(selected_dropdown_value)

    # if selected_dropdown_value is None:
    #     selected_dropdown_value = dict_topics
    top_post_filtered_df['dominant_topic_text'] = top_post_df['dominanttopic'].apply(convertTuple)
    top_post_filtered_df = top_post_filtered_df[
        (top_post_filtered_df['dominant_topic_text'].isin(selected_dropdown_value))]
    top_post_filtered_df = top_post_filtered_df.drop(columns=['dominanttopic'])
    return top_post_filtered_df


if __name__ == '__main__':
    app.run_server(debug=True)
