# utils/icon_utils.py - Enhanced Bootstrap Icons utility functions for Haven Frontend
# Updated version that integrates with the new professional navigation

import streamlit as st
import os
import base64
from typing import Optional

# Bootstrap Icons Path - Updated for your setup
BOOTSTRAP_ICONS_PATH = "assets"  # Your icons are in assets/ directory

def display_icon(icon_name: str, width: int = 20, height: Optional[int] = None) -> None:
    """
    Display a Bootstrap icon from the bootstrap-icons/icons directory.
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
        width (int): Width of the icon in pixels (defaults to 20)
        height (Optional[int]): Height of the icon in pixels (defaults to width)
    
    Example:
        display_icon("house-fill", 24)
        display_icon("heart", 20, 20)
        display_icon("currency-dollar", 32)
    """
    if height is None:
        height = width
    
    icon_path = os.path.join(BOOTSTRAP_ICONS_PATH, f"{icon_name}.svg")
    
    if os.path.exists(icon_path):
        try:
            st.image(icon_path, width=width)
        except Exception as e:
            st.error(f"Error displaying icon '{icon_name}': {e}")
    else:
        st.error(f"Icon '{icon_name}' not found in {BOOTSTRAP_ICONS_PATH}/")

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
    else:
        return f'<span style="margin-right: 5px;">[{icon_name}?]</span>'

def get_icon_html_b64(icon_name: str, size: int = 16, color_filter: str = "") -> str:
    """
    Get HTML string for inline icon usage with base64 encoding.
    This solves deployment and path issues.
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
        size (int): Size in pixels
        color_filter (str): CSS filter for coloring
    
    Returns:
        str: HTML string with base64 encoded icon
    
    Example:
        get_icon_html_b64("house-fill", 20)
        get_icon_html_b64("heart", 16, "invert(27%) sepia(51%) saturate(2878%)")
    """
    icon_path = os.path.join(BOOTSTRAP_ICONS_PATH, f"{icon_name}.svg")
    
    if os.path.exists(icon_path):
        try:
            with open(icon_path, "rb") as f:
                svg_data = f.read()
            
            b64_svg = base64.b64encode(svg_data).decode()
            
            filter_style = f"filter: {color_filter};" if color_filter else ""
            
            return f'''<img src="data:image/svg+xml;base64,{b64_svg}" 
                       width="{size}" height="{size}" 
                       style="vertical-align: middle; margin-right: 5px; {filter_style}" 
                       alt="{icon_name}">'''
        except Exception as e:
            return f'<span style="margin-right: 5px;">[{icon_name}?]</span>'
    else:
        return f'<span style="margin-right: 5px;">[{icon_name}?]</span>'

def icon_button(icon_name: str, label: str, key: str, icon_size: int = 20) -> bool:
    """
    Create a button with an icon and label.
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
        label (str): Button label
        key (str): Unique key for the button
        icon_size (int): Size of the icon in pixels
    
    Returns:
        bool: True if button was clicked
    
    Example:
        if icon_button("search", "Search", "search_btn"):
            st.write("Search clicked!")
    """
    col1, col2 = st.columns([1, 4])
    
    with col1:
        display_icon(icon_name, icon_size)
    
    with col2:
        return st.button(label, key=key)

def icon_button_html(icon_name: str, label: str, key: str, icon_size: int = 20) -> bool:
    """
    Create a button with an icon using HTML (more reliable for navigation).
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
        label (str): Button label
        key (str): Unique key for the button
        icon_size (int): Size of the icon in pixels
    
    Returns:
        bool: True if button was clicked
    
    Example:
        if icon_button_html("home", "Home", "home_btn"):
            st.write("Home clicked!")
    """
    icon_html = get_icon_html_b64(icon_name, icon_size)
    
    # Display icon with HTML
    st.markdown(f"{icon_html} {label}", unsafe_allow_html=True)
    
    # Return button state
    return st.button(f"→ {label}", key=key, help=f"Navigate to {label}")

def verify_icon_exists(icon_name: str) -> bool:
    """
    Check if an icon file exists.
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
    
    Returns:
        bool: True if icon exists, False otherwise
    
    Example:
        if verify_icon_exists("house-fill"):
            display_icon("house-fill")
    """
    icon_path = os.path.join(BOOTSTRAP_ICONS_PATH, f"{icon_name}.svg")
    return os.path.exists(icon_path)

