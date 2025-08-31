# config/icon_mapping.py
# Icon mapping configuration for Haven Crowdfunding Platform

"""
Icon mapping configuration for Haven Crowdfunding Platform.
Maps UI elements to appropriate Bootstrap icons and provides color schemes.
"""

# Navigation Icons
NAVIGATION_ICONS = {
    'home': 'house-fill',
    'browse': 'search',
    'campaigns': 'grid-3x3-gap-fill',
    'create': 'plus-circle-fill',
    'profile': 'person-circle',
    'dashboard': 'speedometer2',
    'notifications': 'bell-fill',
    'messages': 'chat-dots-fill',
    'settings': 'gear-fill',
    'help': 'question-circle-fill',
    'logout': 'box-arrow-right'
}

# Campaign Category Icons
CATEGORY_ICONS = {
    'technology': 'cpu-fill',
    'environment': 'tree-fill',
    'education': 'book-fill',
    'health': 'heart-pulse-fill',
    'arts': 'palette-fill',
    'games': 'controller',
    'music': 'music-note-beamed',
    'film': 'camera-video-fill',
    'food': 'cup-hot-fill',
    'fashion': 'bag-fill',
    'sports': 'trophy-fill',
    'travel': 'airplane-fill',
    'community': 'people-fill',
    'business': 'briefcase-fill',
    'charity': 'heart-fill'
}

# Campaign Status Icons
STATUS_ICONS = {
    'active': 'play-circle-fill',
    'completed': 'check-circle-fill',
    'pending': 'clock-fill',
    'cancelled': 'x-circle-fill',
    'draft': 'file-earmark-text',
    'review': 'eye-fill',
    'funded': 'currency-dollar',
    'overfunded': 'graph-up-arrow'
}

# Financial Icons
FINANCIAL_ICONS = {
    'goal': 'bullseye',
    'raised': 'currency-dollar',
    'percentage': 'percent',
    'backers': 'people',
    'funding': 'cash-coin',
    'wallet': 'wallet2',
    'payment': 'credit-card',
    'bank': 'bank',
    'investment': 'graph-up',
    'profit': 'arrow-up-circle-fill',
    'loss': 'arrow-down-circle-fill'
}

# User Action Icons
ACTION_ICONS = {
    'like': 'heart',
    'liked': 'heart-fill',
    'share': 'share',
    'bookmark': 'bookmark',
    'bookmarked': 'bookmark-fill',
    'follow': 'person-plus',
    'following': 'person-check-fill',
    'comment': 'chat-left-text',
    'edit': 'pencil-square',
    'delete': 'trash',
    'view': 'eye',
    'download': 'download',
    'upload': 'upload',
    'save': 'floppy',
    'print': 'printer'
}

# Time and Date Icons
TIME_ICONS = {
    'calendar': 'calendar',
    'clock': 'clock',
    'deadline': 'alarm',
    'schedule': 'calendar-event',
    'history': 'clock-history',
    'timer': 'stopwatch',
    'duration': 'hourglass-split'
}

# Communication Icons
COMMUNICATION_ICONS = {
    'email': 'envelope',
    'phone': 'telephone',
    'message': 'chat-dots',
    'notification': 'bell',
    'announcement': 'megaphone',
    'feedback': 'chat-square-text',
    'support': 'headset',
    'faq': 'question-circle'
}

# Security and Authentication Icons
SECURITY_ICONS = {
    'login': 'box-arrow-in-right',
    'logout': 'box-arrow-right',
    'register': 'person-plus',
    'password': 'key',
    'security': 'shield-check',
    'verification': 'patch-check',
    'privacy': 'eye-slash',
    'lock': 'lock',
    'unlock': 'unlock'
}

# Media and Content Icons
MEDIA_ICONS = {
    'image': 'image',
    'video': 'play-circle',
    'audio': 'volume-up',
    'document': 'file-earmark-text',
    'pdf': 'file-earmark-pdf',
    'link': 'link-45deg',
    'attachment': 'paperclip',
    'gallery': 'images'
}

# System and Technical Icons
SYSTEM_ICONS = {
    'loading': 'arrow-clockwise',
    'refresh': 'arrow-repeat',
    'sync': 'arrow-left-right',
    'backup': 'cloud-upload',
    'restore': 'cloud-download',
    'error': 'exclamation-triangle',
    'warning': 'exclamation-circle',
    'info': 'info-circle',
    'success': 'check-circle'
}

# Location and Geography Icons
LOCATION_ICONS = {
    'location': 'geo-alt',
    'map': 'map',
    'globe': 'globe',
    'country': 'flag',
    'city': 'building',
    'address': 'house'
}

# Social Media Icons
SOCIAL_ICONS = {
    'facebook': 'facebook',
    'twitter': 'twitter',
    'instagram': 'instagram',
    'linkedin': 'linkedin',
    'youtube': 'youtube',
    'github': 'github',
    'discord': 'discord',
    'telegram': 'telegram'
}

