# config/icon_mapping.py - Enhanced Bootstrap Icons mapping for Haven Frontend
# Updated version that integrates with the new professional navigation

from typing import Dict, List, Optional, Union

# ================================
# ICON CATEGORIES AND MAPPINGS
# ================================

# Navigation icons for different sections
NAVIGATION_ICONS = {
    'home': 'house-fill',
    'dashboard': 'speedometer2',
    'profile': 'person-circle',
    'settings': 'gear-fill',
    'search': 'search',
    'browse': 'search',
    'explore': 'compass-fill',
    'help': 'question-circle-fill',
    'support': 'headset',
    'about': 'info-circle-fill',
    'contact': 'envelope-fill',
    'menu': 'list',
    'back': 'arrow-left',
    'forward': 'arrow-right',
    'up': 'arrow-up',
    'down': 'arrow-down'
}

# Authentication and user management icons
AUTHENTICATION_ICONS = {
    'login': 'box-arrow-in-right',
    'logout': 'box-arrow-right',
    'register': 'person-plus-fill',
    'signup': 'person-plus-fill',
    'user': 'person-circle',
    'users': 'people-fill',
    'admin': 'person-badge-fill',
    'password': 'key-fill',
    'security': 'shield-fill-check',
    'privacy': 'eye-slash-fill',
    'account': 'person-gear',
    'verification': 'patch-check-fill',
    'verified': 'patch-check-fill',
    'unverified': 'patch-exclamation-fill'
}

# Financial and crowdfunding specific icons
FINANCIAL_ICONS = {
    'money': 'currency-dollar',
    'dollar': 'currency-dollar',
    'euro': 'currency-euro',
    'pound': 'currency-pound',
    'bitcoin': 'currency-bitcoin',
    'payment': 'credit-card-fill',
    'card': 'credit-card-fill',
    'wallet': 'wallet-fill',
    'bank': 'bank2',
    'transfer': 'arrow-left-right',
    'funding': 'cash-stack',
    'donation': 'heart-fill',
    'investment': 'graph-up-arrow',
    'revenue': 'graph-up',
    'profit': 'trending-up',
    'loss': 'trending-down',
    'campaign': 'megaphone-fill',
    'goal': 'bullseye',
    'target': 'bullseye',
    'progress': 'bar-chart-fill',
    'percentage': 'percent',
    'calculator': 'calculator-fill'
}

# Action and interaction icons
ACTION_ICONS = {
    'create': 'plus-circle-fill',
    'add': 'plus-circle-fill',
    'new': 'plus-circle-fill',
    'edit': 'pencil-fill',
    'update': 'pencil-fill',
    'delete': 'trash-fill',
    'remove': 'x-circle-fill',
    'save': 'floppy-fill',
    'download': 'download',
    'upload': 'upload',
    'share': 'share-fill',
    'copy': 'clipboard-fill',
    'paste': 'clipboard-plus-fill',
    'cut': 'scissors',
    'undo': 'arrow-counterclockwise',
    'redo': 'arrow-clockwise',
    'refresh': 'arrow-clockwise',
    'reload': 'arrow-clockwise',
    'sync': 'arrow-repeat',
    'submit': 'check-circle-fill',
    'confirm': 'check-circle-fill',
    'approve': 'check-circle-fill',
    'reject': 'x-circle-fill',
    'cancel': 'x-circle-fill',
    'close': 'x-lg',
    'expand': 'arrows-fullscreen',
    'collapse': 'arrows-collapse',
    'maximize': 'fullscreen',
    'minimize': 'fullscreen-exit'
}

# Status and feedback icons
STATUS_ICONS = {
    'success': 'check-circle-fill',
    'error': 'x-circle-fill',
    'warning': 'exclamation-triangle-fill',
    'info': 'info-circle-fill',
    'pending': 'clock-fill',
    'loading': 'arrow-clockwise',
    'active': 'lightning-charge-fill',
    'inactive': 'pause-circle-fill',
    'online': 'wifi',
    'offline': 'wifi-off',
    'connected': 'link-45deg',
    'disconnected': 'link-45deg',
    'verified': 'patch-check-fill',
    'unverified': 'patch-exclamation-fill',
    'featured': 'star-fill',
    'popular': 'fire',
    'trending': 'graph-up-arrow',
    'new': 'badge-wc-fill',
    'hot': 'fire',
    'completed': 'check-circle-fill',
    'failed': 'x-circle-fill',
    'cancelled': 'dash-circle-fill'
}

