import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from machine_learning import topic_extraction,create_dict_list_of_topics

global final_reddit_topic_df
global top_post_df

# Set up the app
app = dash.Dash()
reddit_post_df = pd.read_csv('resource/topics.csv')
sorted_reddit_post_df = reddit_post_df.sort_values(by=['comms_num'],ascending=False)
final_reddit_post_df = sorted_reddit_post_df.head(5)
final_reddit_topic_df = topic_extraction(sorted_reddit_post_df)
top_post_df = final_reddit_topic_df[['title','score','url','dominanttopic']].sort_values(by=['score'], ascending=False)
top_post_df = top_post_df.assign(rank=[ 1+i for i in range(len(top_post_df))])[['rank'] + top_post_df.columns.tolist()]
dict_topics = create_dict_list_of_topics(final_reddit_topic_df)



app.layout = html.Div([
    html.H1('Auto Generated FAQ'),
    html.H3('Drop down'),
    dcc.Dropdown(
        id='my-dropdown',
        options=dict_topics,
        multi=True
    ),
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
              }),
    html.H2('FAQ'),
    html.Table(id= 'my-table')
])

@app.callback(Output('my-table', 'children'), [Input('my-dropdown', 'value')])
def generate_table(selected_dropdown_value,max_rows=10):

    print(selected_dropdown_value)
    #filtering
    top_post_filtered_df= top_post_df.copy()
    top_post_filtered_df['dominant_topic_text']= top_post_df['dominanttopic'].apply(convertTuple)
    top_post_filtered_df= top_post_filtered_df[(top_post_filtered_df['dominant_topic_text'].isin(selected_dropdown_value))]
    top_post_filtered_df = top_post_filtered_df.drop(columns=['dominanttopic'])
    print(top_post_filtered_df)

    return [html.Tr([html.Th(col) for col in top_post_filtered_df.columns])] + [html.Tr([
        html.Td(html.A('click',href=top_post_filtered_df.iloc[i][col])) if col =='url' else html.Td(top_post_filtered_df.iloc[i][col]) for col in top_post_filtered_df.columns
    ]) for i in range(min(len(top_post_filtered_df), max_rows))]

def convertTuple(tup):
    str =  ','.join(tup)
    return str

if __name__ == '__main__':
    app.run_server(debug=True)

