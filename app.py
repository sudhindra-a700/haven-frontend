# Haven Crowdfunding Platform - Complete Integration
# Complete app.py with Bootstrap icon navigation using existing utility files

import streamlit as st
import base64
import os
import sys

# Add utils to path for imports
sys.path.append('utils')
sys.path.append('config')

# Import existing utility files
try:
    from utils.icon_utils import display_icon, get_icon_html, icon_button, verify_icon_exists
    from config.icon_mapping import get_icon, ICON_COLORS, ICON_SIZES, get_icon_by_category
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    print("Warning: Could not import icon utilities. Using fallback methods.")

# ================================
# ENHANCED ICON UTILITY FUNCTIONS
# ================================

def get_bootstrap_icon_b64(icon_name, size=18, color="#ffffff"):
    """
    Convert Bootstrap SVG icon to base64 for reliable display.
    Integrates with existing icon_utils.py functionality.
    """
    # Try to use existing utility first
    if UTILS_AVAILABLE and verify_icon_exists(icon_name):
        svg_path = f"assets/{icon_name}.svg"
    else:
        svg_path = f"assets/{icon_name}.svg"
    
    if os.path.exists(svg_path):
        try:
            with open(svg_path, "rb") as f:
                svg_data = f.read()
            
            # Convert to base64
            b64_svg = base64.b64encode(svg_data).decode()
            
            # Return as data URL with styling
            return f'''<img src="data:image/svg+xml;base64,{b64_svg}" 
                       width="{size}" height="{size}" 
                       style="vertical-align: middle; margin-right: 10px; 
                              filter: brightness(0) saturate(100%) invert(100%);">'''
        except Exception as e:
            print(f"Error loading icon {icon_name}: {e}")
            return f'<span style="margin-right: 10px; color: white;">●</span>'
    
    # Fallback if icon doesn't exist
    return f'<span style="margin-right: 10px; color: white;">●</span>'

def get_colored_icon_b64(icon_name, size=24, color="#4CAF50"):
    """Get colored Bootstrap icon using existing utilities."""
    
    # Try to use existing icon mapping
    if UTILS_AVAILABLE:
        try:
            # Use icon mapping if available
            mapped_icon = get_icon('ui', icon_name) if hasattr(get_icon, '__call__') else icon_name
            icon_name = mapped_icon or icon_name
        except:
            pass
    
    svg_path = f"assets/{icon_name}.svg"
    
    if os.path.exists(svg_path):
        try:
            with open(svg_path, "rb") as f:
                svg_data = f.read()
            
            b64_svg = base64.b64encode(svg_data).decode()
            
            # Color filter mapping
            color_filters = {
                "#4CAF50": "invert(27%) sepia(51%) saturate(2878%) hue-rotate(346deg) brightness(104%) contrast(97%)",
                "#2196F3": "invert(27%) sepia(98%) saturate(1000%) hue-rotate(196deg) brightness(104%) contrast(97%)",
                "#FF9800": "invert(27%) sepia(98%) saturate(1000%) hue-rotate(25deg) brightness(104%) contrast(97%)",
                "#9C27B0": "invert(27%) sepia(98%) saturate(1000%) hue-rotate(280deg) brightness(104%) contrast(97%)",
                "#FF5722": "invert(27%) sepia(98%) saturate(1000%) hue-rotate(15deg) brightness(104%) contrast(97%)"
            }
            
            filter_css = color_filters.get(color, "")
            
            return f'''<img src="data:image/svg+xml;base64,{b64_svg}" 
                       width="{size}" height="{size}" 
                       style="vertical-align: middle; filter: {filter_css};">'''
        except Exception as e:
            return f'<span style="color: {color};">●</span>'
    
    return f'<span style="color: {color};">●</span>'

