# In utils/icon_utils.py

import streamlit as st
from pathlib import Path
import base64

# --- New function to encode SVG to Base64 ---
@st.cache_data
def get_icon_as_base64(file_path: str) -> str:
    """Reads an SVG file and returns it as a Base64 encoded string."""
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        st.error(f"Icon not found at {file_path}: {e}")
        return ""

# --- Corrected function to display the icon ---
def display_icon(icon_name: str, color: str = "currentColor", size: int = 20):
    """
    Displays an icon by embedding its Base64-encoded SVG content.
    """
    icon_path = Path(f"assets/{icon_name}.svg")
    if not icon_path.exists():
        st.warning(f"Icon '{icon_name}' not found.")
        return

    icon_base64 = get_icon_as_base64(str(icon_path))
    
    st.markdown(
        f"""
        <div style="display: inline-block; vertical-align: middle;">
            <img src="data:image/svg+xml;base64,{icon_base64}" width="{size}" height="{size}" 
                 style="filter: invert(0.5) sepia(1) saturate(5) hue-rotate(100deg);">
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Kept your original nav_bar function, but it should also be updated if it uses icons ---
def nav_bar(authenticated: bool):
    # This function should be reviewed to use the new `display_icon` method if needed
    # Or preferably, use the streamlit-option-menu as we discussed
    pass

# You may not need this function anymore if you use display_icon
def get_icon_svg(icon_name: str, fill: str = "currentColor"):
    icon_path = Path(f"assets/{icon_name}.svg")
    if not icon_path.exists():
        return ""
    
    icon_base64 = get_icon_as_base64(str(icon_path))
    return f'<img src="data:image/svg+xml;base64,{icon_base64}" width="20" height="20">'