# Social and community icons
SOCIAL_ICONS = {
    'like': 'heart-fill',
    'love': 'heart-fill',
    'favorite': 'heart-fill',
    'bookmark': 'bookmark-fill',
    'follow': 'person-plus-fill',
    'unfollow': 'person-dash-fill',
    'comment': 'chat-fill',
    'message': 'envelope-fill',
    'notification': 'bell-fill',
    'alert': 'bell-fill',
    'community': 'people-fill',
    'team': 'people-fill',
    'group': 'people-fill',
    'network': 'diagram-3-fill',
    'connection': 'link-45deg',
    'feedback': 'chat-square-text-fill',
    'review': 'star-fill',
    'rating': 'star-fill',
    'vote': 'hand-thumbs-up-fill',
    'upvote': 'hand-thumbs-up-fill',
    'downvote': 'hand-thumbs-down-fill'
}

# Media and content icons
MEDIA_ICONS = {
    'image': 'image-fill',
    'video': 'play-circle-fill',
    'audio': 'music-note-beamed',
    'document': 'file-text-fill',
    'pdf': 'file-pdf-fill',
    'file': 'file-fill',
    'folder': 'folder-fill',
    'gallery': 'images',
    'camera': 'camera-fill',
    'microphone': 'mic-fill',
    'speaker': 'volume-up-fill',
    'mute': 'volume-mute-fill',
    'play': 'play-fill',
    'pause': 'pause-fill',
    'stop': 'stop-fill',
    'record': 'record-circle-fill',
    'fullscreen': 'fullscreen',
    'zoom': 'zoom-in'
}

# System and technical icons
SYSTEM_ICONS = {
    'settings': 'gear-fill',
    'config': 'sliders',
    'tools': 'tools',
    'code': 'code-slash',
    'database': 'server',
    'cloud': 'cloud-fill',
    'api': 'diagram-3-fill',
    'webhook': 'arrow-down-up',
    'integration': 'puzzle-fill',
    'plugin': 'plugin',
    'extension': 'puzzle-fill',
    'backup': 'shield-fill-check',
    'restore': 'arrow-counterclockwise',
    'export': 'box-arrow-up',
    'import': 'box-arrow-in-down',
    'filter': 'funnel-fill',
    'sort': 'sort-down',
    'search': 'search',
    'find': 'search',
    'locate': 'geo-alt-fill'
}

# Time and calendar icons
TIME_ICONS = {
    'time': 'clock-fill',
    'clock': 'clock-fill',
    'calendar': 'calendar-fill',
    'date': 'calendar-date-fill',
    'schedule': 'calendar-check-fill',
    'deadline': 'alarm-fill',
    'timer': 'stopwatch-fill',
    'history': 'clock-history',
    'recent': 'clock-history',
    'future': 'clock-fill',
    'past': 'clock-history',
    'today': 'calendar-day-fill',
    'tomorrow': 'calendar-plus-fill',
    'yesterday': 'calendar-minus-fill'
}

# E-commerce and business icons
BUSINESS_ICONS = {
    'cart': 'cart-fill',
    'shopping': 'bag-fill',
    'store': 'shop',
    'product': 'box-fill',
    'inventory': 'boxes',
    'order': 'receipt-cutoff',
    'invoice': 'receipt',
    'shipping': 'truck',
    'delivery': 'truck',
    'package': 'box-seam-fill',
    'warehouse': 'building-fill',
    'supplier': 'person-workspace',
    'customer': 'person-heart',
    'client': 'person-check-fill',
    'vendor': 'person-badge-fill',
    'partner': 'handshake-fill',
    'contract': 'file-text-fill',
    'agreement': 'file-check-fill'
}