def list_available_icons() -> list:
    """
    Get list of available Bootstrap icons.
    
    Returns:
        list: List of available icon names (without .svg extension)
    
    Example:
        icons = list_available_icons()
        st.write(f"Available icons: {len(icons)}")
    """
    if not os.path.exists(BOOTSTRAP_ICONS_PATH):
        return []
    
    try:
        files = os.listdir(BOOTSTRAP_ICONS_PATH)
        icons = [f.replace('.svg', '') for f in files if f.endswith('.svg')]
        return sorted(icons)
    except Exception as e:
        st.error(f"Error listing icons: {e}")
        return []

def setup_verification() -> dict:
    """
    Verify Bootstrap icons setup and return status.
    
    Returns:
        dict: Setup status information
    
    Example:
        status = setup_verification()
        if status['success']:
            st.success(f"✅ {status['icon_count']} icons loaded successfully")
    """
    status = {
        'success': False,
        'path_exists': False,
        'icon_count': 0,
        'missing_icons': [],
        'message': ''
    }
    
    # Check if path exists
    if os.path.exists(BOOTSTRAP_ICONS_PATH):
        status['path_exists'] = True
        
        # Count icons
        icons = list_available_icons()
        status['icon_count'] = len(icons)
        
        # Check for essential icons
        essential_icons = [
            'house-fill', 'search', 'plus-circle-fill', 'person-circle',
            'currency-dollar', 'people-fill', 'trophy-fill', 'lightning-charge-fill',
            'star-fill', 'fire', 'wifi', 'patch-check-fill'
        ]
        
        missing = [icon for icon in essential_icons if not verify_icon_exists(icon)]
        status['missing_icons'] = missing
        
        if status['icon_count'] > 0:
            status['success'] = True
            if missing:
                status['message'] = f"✅ {status['icon_count']} icons loaded. ⚠️ {len(missing)} essential icons missing: {', '.join(missing)}"
            else:
                status['message'] = f"✅ {status['icon_count']} icons loaded successfully. All essential icons present."
        else:
            status['message'] = f"❌ No icons found in {BOOTSTRAP_ICONS_PATH}/"
    else:
        status['message'] = f"❌ Icons directory not found: {BOOTSTRAP_ICONS_PATH}/"
    
    return status

def display_icon_showcase(icons_per_row: int = 8) -> None:
    """
    Display a showcase of available icons.
    
    Args:
        icons_per_row (int): Number of icons to display per row
    
    Example:
        display_icon_showcase(6)
    """
    st.markdown("### 🎨 Available Bootstrap Icons")
    
    icons = list_available_icons()
    
    if not icons:
        st.error("No icons found. Please check your Bootstrap icons setup.")
        return
    
    st.markdown(f"**Total icons available: {len(icons)}**")
    
    # Display icons in grid
    for i in range(0, len(icons), icons_per_row):
        cols = st.columns(icons_per_row)
        
        for j, col in enumerate(cols):
            if i + j < len(icons):
                icon_name = icons[i + j]
                with col:
                    try:
                        display_icon(icon_name, 24)
                        st.caption(icon_name)
                    except:
                        st.caption(f"❌ {icon_name}")

def get_icon_categories() -> dict:
    """
    Get categorized list of common Bootstrap icons.
    
    Returns:
        dict: Dictionary of icon categories and their icons
    
    Example:
        categories = get_icon_categories()
        for category, icons in categories.items():
            st.write(f"{category}: {len(icons)} icons")
    """
    return {
        'Navigation': [
            'house-fill', 'house', 'search', 'compass', 'map',
            'arrow-left', 'arrow-right', 'arrow-up', 'arrow-down'
        ],
        'Actions': [
            'plus-circle-fill', 'plus', 'minus-circle-fill', 'minus',
            'x-circle-fill', 'x', 'check-circle-fill', 'check'
        ],
        'Social': [
            'people-fill', 'people', 'person-circle', 'person',
            'heart-fill', 'heart', 'share-fill', 'share'
        ],
        'Financial': [
            'currency-dollar', 'currency-euro', 'currency-pound',
            'credit-card-fill', 'credit-card', 'wallet-fill', 'wallet'
        ],
        'Status': [
            'trophy-fill', 'trophy', 'star-fill', 'star',
            'lightning-charge-fill', 'lightning-charge', 'fire'
        ],
        'Communication': [
            'envelope-fill', 'envelope', 'telephone-fill', 'telephone',
            'chat-fill', 'chat', 'question-circle-fill', 'question-circle'
        ],
        'Media': [
            'play-circle-fill', 'play-circle', 'pause-circle-fill',
            'stop-circle-fill', 'volume-up-fill', 'volume-mute-fill'
        ],
        'System': [
            'gear-fill', 'gear', 'wifi', 'patch-check-fill',
            'shield-fill-check', 'lock-fill', 'unlock-fill'
        ]
    }

