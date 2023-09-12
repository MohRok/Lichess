import webbrowser
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

# Initialize the Dash app
app = Dash(__name__)

# Define custom CSS styles
custom_styles = {
    'navbar': {
        'background-image': 'linear-gradient(to left, black, white)',
        'color': 'white',
        'padding': '10px',
        'display': 'flex',
        'justify-content': 'link',
        'align-items': 'center',
        'position': 'relative',
    },
    'nav_links': {
        'list-style': 'none',
        'margin': '0',
        'padding': '0',
    },
    'nav_link': {
        'text-decoration': 'none',
        'color': 'inherit',
        'margin-right': '60px',
        'font-weight': 'bold',
    },
    'nav_dropdown': {
        'position': 'relative',
    },
    'nav_dropdown_content': {
        'display': 'flex',
        'color': 'darkblue',
        'position': 'absolute',
        'top': '100%',
        'background-color': 'darkblue',
        'box-shadow': '0px 8px 16px 0px rgba(0,0,0,0.2)',
        'min-width': '25%',
        'z-index': '1',
    },
}

# Layout of the home page
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div([
        html.Img(src="/assets/lichesslogo.png", alt="foto", width="300px",
                 style={'position': 'absolute', 'top': '0px', 'right': '0px'}),
    ]),
    html.Nav(
        children=[
            html.A("Home", href="/", style=custom_styles['nav_link']),
            html.Button("☰", id="dropdown-button", style={'font-size': '24px'}),
        ],
        style={'background-image': 'linear-gradient(to left, black, white)', 'color': 'black', 'padding': '10px',
               'display': 'flex', 'justify-content': 'link', 'align-items': 'center'},
    ),
    html.Div([
        html.Div([
            html.Ul([
                html.Li(html.A("Option 1", href="/options/option1", style=custom_styles['nav_link'])),
                html.Li(html.A("Option 2", href="/options/option2", style=custom_styles['nav_link'])),
                html.Li(html.A("Option 3", href="/options/option3", style=custom_styles['nav_link'])),
            ], style=custom_styles['nav_links']),
        ], style=custom_styles['nav_dropdown_content'], id="dropdown-content"),
    ], style=custom_styles['nav_dropdown']),
    html.Div(id='graph-content', style={'text-align': 'center', 'margin-top': '150px'}),


])

# Layout of the home page content
home_layout = html.Div([
    html.Div([
        html.H1("Welcome to Data Science Project Lichess Page", style={'margin-right': '20px'}),
        html.P("Team: Michel, Mohamad, Viktoria.", style={'font-size': '24px'}),
    ], style={'display': 'flex', 'align-items': 'center'}),
], style={'background-image': 'linear-gradient(to bottom, gray, white)', 'color': 'black', 'padding': '10px'})

# Layout for Option 1 content
option1_layout = html.Div([
    html.Div([
        html.H1("Option 1", style={'margin-right': '20px'}),
        html.P("This is the content for Option 1.", style={'font-size': '24px'}),
    ], style={'display': 'flex', 'align-items': 'center'}),
], style={'background-image': 'linear-gradient(to Bottom, gray, white)', 'color': 'black', 'padding': '10px',
          'display': 'flex', 'justify-content': 'link', 'align-items': 'center'}, )

# Layout for Option 2 content
option2_layout = html.Div([
    html.Div([
        html.H1("Option 2", style={'margin-right': '20px'}),
        html.P("This is the content for Option 2.", style={'font-size': '24px'}),
    ], style={'display': 'flex', 'align-items': 'center'}),
], style={'background-image': 'linear-gradient(to Bottom, gray, white)', 'color': 'black', 'padding': '10px',
          'display': 'flex', 'justify-content': 'link', 'align-items': 'center'},)

# Layout for Option 3 content
option3_layout = html.Div([
    html.Div([
        html.H1("Option 3", style={'margin-right': '20px'}),
        html.P("This is the content for Option 3.", style={'font-size': '24px'}),
    ], style={'display': 'flex', 'align-items': 'center'}),
], style={'background-image': 'linear-gradient(to Bottom, gray, white)', 'color': 'black', 'padding': '10px',
          'display': 'flex', 'justify-content': 'link', 'align-items': 'center'}, )


# Callback function to display the appropriate content based on URL pathname
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    if pathname == "/options/option1":
        return option1_layout
    elif pathname == "/options/option2":
        return option2_layout
    elif pathname == "/options/option3":
        return option3_layout
    else:
        return home_layout


# Callback to update the graph content based on URL pathname
@app.callback(
    Output('graph-content', 'children'),
    Input('url', 'pathname')
)
def update_graph(pathname):
    if pathname == '/options/option1':
        return dcc.Graph(
            id='option1-chart',
            figure={
                'data': [
                    go.Bar(
                        x=['Category A', 'Category B', 'Category C'],
                        y=[10, 20, 30],
                        name='Option 1 Data',
                    ),
                ],
                'layout': {
                    'title': 'Option 1 Chart',
                },
            }
        )
    elif pathname == '/options/option2':
        return dcc.Graph(
            id='option2-chart',
            figure={
                'data': [
                    go.Scatter(
                        x=[1, 2, 3, 4, 5],
                        y=[10, 11, 12, 13, 14],
                        mode='markers',
                        name='Option 2 Data',
                    ),
                ],
                'layout': {
                    'title': 'Option 2 Chart',
                },
            }
        )
    elif pathname == '/options/option3':
        return dcc.Graph(
            id='option3-chart',
            figure={
                'data': [
                    go.Pie(
                        labels=['Category A', 'Category B', 'Category C'],
                        values=[40, 30, 20],
                        name='Option 3 Data',
                    ),
                ],
                'layout': {
                    'title': 'Option 3 Chart',
                },
            }
        )
    else:
        raise PreventUpdate


# Callback to toggle the visibility of the dropdown content when the button is clicked
@app.callback(
    Output("dropdown-content", "style"),
    Input("dropdown-button", "n_clicks"),
)
def toggle_sidebar(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'position': 'relative', 'top': '00px', 'left': '0px', 'width': '300px',
                'background-image': 'linear-gradient(to top, gray, white)', 'padding': '100px'}
    else:
        return {'position': 'absolute', 'top': '00px', 'left': '-200px', 'width': '0px',
                'background-image': 'linear-gradient(to top, gray, white)', 'padding': '0px'}


if __name__ == '__main__':
    webbrowser.open_new_tab('http://localhost:8050')
    app.run_server(debug=True)