# ================================
# COLOR SCHEMES
# ================================

# Primary color palette for Haven platform
ICON_COLORS = {
    'primary': '#4CAF50',      # Green - main brand color
    'secondary': '#2196F3',    # Blue - secondary actions
    'success': '#4CAF50',      # Green - success states
    'warning': '#FF9800',      # Orange - warnings
    'danger': '#F44336',       # Red - errors/danger
    'info': '#2196F3',         # Blue - information
    'light': '#F5F5F5',        # Light gray
    'dark': '#333333',         # Dark gray
    'white': '#FFFFFF',        # White
    'black': '#000000',        # Black
    'muted': '#6C757D',        # Muted gray
    'accent': '#9C27B0',       # Purple - accent color
    'financial': '#4CAF50',    # Green - financial success
    'social': '#E91E63',       # Pink - social interactions
    'system': '#607D8B',       # Blue gray - system functions
    'media': '#FF5722'         # Deep orange - media content
}

# Contextual color mappings
CONTEXTUAL_COLORS = {
    'navigation': ICON_COLORS['primary'],
    'authentication': ICON_COLORS['secondary'],
    'financial': ICON_COLORS['financial'],
    'actions': ICON_COLORS['primary'],
    'status': ICON_COLORS['info'],
    'social': ICON_COLORS['social'],
    'media': ICON_COLORS['media'],
    'system': ICON_COLORS['system'],
    'time': ICON_COLORS['muted'],
    'business': ICON_COLORS['accent']
}

# ================================
# SIZE PRESETS
# ================================

ICON_SIZES = {
    'xs': 12,      # Extra small
    'sm': 16,      # Small
    'md': 20,      # Medium (default)
    'lg': 24,      # Large
    'xl': 32,      # Extra large
    'xxl': 48,     # Extra extra large
    'hero': 64,    # Hero size
    'jumbo': 96    # Jumbo size
}

# ================================
# UTILITY FUNCTIONS
# ================================

def get_icon(category: str, icon_key: str) -> Optional[str]:
    """
    Get icon name from category and key.
    
    Args:
        category (str): Icon category ('navigation', 'financial', etc.)
        icon_key (str): Icon key within the category
    
    Returns:
        Optional[str]: Icon filename (without .svg) or None if not found
    
    Example:
        get_icon('navigation', 'home')  # Returns 'house-fill'
        get_icon('financial', 'money')  # Returns 'currency-dollar'
    """
    category_maps = {
        'navigation': NAVIGATION_ICONS,
        'auth': AUTHENTICATION_ICONS,
        'authentication': AUTHENTICATION_ICONS,
        'financial': FINANCIAL_ICONS,
        'money': FINANCIAL_ICONS,
        'actions': ACTION_ICONS,
        'action': ACTION_ICONS,
        'status': STATUS_ICONS,
        'social': SOCIAL_ICONS,
        'media': MEDIA_ICONS,
        'system': SYSTEM_ICONS,
        'time': TIME_ICONS,
        'business': BUSINESS_ICONS,
        'ui': ACTION_ICONS  # Alias for actions
    }
    
    category_map = category_maps.get(category.lower())
    if category_map:
        return category_map.get(icon_key.lower())
    
    return None

def get_icon_by_category(category: str) -> Dict[str, str]:
    """
    Get all icons in a specific category.
    
    Args:
        category (str): Icon category name
    
    Returns:
        Dict[str, str]: Dictionary of icon keys and their filenames
    
    Example:
        nav_icons = get_icon_by_category('navigation')
        # Returns {'home': 'house-fill', 'dashboard': 'speedometer2', ...}
    """
    category_maps = {
        'navigation': NAVIGATION_ICONS,
        'authentication': AUTHENTICATION_ICONS,
        'financial': FINANCIAL_ICONS,
        'actions': ACTION_ICONS,
        'status': STATUS_ICONS,
        'social': SOCIAL_ICONS,
        'media': MEDIA_ICONS,
        'system': SYSTEM_ICONS,
        'time': TIME_ICONS,
        'business': BUSINESS_ICONS
    }
    
    return category_maps.get(category.lower(), {})

