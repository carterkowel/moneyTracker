from dash import dash_table
import pandas as pd

def load_root_table(df, editable=False):
    if df is None or df.empty:
        return dash_table.DataTable(
            id="root-data-table",
            css=[{"selector":".dropdown", "rule": "position: static"}],
            columns=[],
            data=[],
            editable=editable,
            page_size=15,
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '5px',
                'minWidth': '100px',
                'maxWidth': '200px',
                'whiteSpace': 'normal'
            },
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold',
                'textAlign': 'center'
            }
        )

    if "Category" in df.columns:
        df["__CategoryOrder"] = df["Category"].apply(lambda x: 0 if str(x).strip().lower() == "uncategorized" else 1)
        df = df.sort_values(by=["__CategoryOrder", "Date"], ascending=[True, False]).drop(columns="__CategoryOrder")

    possible_categories = sorted(set(df['Category'].dropna().unique()))
    columns = []
    dropdown = {}

    for col in df.columns:
        if col == "Category" and editable:
            columns.append({
                "name": col,
                "id": col,
                "editable": True,
                "presentation": "dropdown"
            })
            dropdown[col] = {"options": [{"label": cat, "value": cat} for cat in possible_categories]}
        else:
            columns.append({"name": col, "id": col, "editable": editable})

    return dash_table.DataTable(
        id="root-data-table",
        css=[{"selector":".dropdown", "rule": "position: static"}],
        columns=columns,
        data=df.to_dict("records"),
        editable=editable,
        dropdown=dropdown if editable else {},
        page_size=15,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '5px',
            'minWidth': '100px',
            'maxWidth': '200px',
            'whiteSpace': 'normal'
        },
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_data_conditional=[
            {"if": {"filter_query": '{Category} = "Uncategorized"'}, "backgroundColor": "#ffe6e6", "color": "black"}
        ]
    )
