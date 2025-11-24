"""Main entry point that delegates to smart_contracts.app for Streamlit UI."""

from importlib import util
from pathlib import Path


def _load_app_module():
    app_path = Path(__file__).with_name("app.py")
    spec = util.spec_from_file_location("smart_contracts_app", app_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load Streamlit app from {app_path}")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


app_module = _load_app_module()

if hasattr(app_module, "render_app"):
    app_module.render_app()
