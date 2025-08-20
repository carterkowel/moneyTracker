from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

def editor_toggle():
    return html.Div([
        html.Div(
            "📝 Viewer Mode",
            id="editor-toggle-label",
            style={
                "textAlign": "center",
                "marginBottom": "0.25rem",
                "fontWeight": "bold"
            }
        ),
        daq.ToggleSwitch(
            id="editor-toggle-btn",
            value=False,
            style={"marginBottom": "0rem"}
        ),
        dcc.Store(id="editor-mode-flag", data=False),
        dcc.Store(id="edited-data-store"),

        dbc.Modal(
            [
                dbc.ModalHeader("Save Changes?"),
                dbc.ModalBody("You have unsaved edits. Would you like to save them?"),
                dbc.ModalFooter([
                    dbc.Button("Save", id="confirm-save-btn", color="success", className="me-2"),
                    dbc.Button("Discard", id="discard-changes-btn", color="secondary"),
                ])
            ],
            id="save-confirm-modal",
            is_open=False
        )
    ])