# Campaign Progress Icons
PROGRESS_ICONS = {
    'milestone': 'flag',
    'achievement': 'award',
    'progress': 'bar-chart',
    'target': 'bullseye',
    'growth': 'trending-up',
    'decline': 'trending-down',
    'stable': 'dash'
}

# Quality and Rating Icons
QUALITY_ICONS = {
    'star': 'star',
    'star_filled': 'star-fill',
    'rating': 'star-half',
    'quality': 'gem',
    'premium': 'crown',
    'verified': 'patch-check-fill',
    'featured': 'lightning-charge-fill'
}

# Color schemes for different icon contexts
ICON_COLORS = {
    'primary': '#4CAF50',
    'secondary': '#2196F3',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'muted': '#6c757d'
}

# Size presets for different UI contexts
ICON_SIZES = {
    'xs': 12,
    'sm': 16,
    'md': 20,
    'lg': 24,
    'xl': 32,
    'xxl': 48
}

# Predefined icon sets for common UI patterns
UI_PATTERNS = {
    'campaign_card_actions': ['heart', 'share', 'bookmark', 'cash-coin'],
    'user_profile_actions': ['pencil-square', 'gear', 'bell', 'box-arrow-right'],
    'campaign_metrics': ['currency-dollar', 'people', 'calendar', 'percent'],
    'navigation_primary': ['house-fill', 'search', 'plus-circle-fill', 'person-circle'],
    'status_indicators': ['check-circle-fill', 'clock-fill', 'x-circle-fill', 'exclamation-triangle'],
    'social_actions': ['heart', 'chat-dots', 'share', 'bookmark'],
    'file_operations': ['upload', 'download', 'floppy', 'trash']
}

def get_icon(category: str, name: str) -> str:
    """
    Get icon name by category and specific name.
    
    Args:
        category (str): Icon category (e.g., 'navigation', 'action')
        name (str): Specific icon name within category
    
    Returns:
        str: Bootstrap icon name or default icon if not found
    
    Example:
        get_icon('navigation', 'home')  # Returns 'house-fill'
        get_icon('action', 'like')      # Returns 'heart'
    """
    icon_maps = {
        'navigation': NAVIGATION_ICONS,
        'category': CATEGORY_ICONS,
        'status': STATUS_ICONS,
        'financial': FINANCIAL_ICONS,
        'action': ACTION_ICONS,
        'time': TIME_ICONS,
        'communication': COMMUNICATION_ICONS,
        'security': SECURITY_ICONS,
        'media': MEDIA_ICONS,
        'system': SYSTEM_ICONS,
        'location': LOCATION_ICONS,
        'social': SOCIAL_ICONS,
        'progress': PROGRESS_ICONS,
        'quality': QUALITY_ICONS
    }
    
    icon_map = icon_maps.get(category, {})
    return icon_map.get(name, 'circle')  # Default to 'circle' if not found

def get_category_icon(category: str) -> str:
    """
    Get icon for a campaign category.
    
    Args:
        category (str): Category name
    
    Returns:
        str: Icon name for the category
    """
    return CATEGORY_ICONS.get(category.lower(), 'tag-fill')

def get_status_icon(status: str) -> str:
    """
    Get icon for a campaign status.
    
    Args:
        status (str): Status name
    
    Returns:
        str: Icon name for the status
    """
    return STATUS_ICONS.get(status.lower(), 'circle')

def get_action_icon(action: str) -> str:
    """
    Get icon for a user action.
    
    Args:
        action (str): Action name
    
    Returns:
        str: Icon name for the action
    """
    return ACTION_ICONS.get(action.lower(), 'circle')

def get_ui_pattern_icons(pattern: str) -> list:
    """
    Get list of icons for a UI pattern.
    
    Args:
        pattern (str): UI pattern name
    
    Returns:
        list: List of icon names for the pattern
    """
    return UI_PATTERNS.get(pattern, [])

def get_color_for_context(context: str) -> str:
    """
    Get color for a specific context.
    
    Args:
        context (str): Context name (primary, success, warning, etc.)
    
    Returns:
        str: Hex color code
    """
    return ICON_COLORS.get(context, ICON_COLORS['muted'])

def get_size_for_context(context: str) -> int:
    """
    Get size for a specific context.
    
    Args:
        context (str): Context name (xs, sm, md, lg, xl, xxl)
    
    Returns:
        int: Size in pixels
    """
    return ICON_SIZES.get(context, ICON_SIZES['md'])

# Haven-specific icon mappings
HAVEN_SPECIFIC = {
    'platform_logo': 'house-heart-fill',
    'campaign_success': 'trophy-fill',
    'funding_goal': 'bullseye',
    'backer_count': 'people-fill',
    'time_remaining': 'clock',
    'amount_raised': 'currency-dollar',
    'project_update': 'megaphone-fill',
    'creator_profile': 'person-badge',
    'reward_tier': 'gift-fill',
    'payment_secure': 'shield-lock-fill'
}

