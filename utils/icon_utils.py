# utils/icon_utils.py
# Bootstrap Icons utility functions for Haven Frontend

import streamlit as st
import os
from typing import Optional

# BOOTSTRAP ICONS PATH - Based on repository verification
BOOTSTRAP_ICONS_PATH = "assets"

def display_icon(icon_name: str, width: int = 20, height: Optional[int] = None) -> None:
    """
    Display a Bootstrap icon from the bootstrap-icons/icons directory.
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
        width (int): Width of the icon in pixels
        height (Optional[int]): Height of the icon in pixels (defaults to width)
    
    Example:
        display_icon("house-fill", 24)
        display_icon("heart", 20)
        display_icon("currency-dollar", 32)
    """
    icon_path = os.path.join(BOOTSTRAP_ICONS_PATH, f"{icon_name}.svg")
    if os.path.exists(icon_path):
        st.image(icon_path, width=width)
    else:
        st.error(f"Icon '{icon_name}' not found in {BOOTSTRAP_ICONS_PATH}/")
        st.info(f"Looking for: {icon_path}")

def get_icon_html(icon_name: str, size: int = 16, color: str = "currentColor", css_class: str = "") -> str:
    """
    Get HTML string for inline icon usage.
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
        size (int): Size in pixels
        color (str): CSS color value
        css_class (str): Additional CSS classes
    
    Returns:
        str: HTML string for the icon
    
    Example:
        get_icon_html("house-fill", 20, "#4CAF50")
        get_icon_html("heart", 16, "red")
    """
    icon_path = os.path.join(BOOTSTRAP_ICONS_PATH, f"{icon_name}.svg")
    if os.path.exists(icon_path):
        return f'''<img src="{icon_path}" width="{size}" height="{size}" 
                   style="color: {color}; vertical-align: middle; margin-right: 5px;" 
                   class="{css_class}" alt="{icon_name}">'''
    return f'<span style="color: red; font-size: {size}px;">[{icon_name}?]</span>'

def icon_button(icon_name: str, label: str, key: str, icon_size: int = 20) -> bool:
    """
    Create a button with an icon and label.
    
    Args:
        icon_name (str): Name of the icon
        label (str): Button label
        key (str): Unique key for the button
        icon_size (int): Size of the icon
    
    Returns:
        bool: True if button was clicked
    """
    if st.button(f"{get_icon_html(icon_name, icon_size)} {label}", key=key, help=label):
        return True
    return False

def verify_icon_exists(icon_name: str) -> bool:
    """
    Check if an icon exists in the bootstrap-icons directory.
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
    
    Returns:
        bool: True if icon exists, False otherwise
    """
    icon_path = os.path.join(BOOTSTRAP_ICONS_PATH, f"{icon_name}.svg")
    return os.path.exists(icon_path)

def list_available_icons(limit: int = 50) -> list:
    """
    List available icons in the bootstrap-icons directory.
    
    Args:
        limit (int): Maximum number of icons to return
    
    Returns:
        list: List of available icon names (without .svg extension)
    """
    if not os.path.exists(BOOTSTRAP_ICONS_PATH):
        return []
    
    icons = []
    for file in os.listdir(BOOTSTRAP_ICONS_PATH):
        if file.endswith('.svg'):
            icons.append(file[:-4])  # Remove .svg extension
            if len(icons) >= limit:
                break
    
    return sorted(icons)

def get_icon_path(icon_name: str) -> str:
    """
    Get the full path to an icon file.
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
    
    Returns:
        str: Full path to the icon file
    """
    return os.path.join(BOOTSTRAP_ICONS_PATH, f"{icon_name}.svg")

def render_icon_showcase(title: str = "Available Icons", limit: int = 20) -> None:
    """
    Render a showcase of available icons for testing.
    
    Args:
        title (str): Title for the showcase
        limit (int): Number of icons to display
    """
    st.markdown(f"### {title}")
    
    icons = list_available_icons(limit)
    if not icons:
        st.error("No icons found. Please check your bootstrap-icons setup.")
        return
    
    # Display icons in a grid
    cols = st.columns(4)
    for i, icon_name in enumerate(icons):
        with cols[i % 4]:
            if verify_icon_exists(icon_name):
                display_icon(icon_name, 24)
                st.caption(f"✅ {icon_name}")
            else:
                st.error(f"❌ {icon_name}")

def setup_verification() -> bool:
    """
    Verify that the Bootstrap icons setup is correct.
    
    Returns:
        bool: True if setup is correct, False otherwise
    """
    if not os.path.exists(BOOTSTRAP_ICONS_PATH):
        st.error(f"""
        ⚠️ **Bootstrap Icons directory not found!**
        
        Expected path: `{BOOTSTRAP_ICONS_PATH}`
        
        Please ensure you have:
        1. Downloaded the bootstrap-icons repository
        2. Copied the `bootstrap-icons/icons/` directory to your project root
        
        Directory structure should be:
        ```
        your-haven-project/
        ├── bootstrap-icons/
        │   └── icons/
        │       ├── house-fill.svg
        │       ├── heart.svg
        │       ├── currency-dollar.svg
        │       └── ... (1000+ more icons)
        ├── app.py
        └── utils/
            └── icon_utils.py
        ```
        """)
        return False
    
    # Count available icons
    icon_count = len([f for f in os.listdir(BOOTSTRAP_ICONS_PATH) if f.endswith('.svg')])
    
    if icon_count == 0:
        st.error("No SVG files found in the bootstrap-icons directory!")
        return False
    
    st.success(f"✅ Bootstrap Icons loaded successfully! ({icon_count} icons available)")
    return True

# Common icon sets for quick access
COMMON_ICONS = {
    'navigation': ['house-fill', 'search', 'plus-circle-fill', 'person-circle', 'gear-fill'],
    'actions': ['heart', 'share', 'bookmark', 'download', 'upload', 'edit', 'delete'],
    'status': ['check-circle-fill', 'x-circle-fill', 'clock-fill', 'exclamation-triangle'],
    'financial': ['currency-dollar', 'credit-card', 'bank', 'cash-coin', 'wallet2'],
    'communication': ['envelope', 'chat-dots', 'telephone', 'bell', 'megaphone'],
    'media': ['image', 'play-circle', 'camera', 'video', 'music-note']
}

def get_common_icons(category: str) -> list:
    """
    Get a list of common icons for a specific category.
    
    Args:
        category (str): Category name ('navigation', 'actions', 'status', etc.)
    
    Returns:
        list: List of icon names for the category
    """
    return COMMON_ICONS.get(category, [])