def get_all_categories() -> List[str]:
    """
    Get list of all available icon categories.
    
    Returns:
        List[str]: List of category names
    
    Example:
        categories = get_all_categories()
        # Returns ['navigation', 'authentication', 'financial', ...]
    """
    return [
        'navigation', 'authentication', 'financial', 'actions',
        'status', 'social', 'media', 'system', 'time', 'business'
    ]

def search_icons(query: str) -> Dict[str, List[str]]:
    """
    Search for icons across all categories.
    
    Args:
        query (str): Search query
    
    Returns:
        Dict[str, List[str]]: Dictionary with categories as keys and matching icons as values
    
    Example:
        results = search_icons('user')
        # Returns {'authentication': ['user', 'users'], 'social': ['user'], ...}
    """
    results = {}
    query_lower = query.lower()
    
    all_categories = {
        'navigation': NAVIGATION_ICONS,
        'authentication': AUTHENTICATION_ICONS,
        'financial': FINANCIAL_ICONS,
        'actions': ACTION_ICONS,
        'status': STATUS_ICONS,
        'social': SOCIAL_ICONS,
        'media': MEDIA_ICONS,
        'system': SYSTEM_ICONS,
        'time': TIME_ICONS,
        'business': BUSINESS_ICONS
    }
    
    for category, icons in all_categories.items():
        matches = []
        for key, icon_name in icons.items():
            if query_lower in key.lower() or query_lower in icon_name.lower():
                matches.append(key)
        
        if matches:
            results[category] = matches
    
    return results

def get_icon_color(category: str) -> str:
    """
    Get the default color for a specific category.
    
    Args:
        category (str): Icon category name
    
    Returns:
        str: Hex color code
    
    Example:
        color = get_icon_color('financial')  # Returns '#4CAF50'
    """
    return CONTEXTUAL_COLORS.get(category.lower(), ICON_COLORS['primary'])

def get_icon_size(size_key: str) -> int:
    """
    Get pixel size for a size key.
    
    Args:
        size_key (str): Size key ('xs', 'sm', 'md', etc.)
    
    Returns:
        int: Size in pixels
    
    Example:
        size = get_icon_size('lg')  # Returns 24
    """
    return ICON_SIZES.get(size_key.lower(), ICON_SIZES['md'])

def create_icon_config(category: str, icon_key: str, size: str = 'md', color: Optional[str] = None) -> Dict[str, Union[str, int]]:
    """
    Create a complete icon configuration.
    
    Args:
        category (str): Icon category
        icon_key (str): Icon key within category
        size (str): Size key
        color (Optional[str]): Custom color (uses category default if None)
    
    Returns:
        Dict[str, Union[str, int]]: Complete icon configuration
    
    Example:
        config = create_icon_config('navigation', 'home', 'lg')
        # Returns {'icon': 'house-fill', 'size': 24, 'color': '#4CAF50'}
    """
    icon_name = get_icon(category, icon_key)
    icon_size = get_icon_size(size)
    icon_color = color or get_icon_color(category)
    
    return {
        'icon': icon_name,
        'size': icon_size,
        'color': icon_color,
        'category': category,
        'key': icon_key
    }

# ================================
# HAVEN PLATFORM SPECIFIC MAPPINGS
# ================================

# Specific icon mappings for Haven crowdfunding platform
HAVEN_SPECIFIC_ICONS = {
    'campaign': 'megaphone-fill',
    'project': 'lightbulb-fill',
    'backer': 'person-heart',
    'creator': 'person-workspace',
    'reward': 'gift-fill',
    'tier': 'layers-fill',
    'milestone': 'flag-fill',
    'update': 'newspaper',
    'pledge': 'hand-thumbs-up-fill',
    'contribution': 'heart-fill',
    'supporter': 'person-plus-fill',
    'innovation': 'lightbulb-fill',
    'startup': 'rocket-takeoff-fill',
    'entrepreneur': 'person-badge-fill',
    'crowdfunding': 'people-fill',
    'fundraising': 'cash-stack',
    'investment_round': 'arrow-up-circle-fill',
    'equity': 'pie-chart-fill',
    'valuation': 'graph-up-arrow',
    'pitch': 'presentation',
    'demo': 'play-circle-fill',
    'prototype': 'cpu-fill',
    'mvp': 'award-fill',
    'launch': 'rocket-takeoff-fill',
    'pre_order': 'cart-plus-fill',
    'early_bird': 'clock-fill',
    'stretch_goal': 'bullseye',
    'funding_goal': 'target',
    'campaign_end': 'calendar-x-fill',
    'success_story': 'trophy-fill',
    'testimonial': 'chat-quote-fill'
}