def enhanced_icon_button(icon_name, label, key, help_text=None, use_existing_utils=True):
    """Enhanced icon button that uses existing utilities when available."""
    
    if UTILS_AVAILABLE and use_existing_utils:
        try:
            # Use existing icon_button function
            return icon_button(icon_name, label, key)
        except:
            pass
    
    # Fallback to custom implementation
    col1, col2 = st.columns([1, 4])
    with col1:
        icon_html = get_bootstrap_icon_b64(icon_name, 18)
        st.markdown(icon_html, unsafe_allow_html=True)
    with col2:
        return st.button(label, key=key, help=help_text)

def get_navigation_icons():
    """Get navigation icons using existing icon mapping if available."""
    
    if UTILS_AVAILABLE:
        try:
            # Use existing icon mapping
            return {
                'home': get_icon('navigation', 'home') or 'house-fill',
                'search': get_icon('navigation', 'search') or 'search',
                'create': get_icon('actions', 'create') or 'plus-circle-fill',
                'dashboard': get_icon('navigation', 'dashboard') or 'speedometer2',
                'profile': get_icon('navigation', 'profile') or 'person-circle',
                'login': get_icon('authentication', 'login') or 'box-arrow-in-right',
                'register': get_icon('authentication', 'register') or 'person-plus-fill',
                'help': get_icon('navigation', 'help') or 'question-circle-fill'
            }
        except:
            pass
    
    # Fallback icon mapping
    return {
        'home': 'house-fill',
        'search': 'search',
        'create': 'plus-circle-fill',
        'dashboard': 'speedometer2',
        'profile': 'person-circle',
        'login': 'box-arrow-in-right',
        'register': 'person-plus-fill',
        'help': 'question-circle-fill'
    }

def get_ui_colors():
    """Get UI colors using existing color mapping if available."""
    
    if UTILS_AVAILABLE:
        try:
            return {
                'primary': ICON_COLORS.get('primary', '#4CAF50'),
                'secondary': ICON_COLORS.get('secondary', '#2196F3'),
                'success': ICON_COLORS.get('success', '#4CAF50'),
                'warning': ICON_COLORS.get('warning', '#FF9800'),
                'danger': ICON_COLORS.get('danger', '#F44336'),
                'info': ICON_COLORS.get('info', '#2196F3')
            }
        except:
            pass
    
    # Fallback colors
    return {
        'primary': '#4CAF50',
        'secondary': '#2196F3',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'danger': '#F44336',
        'info': '#2196F3'
    }

# ================================
# NAVIGATION COMPONENTS
# ================================

