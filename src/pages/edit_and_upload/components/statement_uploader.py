from dash import html, dcc

def upload_statements(disabled=False):
    return html.Div([
        html.H4("Upload Statements"),

        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A(
                    'Select Statements/CSVs',
                    style={'color': 'blue', 'textDecoration': 'underline'}
                )
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=True,
            disabled=disabled
        ),

        html.Div(
            id='upload-output',
            style={"whiteSpace": "pre-wrap", "marginTop": "1rem"}
        )
    ])


# from dash import html, dcc

# def upload_statements():
#     return html.Div([
#         html.H4("Upload Statements"),

#         dcc.Upload(
#             id='upload-data',
#             children=html.Div([
#                 'Drag and Drop or ',
#                 html.A(
#                     'Select Statements/CSVs',
#                     style={'color': 'blue', 'textDecoration': 'underline'}
#                 )
#             ]),
#             style={
#                 'width': '100%',
#                 'height': '60px',
#                 'lineHeight': '60px',
#                 'borderWidth': '1px',
#                 'borderStyle': 'dashed',
#                 'borderRadius': '5px',
#                 'textAlign': 'center',
#                 'margin': '10px'
#             },
#             multiple=True
#         ),
#         html.Div(
#             id='upload-output',
#             style={"whiteSpace": "pre-wrap", "marginTop": "1rem"}
#         )
#     ])