# UI patterns for common Haven platform elements
HAVEN_UI_PATTERNS = {
    'primary_button': {
        'icon': 'arrow-right-circle-fill',
        'size': 'md',
        'color': ICON_COLORS['primary']
    },
    'secondary_button': {
        'icon': 'arrow-right',
        'size': 'sm',
        'color': ICON_COLORS['secondary']
    },
    'danger_button': {
        'icon': 'x-circle-fill',
        'size': 'md',
        'color': ICON_COLORS['danger']
    },
    'success_message': {
        'icon': 'check-circle-fill',
        'size': 'lg',
        'color': ICON_COLORS['success']
    },
    'error_message': {
        'icon': 'x-circle-fill',
        'size': 'lg',
        'color': ICON_COLORS['danger']
    },
    'warning_message': {
        'icon': 'exclamation-triangle-fill',
        'size': 'lg',
        'color': ICON_COLORS['warning']
    },
    'info_message': {
        'icon': 'info-circle-fill',
        'size': 'lg',
        'color': ICON_COLORS['info']
    },
    'loading_spinner': {
        'icon': 'arrow-clockwise',
        'size': 'md',
        'color': ICON_COLORS['primary']
    },
    'empty_state': {
        'icon': 'inbox',
        'size': 'hero',
        'color': ICON_COLORS['muted']
    }
}

def get_haven_icon(icon_key: str) -> Optional[str]:
    """
    Get Haven-specific icon.
    
    Args:
        icon_key (str): Haven-specific icon key
    
    Returns:
        Optional[str]: Icon filename or None if not found
    
    Example:
        get_haven_icon('campaign')  # Returns 'megaphone-fill'
    """
    return HAVEN_SPECIFIC_ICONS.get(icon_key.lower())

def get_ui_pattern(pattern_key: str) -> Optional[Dict[str, Union[str, int]]]:
    """
    Get UI pattern configuration.
    
    Args:
        pattern_key (str): UI pattern key
    
    Returns:
        Optional[Dict]: Pattern configuration or None if not found
    
    Example:
        pattern = get_ui_pattern('primary_button')
        # Returns {'icon': 'arrow-right-circle-fill', 'size': 'md', 'color': '#4CAF50'}
    """
    return HAVEN_UI_PATTERNS.get(pattern_key.lower())

# ================================
# EXPORT ALL MAPPINGS
# ================================

# Main mappings dictionary for easy access
ALL_ICON_MAPPINGS = {
    'navigation': NAVIGATION_ICONS,
    'authentication': AUTHENTICATION_ICONS,
    'financial': FINANCIAL_ICONS,
    'actions': ACTION_ICONS,
    'status': STATUS_ICONS,
    'social': SOCIAL_ICONS,
    'media': MEDIA_ICONS,
    'system': SYSTEM_ICONS,
    'time': TIME_ICONS,
    'business': BUSINESS_ICONS,
    'haven': HAVEN_SPECIFIC_ICONS
}

# Export main functions and constants
__all__ = [
    'get_icon',
    'get_icon_by_category',
    'get_all_categories',
    'search_icons',
    'get_icon_color',
    'get_icon_size',
    'create_icon_config',
    'get_haven_icon',
    'get_ui_pattern',
    'ICON_COLORS',
    'ICON_SIZES',
    'CONTEXTUAL_COLORS',
    'ALL_ICON_MAPPINGS',
    'HAVEN_SPECIFIC_ICONS',
    'HAVEN_UI_PATTERNS'
]