def render_professional_sidebar():
    """Render professional sidebar navigation using existing utilities."""
    
    # Get colors and icons from existing utilities
    colors = get_ui_colors()
    nav_icons = get_navigation_icons()
    
    # Professional CSS styling
    st.markdown(f"""
    <style>
    .nav-section {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }}
    
    .nav-title {{
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
        color: white;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 15px;
    }}
    
    .nav-item {{
        display: flex;
        align-items: center;
        padding: 12px 15px;
        margin: 8px 0;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-size: 14px;
        font-weight: 500;
    }}
    
    .nav-item:hover {{
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }}
    
    .nav-item.active {{
        background: rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }}
    
    .stats-section {{
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }}
    
    .stat-item {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #dee2e6;
        font-size: 14px;
    }}
    
    .stat-item:last-child {{
        border-bottom: none;
    }}
    
    .stat-value {{
        font-weight: bold;
        color: {colors['primary']};
        font-size: 16px;
    }}
    
    .stButton > button {{
        width: 100%;
        border-radius: 8px;
        border: none;
        background: transparent;
        color: inherit;
        padding: 0;
        margin: 0;
        height: auto;
    }}
    
    .stButton > button:hover {{
        background: transparent;
        border: none;
        box-shadow: none;
    }}
    
    .stButton > button:focus {{
        background: transparent;
        border: none;
        box-shadow: none;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation items using existing icon mapping
    nav_items = [
        (nav_icons['home'], "Home", "home"),
        (nav_icons['search'], "Browse Campaigns", "browse"),
        (nav_icons['create'], "Create Campaign", "create"),
        (nav_icons['dashboard'], "Dashboard", "dashboard"),
        (nav_icons['profile'], "Profile", "profile"),
        (nav_icons['login'], "Login", "login"),
        (nav_icons['register'], "Register", "register"),
        (nav_icons['help'], "Help", "help")
    ]
    
    # Initialize current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Render navigation section
    st.sidebar.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="nav-title">🏠 Haven Platform</div>', unsafe_allow_html=True)
    
    for icon_name, label, page_key in nav_items:
        # Get Bootstrap icon as base64
        icon_html = get_bootstrap_icon_b64(icon_name, 18)
        
        # Check if this is the current page
        is_active = st.session_state.current_page == page_key
        active_class = "active" if is_active else ""
        
        # Create navigation item HTML
        nav_item_html = f'''
        <div class="nav-item {active_class}">
            {icon_html}
            <span style="flex: 1;">{label}</span>
            {"🔹" if is_active else ""}
        </div>
        '''
        
        # Display the styled navigation item
        st.sidebar.markdown(nav_item_html, unsafe_allow_html=True)
        
        # Use enhanced icon button
        if enhanced_icon_button(icon_name, f"→ {label}", f"nav_{page_key}", f"Navigate to {label}", False):
            st.session_state.current_page = page_key
            st.rerun()
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # User info section
    render_user_stats_section()

def render_user_stats_section():
    """Render user statistics section using existing utilities."""
    
    colors = get_ui_colors()
    
    st.sidebar.markdown('<div class="stats-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 👤 Welcome, John Doe")
    
    # User stats with Bootstrap icons - try to use existing mapping
    if UTILS_AVAILABLE:
        try:
            stats_items = [
                (get_icon('financial', 'campaign') or 'rocket-takeoff', "Campaigns Created", "3"),
                (get_icon('actions', 'bookmark') or 'bookmark-star', "Campaigns Backed", "12"),
                (get_icon('financial', 'money') or 'currency-dollar', "Total Contributed", "$2,450")
            ]
        except:
            stats_items = [
                ('rocket-takeoff', "Campaigns Created", "3"),
                ('bookmark-star', "Campaigns Backed", "12"),
                ('currency-dollar', "Total Contributed", "$2,450")
            ]
    else:
        stats_items = [
            ('rocket-takeoff', "Campaigns Created", "3"),
            ('bookmark-star', "Campaigns Backed", "12"),
            ('currency-dollar', "Total Contributed", "$2,450")
        ]
    
    for icon_name, label, value in stats_items:
        icon_html = get_colored_icon_b64(icon_name, 16, colors['primary'])
        
        stat_html = f'''
        <div class="stat-item">
            <span>{icon_html} {label}</span>
            <span class="stat-value">{value}</span>
        </div>
        '''
        st.sidebar.markdown(stat_html, unsafe_allow_html=True)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ================================
# MAIN CONTENT COMPONENTS
# ================================

def render_main_header():
    """Render main header with professional styling using existing utilities."""
    
    colors = get_ui_colors()
    nav_icons = get_navigation_icons()
    
    # Header styling
    st.markdown(f"""
    <style>
    .main-header {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['success']} 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);
    }}
    
    .header-title {{
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    .header-subtitle {{
        font-size: 18px;
        opacity: 0.9;
        margin-bottom: 20px;
    }}
    
    .status-indicators {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 15px;
    }}
    
    .status-item {{
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    header_html = f'''
    <div class="main-header">
        <div class="header-title">
            {get_bootstrap_icon_b64(nav_icons['home'], 36)} Haven Crowdfunding Platform
        </div>
        <div class="header-subtitle">Your gateway to innovative crowdfunding projects</div>
        <div class="status-indicators">
            <div class="status-item">
                {get_bootstrap_icon_b64('wifi', 16)} Online
            </div>
            <div class="status-item">
                {get_bootstrap_icon_b64('patch-check-fill', 16)} Verified
            </div>
        </div>
    </div>
    '''
    
    st.markdown(header_html, unsafe_allow_html=True)

def render_home_content():
    """Render home page content using existing utilities."""
    
    colors = get_ui_colors()
    
    # Welcome section
    welcome_html = f'''
    <div style="text-align: center; margin: 40px 0;">
        <h2 style="color: #333; font-size: 28px; margin-bottom: 15px;">
            {get_colored_icon_b64("star-fill", 32, colors['warning'])} Welcome to Haven
        </h2>
        <p style="font-size: 18px; color: #666; max-width: 600px; margin: 0 auto;">
            Your gateway to innovative crowdfunding projects. Connect with creators, support amazing ideas, and bring innovations to life.
        </p>
    </div>
    '''
    st.markdown(welcome_html, unsafe_allow_html=True)
    
    # Platform metrics with Bootstrap icons using existing utilities
    st.markdown("### 📊 Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Try to use existing icon mapping
    if UTILS_AVAILABLE:
        try:
            metrics = [
                (get_icon('financial', 'money') or 'currency-dollar', "Total Raised", "$2.5M", colors['primary']),
                (get_icon('social', 'users') or 'people-fill', "Active Users", "15,432", colors['secondary']),
                (get_icon('status', 'success') or 'trophy-fill', "Successful Projects", "1,247", colors['warning']),
                (get_icon('status', 'active') or 'lightning-charge-fill', "Active Campaigns", "89", '#9C27B0')
            ]
        except:
            metrics = [
                ('currency-dollar', "Total Raised", "$2.5M", colors['primary']),
                ('people-fill', "Active Users", "15,432", colors['secondary']),
                ('trophy-fill', "Successful Projects", "1,247", colors['warning']),
                ('lightning-charge-fill', "Active Campaigns", "89", '#9C27B0')
            ]
    else:
        metrics = [
            ('currency-dollar', "Total Raised", "$2.5M", colors['primary']),
            ('people-fill', "Active Users", "15,432", colors['secondary']),
            ('trophy-fill', "Successful Projects", "1,247", colors['warning']),
            ('lightning-charge-fill', "Active Campaigns", "89", '#9C27B0')
        ]
    
    for i, (icon, label, value, color) in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            metric_html = f'''
            <div style="background: white; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 8px 25px rgba(0,0,0,0.1); text-align: center; 
                        border-left: 5px solid {color}; margin-bottom: 20px;
                        transition: transform 0.3s ease;">
                <div style="font-size: 28px; margin-bottom: 15px;">
                    {get_colored_icon_b64(icon, 40, color)}
                </div>
                <div style="font-size: 28px; font-weight: bold; color: {color}; margin-bottom: 8px;">
                    {value}
                </div>
                <div style="color: #666; font-size: 14px; font-weight: 500;">
                    {label}
                </div>
            </div>
            '''
            st.markdown(metric_html, unsafe_allow_html=True)
    
    # Action section
    st.markdown("---")
    
    action_header_html = f'''
    <div style="text-align: center; margin: 40px 0;">
        <h3 style="color: #333; font-size: 24px;">
            {get_colored_icon_b64("fire", 28, "#FF5722")} What You Can Do
        </h3>
    </div>
    '''
    st.markdown(action_header_html, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    nav_icons = get_navigation_icons()
    
    actions = [
        (nav_icons['search'], "Discover Projects", "Browse thousands of innovative campaigns from creators worldwide", "browse", colors['secondary']),
        (nav_icons['create'], "Start a Campaign", "Bring your ideas to life and get funding from supporters", "create", colors['primary']),
        ('people-fill', "Join Community", "Connect with creators and support projects you believe in", "register", colors['warning'])
    ]
    
    for i, (icon, title, desc, page, color) in enumerate(actions):
        with [col1, col2, col3][i]:
            action_html = f'''
            <div style="background: white; padding: 30px; border-radius: 15px; 
                        box-shadow: 0 8px 25px rgba(0,0,0,0.1); text-align: center; 
                        margin-bottom: 20px; transition: transform 0.3s ease;
                        border-top: 4px solid {color};">
                <div style="font-size: 48px; margin-bottom: 20px;">
                    {get_colored_icon_b64(icon, 56, color)}
                </div>
                <h4 style="margin-bottom: 15px; color: #333; font-size: 20px;">{title}</h4>
                <p style="color: #666; margin-bottom: 25px; line-height: 1.6;">{desc}</p>
            </div>
            '''
            st.markdown(action_html, unsafe_allow_html=True)
            
            if st.button(f"🚀 {title}", key=f"action_{page}", help=f"Navigate to {title}"):
                st.session_state.current_page = page
                st.rerun()

# ================================
# OTHER PAGE CONTENT (Simplified for brevity)
# ================================

def render_browse_content():
    """Render browse campaigns page."""
    colors = get_ui_colors()
    st.markdown(f"## {get_colored_icon_b64('search', 32, colors['secondary'])} Browse Campaigns")
    st.markdown("Discover amazing projects to support")
    
    # Sample campaigns with existing utility integration
    col1, col2, col3 = st.columns(3)
    
    campaigns = [
        ("Smart Home Device", "$45,000", "85%", "12 days left"),
        ("Eco-Friendly Packaging", "$23,500", "67%", "8 days left"),
        ("Mobile App Innovation", "$78,900", "92%", "5 days left")
    ]
    
    for i, (title, raised, progress, time_left) in enumerate(campaigns):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            **{title}**
            
            💰 Raised: {raised}
            📊 Progress: {progress}
            ⏰ {time_left}
            """)
            if st.button(f"View {title}", key=f"campaign_{i}"):
                st.success(f"Viewing {title} campaign details!")

def render_create_content():
    """Render create campaign page."""
    colors = get_ui_colors()
    st.markdown(f"## {get_colored_icon_b64('plus-circle-fill', 32, colors['primary'])} Create Campaign")
    st.markdown("Launch your innovative project")
    
    with st.form("create_campaign"):
        st.text_input("Campaign Title")
        st.text_area("Campaign Description")
        st.number_input("Funding Goal ($)", min_value=1000, value=10000)
        st.number_input("Campaign Duration (days)", min_value=1, max_value=90, value=30)
        
        if st.form_submit_button("🚀 Launch Campaign"):
            st.success("Campaign created successfully!")

def render_dashboard_content():
    """Render user dashboard."""
    colors = get_ui_colors()
    st.markdown(f"## {get_colored_icon_b64('speedometer2', 32, '#9C27B0')} Dashboard")
    st.markdown("Manage your campaigns and contributions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### My Campaigns")
        st.markdown("📊 Active: 2")
        st.markdown("✅ Successful: 1")
        st.markdown("💰 Total Raised: $15,600")
    
    with col2:
        st.markdown("### My Contributions")
        st.markdown("❤️ Backed: 12 projects")
        st.markdown("💵 Total Contributed: $2,450")
        st.markdown("🏆 Success Rate: 83%")

def render_profile_content():
    """Render user profile page."""
    colors = get_ui_colors()
    st.markdown(f"## {get_colored_icon_b64('person-circle', 32, colors['warning'])} User Profile")
    st.markdown("Manage your account settings")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("First Name", value="John")
            st.text_input("Last Name", value="Doe")
            st.text_input("Email", value="john.doe@example.com")
        
        with col2:
            st.text_input("Phone")
            st.selectbox("Country", ["United States", "Canada", "United Kingdom"])
            st.text_area("Bio")
        
        if st.form_submit_button("💾 Save Changes"):
            st.success("Profile updated successfully!")

def render_login_content():
    """Render login page."""
    colors = get_ui_colors()
    nav_icons = get_navigation_icons()
    st.markdown(f"## {get_colored_icon_b64(nav_icons['login'], 32, colors['primary'])} Login")
    st.markdown("Sign in to your Haven account")
    
    with st.form("login_form"):
        st.text_input("Email")
        st.text_input("Password", type="password")
        st.checkbox("Remember me")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("🔐 Sign In"):
                st.success("Logged in successfully!")
        with col2:
            if st.form_submit_button("📝 Create Account"):
                st.session_state.current_page = 'register'
                st.rerun()

def render_register_content():
    """Render registration page."""
    colors = get_ui_colors()
    nav_icons = get_navigation_icons()
    st.markdown(f"## {get_colored_icon_b64(nav_icons['register'], 32, colors['secondary'])} Register")
    st.markdown("Create your Haven account")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("First Name")
            st.text_input("Last Name")
            st.text_input("Email")
        
        with col2:
            st.text_input("Password", type="password")
            st.text_input("Confirm Password", type="password")
            st.checkbox("I agree to the Terms of Service")
        
        if st.form_submit_button("🎉 Create Account"):
            st.success("Account created successfully!")

def render_help_content():
    """Render help page."""
    colors = get_ui_colors()
    nav_icons = get_navigation_icons()
    st.markdown(f"## {get_colored_icon_b64(nav_icons['help'], 32, '#FF5722')} Help & Support")
    st.markdown("Get help with Haven platform")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 Frequently Asked Questions")
        with st.expander("How do I create a campaign?"):
            st.markdown("Click on 'Create Campaign' in the navigation and fill out the form with your project details.")
        
        with st.expander("How do I back a project?"):
            st.markdown("Browse campaigns, select one you like, and choose a reward tier to support the creator.")
        
        with st.expander("What payment methods are accepted?"):
            st.markdown("We accept credit cards, PayPal, and bank transfers for contributions.")
    
    with col2:
        st.markdown("### 📞 Contact Support")
        st.markdown("📧 Email: support@haven.com")
        st.markdown("📱 Phone: 1-800-HAVEN-01")
        st.markdown("💬 Live Chat: Available 24/7")
        
        if st.button("💬 Start Live Chat"):
            st.info("Live chat feature coming soon!")

# ================================
# PAGE ROUTING
# ================================

def render_page_content():
    """Render content based on current page."""
    
    current_page = st.session_state.get('current_page', 'home')
    
    if current_page == 'home':
        render_home_content()
    elif current_page == 'browse':
        render_browse_content()
    elif current_page == 'create':
        render_create_content()
    elif current_page == 'dashboard':
        render_dashboard_content()
    elif current_page == 'profile':
        render_profile_content()
    elif current_page == 'login':
        render_login_content()
    elif current_page == 'register':
        render_register_content()
    elif current_page == 'help':
        render_help_content()
    else:
        render_home_content()

# ================================
# MAIN APPLICATION
# ================================

def main():
    """Main application integrating with existing utility files."""
    
    # Page configuration
    st.set_page_config(
        page_title="Haven - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Display utility status
    if UTILS_AVAILABLE:
        st.sidebar.success("✅ Icon utilities loaded")
    else:
        st.sidebar.warning("⚠️ Using fallback icon system")
    
    # Get colors from existing utilities
    colors = get_ui_colors()
    
    # Global CSS styling
    st.markdown(f"""
    <style>
    /* Hide default Streamlit elements */
    .stApp > header {{
        display: none;
    }}
    
    .stDeployButton {{
        display: none;
    }}
    
    #MainMenu {{
        visibility: hidden;
    }}
    
    footer {{
        visibility: hidden;
    }}
    
    /* Global styling */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #f1f1f1;
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['primary']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['success']};
    }}
    
    /* Improve button styling */
    .stButton > button {{
        transition: all 0.3s ease;
        border-radius: 8px;
        font-weight: 500;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }}
    
    /* Form styling */
    .stTextInput > div > div > input {{
        border-radius: 8px;
    }}
    
    .stTextArea > div > div > textarea {{
        border-radius: 8px;
    }}
    
    .stSelectbox > div > div > select {{
        border-radius: 8px;
    }}
    
    /* Metric styling */
    .metric-container {{
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Render professional navigation
    render_professional_sidebar()
    
    # Render main header
    render_main_header()
    
    # Render page content based on navigation
    render_page_content()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>© 2024 Haven Crowdfunding Platform. All rights reserved.</p>
        <p style="color: {colors['primary']};">🌟 Empowering innovation, one project at a time.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

