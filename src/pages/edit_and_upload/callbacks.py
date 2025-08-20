import io
import os
import dash
import pandas as pd
from dash import html, Input, Output, State, callback
from contextlib import redirect_stdout


from utils import process_uploaded_statements, update_root_csv, assign_categories, assign_necessities, read_root_csv, CLEANED_DIR
from .components import load_card_currentness, load_root_table


def render_summary_and_table(is_editor_mode):
    """Read the root CSV and return both summary cards and table."""
    df = read_root_csv()
    return (
        load_card_currentness(df),
        load_root_table(df, editable=is_editor_mode),
    )

def save_table_to_csv(table_data):
    """Save edited table data to root.csv and re-assign necessities."""
    df = pd.DataFrame(table_data)

    root_csv_path = os.path.join(CLEANED_DIR, "root.csv")

    df = assign_necessities(df)
    df.to_csv(root_csv_path, index=False)
    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    return read_root_csv()

def get_triggered_id():
    """Central helper to get the ID of the component that triggered the callback."""
    ctx = dash.callback_context
    return ctx.triggered_id if ctx.triggered else None


@callback(
    Output('upload-output', 'children'),
    Output('temp-df-store', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def handle_file_upload(list_of_contents, list_of_names):
    if not list_of_contents:
        return "⚠️ No files uploaded.", None

    try:
        df, output_msg = process_uploaded_statements(list_of_contents, list_of_names)
        if df is None or df.empty:
            return f"{output_msg}\n⚠️ No valid transactions extracted.", None
        return output_msg, df.to_json(date_format='iso', orient='split')
    except Exception as e:
        return f"⚠️ Error processing uploaded files: {e}", None


@callback(
    Output('run-updater-output', 'children'),
    Output('csv-updated-flag', 'data'),
    Input('run-updater-btn', 'n_clicks'),
    State('temp-df-store', 'data'),
    prevent_initial_call=True
)
def run_statement_updater(n_clicks, stored_df_json):
    f = io.StringIO()
    try:
        if stored_df_json is None:
            return html.Div(
                "⚠️ No data to update. Please process statements first.", 
                style={'color':'orange'}
            ), dash.no_update

        df = pd.read_json(stored_df_json, orient='split')
        with redirect_stdout(f):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            root_csv_path = os.path.join(CLEANED_DIR, "root.csv")

            categorized_df = assign_categories(df)
            full_categorized_df = assign_necessities(categorized_df)
            update_root_csv(root_csv_path, full_categorized_df)
        return html.Pre(f.getvalue()), True
    except Exception as e:
        return html.Div(f"⚠️ Error while updating root CSV: {e}", style={'color':'red'}), dash.no_update


@callback(
    Output('transaction-summary', 'children'),
    Output('root-table-container', 'children'),
    Output('editor-mode-flag', 'data'),
    Output('save-confirm-modal', 'is_open'),
    Input('editor-toggle-btn', 'value'),
    Input('confirm-save-btn', 'n_clicks'),
    Input('discard-changes-btn', 'n_clicks'),
    Input('csv-updated-flag', 'data'),
    Input('url', 'pathname'),
    State('editor-mode-flag', 'data'),
    State('root-data-table', 'data'),
    prevent_initial_call=True
)
def handle_editor_and_updates(editor_mode_value, save_click, discard_click, csv_flag, pathname, is_editor_mode, table_data):
    triggered_id = get_triggered_id()

    # CSV updated, page load, or some-trigger refresh
    if triggered_id in ['csv-updated-flag', 'url']:
        return *render_summary_and_table(is_editor_mode), is_editor_mode, False

    # Editor toggle
    if triggered_id == 'editor-toggle-btn':
        if editor_mode_value and not is_editor_mode:
            return dash.no_update, load_root_table(read_root_csv(), editable=True), True, False
        elif not editor_mode_value and is_editor_mode:
            return dash.no_update, dash.no_update, dash.no_update, True

    # Save
    if triggered_id == 'confirm-save-btn':
        try:
            df_updated = save_table_to_csv(table_data)
            return load_card_currentness(df_updated), load_root_table(df_updated, editable=False), False, False
        except Exception as e:
            return html.Div(f"⚠️ Failed to save CSV: {e}"), dash.no_update, False, False

    # Discard
    if triggered_id == 'discard-changes-btn':
        return *render_summary_and_table(False), False, False

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update


@callback(
    Output("editor-toggle-label", "children"),
    Output("editor-toggle-btn", "color"),
    Input("editor-toggle-btn", "value")
)
def update_editor_toggle(is_edit_mode):
    label = "🛠️ Editor Mode (toggle back to save)" if is_edit_mode else "📝 Viewer Mode"
    color = "#007bff" if is_edit_mode else "#d3d3d3"
    return label, color