# Color filter presets for different themes
COLOR_FILTERS = {
    'primary': 'invert(27%) sepia(51%) saturate(2878%) hue-rotate(346deg) brightness(104%) contrast(97%)',
    'secondary': 'invert(27%) sepia(98%) saturate(1000%) hue-rotate(196deg) brightness(104%) contrast(97%)',
    'success': 'invert(27%) sepia(51%) saturate(2878%) hue-rotate(346deg) brightness(104%) contrast(97%)',
    'warning': 'invert(27%) sepia(98%) saturate(1000%) hue-rotate(25deg) brightness(104%) contrast(97%)',
    'danger': 'invert(27%) sepia(98%) saturate(1000%) hue-rotate(0deg) brightness(104%) contrast(97%)',
    'info': 'invert(27%) sepia(98%) saturate(1000%) hue-rotate(196deg) brightness(104%) contrast(97%)',
    'white': 'invert(100%)',
    'black': 'invert(0%)'
}

def get_colored_icon_html(icon_name: str, size: int = 16, color_theme: str = 'primary') -> str:
    """
    Get colored icon HTML using predefined color themes.
    
    Args:
        icon_name (str): Name of the icon file (without .svg extension)
        size (int): Size in pixels
        color_theme (str): Color theme ('primary', 'secondary', 'success', etc.)
    
    Returns:
        str: HTML string with colored icon
    
    Example:
        get_colored_icon_html("heart", 20, "danger")
        get_colored_icon_html("star-fill", 24, "warning")
    """
    color_filter = COLOR_FILTERS.get(color_theme, COLOR_FILTERS['primary'])
    return get_icon_html_b64(icon_name, size, color_filter)

# Backward compatibility functions
def display_icon_old(icon_name: str, width: int = 20, height: Optional[int] = None) -> None:
    """Backward compatibility wrapper for display_icon."""
    display_icon(icon_name, width, height)

def get_icon_html_old(icon_name: str, size: int = 16, color: str = "currentColor") -> str:
    """Backward compatibility wrapper for get_icon_html."""
    return get_icon_html(icon_name, size, color)

# Export main functions for easy import
__all__ = [
    'display_icon',
    'get_icon_html',
    'get_icon_html_b64',
    'icon_button',
    'icon_button_html',
    'verify_icon_exists',
    'list_available_icons',
    'setup_verification',
    'display_icon_showcase',
    'get_icon_categories',
    'get_colored_icon_html',
    'COLOR_FILTERS',
    'BOOTSTRAP_ICONS_PATH'
]

# ================================
# USAGE EXAMPLES
# ================================

if __name__ == "__main__":
    # This section runs when the file is executed directly
    # Useful for testing the icon utilities
    
    st.title("🎨 Bootstrap Icons Utility Test")
    
    # Setup verification
    status = setup_verification()
    if status['success']:
        st.success(status['message'])
    else:
        st.error(status['message'])
        st.stop()
    
    # Display some example icons
    st.markdown("### Example Icons")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**display_icon():**")
        display_icon("house-fill", 32)
        st.caption("house-fill")
    
    with col2:
        st.markdown("**get_icon_html():**")
        html = get_icon_html("heart", 32, "#FF0000")
        st.markdown(html, unsafe_allow_html=True)
        st.caption("heart (red)")
    
    with col3:
        st.markdown("**get_icon_html_b64():**")
        html_b64 = get_icon_html_b64("star-fill", 32, COLOR_FILTERS['warning'])
        st.markdown(html_b64, unsafe_allow_html=True)
        st.caption("star-fill (warning)")
    
    with col4:
        st.markdown("**icon_button():**")
        if icon_button("search", "Search", "test_search"):
            st.success("Search clicked!")
    
    # Icon showcase
    with st.expander("🎨 Icon Showcase"):
        display_icon_showcase(6)
    
    # Categories
    with st.expander("📂 Icon Categories"):
        categories = get_icon_categories()
        for category, icons in categories.items():
            st.markdown(f"**{category}:** {', '.join(icons[:5])}{'...' if len(icons) > 5 else ''}")

