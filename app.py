import streamlit as st
import requests
import json
import os
from datetime import datetime

# Import Tabler Icons
try:
    from pytablericons import TablerIcon
    TABLER_AVAILABLE = True
except ImportError:
    TABLER_AVAILABLE = False
    st.warning("⚠️ pytablericons not installed. Install with: pip install pytablericons")

# ===== DYNAMIC THEMING SYSTEM =====
class ThemeManager:
    """Manage dynamic theming for icons based on background"""
    
    @staticmethod
    def get_icon_color(context="light"):
        """Get appropriate icon color based on background context"""
        if context == "dark":
            return "#FFFFFF"  # White icons on dark background
        else:
            return "#000000"  # Black icons on light background
    
    @staticmethod
    def get_primary_color():
        """Get primary theme color"""
        return "#4CAF50"
    
    @staticmethod
    def get_secondary_color():
        """Get secondary theme color"""
        return "#2196F3"

# ===== TABLER ICONS MANAGER =====
class TablerIconManager:
    """Manage Tabler Icons with dynamic theming and caching"""
    
    def __init__(self):
        self.icon_cache = {}
    
    def get_icon(self, icon_name, size=24, color=None, context="light", stroke_width=2):
        """Get Tabler icon with dynamic theming"""
        if not TABLER_AVAILABLE:
            return self._get_fallback_icon(icon_name)
        
        if color is None:
            color = ThemeManager.get_icon_color(context)
        
        # Create cache key
        cache_key = f"{icon_name}_{size}_{color}_{stroke_width}"
        
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
        
        try:
            # Get Tabler icon
            icon = TablerIcon(
                name=icon_name,
                size=size,
                color=color,
                stroke_width=stroke_width
            )
            
            # Cache the result
            self.icon_cache[cache_key] = icon.svg
            return icon.svg
            
        except Exception as e:
            st.error(f"Error loading icon {icon_name}: {e}")
            return self._get_fallback_icon(icon_name)
    
    def _get_fallback_icon(self, icon_name):
        """Fallback emoji icons if Tabler Icons not available"""
        fallbacks = {
            "folder-search": "📁",
            "language-off": "✈️",
            "language": "🌐",
            "brand-google": "🇬",
            "brand-facebook": "🇫",
            "info-small": "ℹ️",
            "circle-plus": "➕",
            "search": "🔍",
            "trending-up": "📈",
            "rupee": "₹",
            "user": "👤",
            "logout": "🚪",
            "home": "🏠"
        }
        return fallbacks.get(icon_name, "❓")
    
    def render_icon(self, icon_name, size=24, color=None, context="light", stroke_width=2):
        """Render Tabler icon in Streamlit"""
        if TABLER_AVAILABLE:
            svg_code = self.get_icon(icon_name, size, color, context, stroke_width)
            st.markdown(svg_code, unsafe_allow_html=True)
        else:
            fallback = self._get_fallback_icon(icon_name)
            st.markdown(f'<span style="font-size: {size}px;">{fallback}</span>', unsafe_allow_html=True)
    
    def get_icon_html(self, icon_name, size=24, color=None, context="light", stroke_width=2):
        """Get Tabler icon as HTML for inline use"""
        if TABLER_AVAILABLE:
            return self.get_icon(icon_name, size, color, context, stroke_width)
        else:
            fallback = self._get_fallback_icon(icon_name)
            return f'<span style="font-size: {size}px;">{fallback}</span>'

# ===== HAVEN ICONS DEFINITIONS =====
class HavenIcons:
    """Centralized icon definitions for HAVEN app using Tabler Icons"""
    
    # Navigation icons
    HOME = "home"
    EXPLORE = "folder-search"
    SEARCH = "search"
    TRENDING = "trending-up"
    CAMPAIGN = "circle-plus"
    PROFILE = "user"
    LOGOUT = "logout"
    
    # Translation icons
    LANGUAGE_OFF = "language-off"
    LANGUAGE_ON = "language"
    
    # Social login icons
    GOOGLE = "brand-google"
    FACEBOOK = "brand-facebook"
    
    # Action icons
    INFO = "info-small"
    RUPEE = "rupee"
    
    # Profile states
    USER_OUTLINED = "user"
    USER_FILLED = "user-filled"

# ===== PROFILE COMPLETION CHECKER =====
class ProfileManager:
    """Manage profile completion status for dynamic icon selection"""
    
    @staticmethod
    def check_profile_completion(user_data):
        """Check if user profile is complete"""
        if not user_data:
            return False
        
        required_fields = ['name', 'email', 'account_type']
        optional_fields = ['phone', 'address', 'bio', 'organization_type']
        
        # Check required fields
        for field in required_fields:
            if not user_data.get(field):
                return False
        
        # Check if at least some optional fields are filled
        optional_filled = sum(1 for field in optional_fields if user_data.get(field))
        
        # Profile is complete if all required + at least 2 optional fields are filled
        return optional_filled >= 2
    
    @staticmethod
    def get_profile_icon_name(user_data):
        """Get appropriate profile icon name based on completion status"""
        is_complete = ProfileManager.check_profile_completion(user_data)
        return "user-filled" if is_complete else "user"

# ===== CONFIGURATION =====
class Config:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID", "")
    TRANSLATION_ENABLED = os.getenv("TRANSLATION_ENABLED", "true").lower() == "true"
    OAUTH_ENABLED = os.getenv("OAUTH_ENABLED", "true").lower() == "true"

# ===== TRANSLATION SYSTEM =====
class TranslationManager:
    """Manage translation state and language selection"""
    
    LANGUAGES = {
        "en": "English",
        "hi": "हिंदी",
        "es": "Español", 
        "fr": "Français"
    }
    
    @staticmethod
    def get_current_language():
        return st.session_state.get('language', 'en')
    
    @staticmethod
    def set_language(lang_code):
        st.session_state.language = lang_code
    
    @staticmethod
    def is_translation_enabled():
        return st.session_state.get('translation_enabled', False)
    
    @staticmethod
    def toggle_translation():
        current = st.session_state.get('translation_enabled', False)
        st.session_state.translation_enabled = not current
        return not current
    
    @staticmethod
    def render_translation_toggle(icon_manager):
        """Render translation toggle with Tabler Icons"""
        col1, col2 = st.columns([1, 10])
        
        with col1:
            is_enabled = TranslationManager.is_translation_enabled()
            icon_name = HavenIcons.LANGUAGE_ON if is_enabled else HavenIcons.LANGUAGE_OFF
            color = ThemeManager.get_primary_color() if is_enabled else ThemeManager.get_icon_color("dark")
            
            # Create clickable translation toggle
            if st.button("", key="translation_toggle", help="Toggle Translation"):
                TranslationManager.toggle_translation()
                st.rerun()
            
            # Display icon with dark context (sidebar has dark background)
            st.markdown(f'<div style="margin-top: -40px; pointer-events: none;">{icon_manager.get_icon_html(icon_name, 24, color, "dark")}</div>', unsafe_allow_html=True)
        
        with col2:
            if TranslationManager.is_translation_enabled():
                # Show language dropdown
                current_lang = TranslationManager.get_current_language()
                selected_lang = st.selectbox(
                    "Language",
                    options=list(TranslationManager.LANGUAGES.keys()),
                    format_func=lambda x: TranslationManager.LANGUAGES[x],
                    index=list(TranslationManager.LANGUAGES.keys()).index(current_lang),
                    key="language_selector"
                )
                
                if selected_lang != current_lang:
                    TranslationManager.set_language(selected_lang)
                    st.rerun()

# ===== STYLING =====
def load_custom_css():
    """Load custom CSS for HAVEN with dynamic theming"""
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #4CAF50;
        --primary-light: #81C784;
        --primary-dark: #388E3C;
        --secondary-color: #2196F3;
        --background-light: #F1F8E9;
        --text-dark: #2E7D32;
        --border-color: #C8E6C9;
        --dark-bg: #2C3E50;
        --icon-light: #000000;
        --icon-dark: #FFFFFF;
    }
    
    /* Main container styling */
    .main-container {
        background: linear-gradient(135deg, #F1F8E9 0%, #E8F5E8 100%);
        min-height: 100vh;
        padding: 20px;
    }
    
    /* Header styling */
    .app-header {
        background: var(--primary-color);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Card styling */
    .info-card {
        background: white;
        border: 2px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Dark themed elements */
    .dark-element {
        background: var(--dark-bg);
        color: var(--icon-dark);
    }
    
    /* Light themed elements */
    .light-element {
        background: white;
        color: var(--icon-light);
    }
    
    /* Icon button styling */
    .icon-button {
        background: var(--dark-bg);
        border: 2px solid #34495E;
        border-radius: 8px;
        padding: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 4px;
        min-width: 48px;
        min-height: 48px;
    }
    
    .icon-button:hover {
        background: #34495E;
        border-color: var(--primary-color);
        transform: translateY(-1px);
    }
    
    /* Social login buttons */
    .social-login-container {
        display: flex;
        justify-content: center;
        gap: 16px;
        margin: 20px 0;
    }
    
    .social-icon {
        background: var(--dark-bg);
        border: 2px solid #34495E;
        border-radius: 8px;
        padding: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 56px;
        height: 56px;
    }
    
    .social-icon:hover {
        background: #34495E;
        border-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Info tooltip styling */
    .info-tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .info-tooltip .tooltip-text {
        visibility: hidden;
        width: 200px;
        background-color: var(--dark-bg);
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
    }
    
    .info-tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    
    /* Navigation styling */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 5px 0;
        transition: all 0.3s ease;
        cursor: pointer;
        background: white;
        border: 1px solid var(--border-color);
    }
    
    .nav-item:hover {
        background: var(--background-light);
        border-color: var(--primary-color);
    }
    
    /* Form styling */
    .form-container {
        background: white;
        padding: 30px;
        border-radius: 12px;
        border: 2px solid var(--border-color);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Translation toggle styling */
    .translation-container {
        background: var(--dark-bg);
        border: 2px solid #34495E;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Upload area styling */
    .upload-area {
        border: 2px dashed var(--border-color);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        background: #FAFAFA;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: var(--primary-color);
        background: var(--background-light);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide sidebar for unauthenticated users */
    .css-1d391kg {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    .css-1lcbmhc {margin-left: 0 !important;}
    
    /* Show sidebar only when authenticated */
    .authenticated section[data-testid="stSidebar"] {display: block !important;}
    .authenticated .css-1d391kg {display: block !important;}
    .authenticated .css-1lcbmhc {margin-left: 21rem !important;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-container {
            padding: 10px;
        }
        
        .form-container {
            padding: 20px;
        }
        
        .social-login-container {
            flex-direction: column;
            align-items: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ===== AUTHENTICATION FUNCTIONS =====
def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def login_user(username, user_data=None):
    """Login user and set session state"""
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.user_data = user_data or {}
    st.session_state.login_time = datetime.now()

def logout_user():
    """Logout user and clear session state"""
    for key in ['authenticated', 'username', 'user_data', 'login_time']:
        if key in st.session_state:
            del st.session_state[key]

# ===== HELPER FUNCTIONS =====
def render_info_tooltip(text, tooltip_text, icon_manager):
    """Render text with info-small icon tooltip using Tabler Icons"""
    info_icon = icon_manager.get_icon_html(HavenIcons.INFO, 16, ThemeManager.get_icon_color("light"), "light")
    return f'''
    <span class="info-tooltip">
        {text} {info_icon}
        <span class="tooltip-text">{tooltip_text}</span>
    </span>
    '''

def render_social_login_buttons(icon_manager):
    """Render social login buttons with Tabler brand icons"""
    st.markdown("### Or sign in with")
    
    google_icon = icon_manager.get_icon_html(HavenIcons.GOOGLE, 32, None, "dark")
    facebook_icon = icon_manager.get_icon_html(HavenIcons.FACEBOOK, 32, None, "dark")
    
    st.markdown(f'''
    <div class="social-login-container">
        <div class="social-icon" onclick="alert('Google OAuth integration required')" title="Sign in with Google">
            {google_icon}
        </div>
        <div class="social-icon" onclick="alert('Facebook OAuth integration required')" title="Sign in with Facebook">
            {facebook_icon}
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ===== NAVIGATION FUNCTIONS =====
def render_navigation(icon_manager):
    """Render navigation sidebar with Tabler Icons"""
    if not check_authentication():
        return
    
    st.sidebar.markdown("### Navigation")
    
    # Translation toggle in sidebar (dark context)
    with st.sidebar:
        st.markdown("#### Translation")
        TranslationManager.render_translation_toggle(icon_manager)
    
    st.sidebar.markdown("---")
    
    # Get user data for profile icon
    user_data = st.session_state.get('user_data', {})
    profile_icon_name = ProfileManager.get_profile_icon_name(user_data)
    
    # Navigation items with Tabler Icons (dark context for sidebar)
    nav_items = [
        (HavenIcons.HOME, "Home", "home"),
        (HavenIcons.TRENDING, "Trending", "trending"),
        (HavenIcons.EXPLORE, "Explore", "explore"),
        (HavenIcons.SEARCH, "Search", "search"),
        (HavenIcons.CAMPAIGN, "Create Campaign", "campaign"),
        (profile_icon_name, "Profile", "profile")
    ]
    
    for icon_name, label, page in nav_items:
        col1, col2 = st.sidebar.columns([1, 4])
        with col1:
            icon_manager.render_icon(icon_name, 20, ThemeManager.get_icon_color("dark"), "dark")
        with col2:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
    
    # Logout button
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns([1, 4])
    with col1:
        icon_manager.render_icon(HavenIcons.LOGOUT, 20, '#F44336', "dark")
    with col2:
        if st.button("Logout", key="logout_btn", use_container_width=True):
            logout_user()
            st.rerun()

# ===== PAGE FUNCTIONS =====
def render_welcome_page(icon_manager):
    """Render welcome page with Tabler Icons"""
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    
    # Header with rupee icon (white on dark background)
    rupee_icon = icon_manager.get_icon_html(HavenIcons.RUPEE, 32, "white", "dark")
    st.markdown(f'''
    <h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">
        {rupee_icon}
        Welcome to Haven
    </h1>
    ''', unsafe_allow_html=True)
    
    st.markdown('<p style="margin: 10px 0 0 0; opacity: 0.9;">Empowering Communities Through Transparent Crowdfunding</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Social login buttons (dark context)
        render_social_login_buttons(icon_manager)
        
        st.markdown("---")
        st.markdown("### Or use email")
        
        # Email/Password Login
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                if st.form_submit_button("Sign In", use_container_width=True):
                    if email and password:
                        # Simulate login with sample user data
                        login_user(email, {
                            "email": email, 
                            "login_method": "email",
                            "name": "John Doe",
                            "account_type": "Individual",
                            "phone": "+1234567890",  # Complete profile
                            "address": "123 Main St",
                            "bio": "Passionate about helping communities"
                        })
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Please enter both email and password")
            
            with col_register:
                if st.form_submit_button("Create Account", use_container_width=True):
                    st.session_state.show_register = True
                    st.rerun()
        
        # Navigation links
        st.markdown("---")
        if st.session_state.get('show_register', False):
            if st.button("Already have an account? Sign in here", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()
        else:
            if st.button("Don't have an account? Register here", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_register_page(icon_manager):
    """Render registration page with Tabler Icons"""
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    
    # Header with circle-plus icon (white on dark background)
    plus_icon = icon_manager.get_icon_html(HavenIcons.CAMPAIGN, 32, "white", "dark")
    st.markdown(f'''
    <h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">
        {plus_icon}
        Create Your Account
    </h1>
    ''', unsafe_allow_html=True)
    
    st.markdown('<p style="margin: 10px 0 0 0; opacity: 0.9;">Join Haven and start making a difference</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Account Type Selection
        st.markdown("### Account Type")
        account_type = st.radio(
            "Choose your account type:",
            ["Individual", "Organization"],
            horizontal=True
        )
        
        st.markdown("---")
        
        # Registration Form
        with st.form("register_form"):
            if account_type == "Individual":
                st.markdown("### Personal Information")
                first_name = st.text_input("First Name", placeholder="Enter your first name")
                last_name = st.text_input("Last Name", placeholder="Enter your last name")
                full_name = f"{first_name} {last_name}".strip()
            else:
                st.markdown("### Organization Information")
                full_name = st.text_input("Organization Name", placeholder="Enter organization name")
                org_type = st.selectbox("Organization Type", [
                    "Non-Profit Organization",
                    "Educational Institution", 
                    "Healthcare Organization",
                    "Community Group",
                    "Religious Organization",
                    "Other"
                ])
            
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            st.markdown("### Document Verification")
            st.markdown("Please upload the required documents for verification:")
            
            # Document upload sections with Tabler Icons (light context)
            col_doc1, col_doc2 = st.columns(2)
            
            with col_doc1:
                user_icon = icon_manager.get_icon_html(HavenIcons.PROFILE, 24, ThemeManager.get_primary_color(), "light")
                st.markdown(f'''
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    {user_icon}
                    <strong>Identity Proof</strong>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('<div class="upload-area">', unsafe_allow_html=True)
                identity_doc = st.file_uploader(
                    "Upload ID Document",
                    type=['pdf', 'jpg', 'jpeg', 'png'],
                    help="Government ID, Passport, or Driver's License",
                    key="identity_upload"
                )
                st.markdown("Limit 200MB per file • PDF, JPG, JPEG, PNG", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_doc2:
                home_icon = icon_manager.get_icon_html(HavenIcons.HOME, 24, ThemeManager.get_primary_color(), "light")
                st.markdown(f'''
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    {home_icon}
                    <strong>Address Proof</strong> <span style="color: #666;">(Optional)</span>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('<div class="upload-area">', unsafe_allow_html=True)
                address_doc = st.file_uploader(
                    "Upload Address Document",
                    type=['pdf', 'jpg', 'jpeg', 'png'],
                    help="Utility bill or rental agreement (optional)",
                    key="address_upload"
                )
                st.markdown("Utility bill or rental agreement (optional)", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Terms and conditions with info tooltips
            st.markdown("### Terms and Conditions")
            
            terms_text = render_info_tooltip("I agree to the Terms and Conditions", "By checking this box, you agree to our terms of service and privacy policy.", icon_manager)
            kyc_text = render_info_tooltip("I consent to KYC verification", "Know Your Customer verification helps us ensure platform security and compliance.", icon_manager)
            data_text = render_info_tooltip("I agree to data processing", "We process your data securely to provide our services and comply with regulations.", icon_manager)
            
            terms_agreed = st.checkbox(terms_text, unsafe_allow_html=True)
            kyc_consent = st.checkbox(kyc_text, unsafe_allow_html=True)
            data_processing = st.checkbox(data_text, unsafe_allow_html=True)
            
            # Submit button
            if st.form_submit_button("Register", use_container_width=True):
                if not full_name or not email or not password:
                    st.error("❌ Please fill in all required fields")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif not terms_agreed or not kyc_consent or not data_processing:
                    st.error("❌ Please agree to all terms and conditions")
                elif not identity_doc:
                    st.error("❌ Identity proof document is required")
                else:
                    # Simulate successful registration with incomplete profile
                    login_user(email, {
                        "name": full_name,
                        "email": email,
                        "account_type": account_type,
                        "registration_time": datetime.now()
                        # Missing optional fields - profile will be incomplete
                    })
                    st.success("✅ Registration successful! Welcome to Haven!")
                    st.rerun()
        
        # Navigation link
        st.markdown("---")
        if st.button("Already have an account? Sign in here", use_container_width=True):
            st.session_state.show_register = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_home_page(icon_manager):
    """Render home dashboard with Tabler Icons"""
    user_data = st.session_state.get('user_data', {})
    user_name = user_data.get('name', st.session_state.get('username', 'User'))
    
    # Header with trending-up icon (white on dark background)
    trending_icon = icon_manager.get_icon_html(HavenIcons.TRENDING, 32, "white", "dark")
    st.markdown(f'''
    <div class="app-header">
        <h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">
            {trending_icon}
            Welcome back, {user_name}!
        </h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # Dashboard content with light context icons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        campaign_icon = icon_manager.get_icon_html(HavenIcons.CAMPAIGN, 24, ThemeManager.get_primary_color(), "light")
        st.markdown(f'''
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            {campaign_icon}
            <strong>My Campaigns</strong>
        </div>
        ''', unsafe_allow_html=True)
        st.metric("Active", "3", "+1")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        rupee_icon = icon_manager.get_icon_html(HavenIcons.RUPEE, 24, ThemeManager.get_secondary_color(), "light")
        st.markdown(f'''
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            {rupee_icon}
            <strong>Total Raised</strong>
        </div>
        ''', unsafe_allow_html=True)
        st.metric("Amount", "₹12,450", "+₹2,100")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        profile_icon_name = ProfileManager.get_profile_icon_name(user_data)
        profile_icon = icon_manager.get_icon_html(profile_icon_name, 24, "#FF5722", "light")
        st.markdown(f'''
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            {profile_icon}
            <strong>Supporters</strong>
        </div>
        ''', unsafe_allow_html=True)
        st.metric("Count", "89", "+12")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity
    st.markdown("### Recent Activity")
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    
    activities = [
        ("New donation received", "₹500", "2 hours ago"),
        ("Campaign milestone reached", "75% funded", "1 day ago"),
        ("Document verified", "Identity confirmed", "3 days ago")
    ]
    
    for activity, detail, time in activities:
        activity_icon = icon_manager.get_icon_html(HavenIcons.TRENDING, 16, "#666", "light")
        st.markdown(f'''
        <div style="display: flex; align-items: center; gap: 8px; padding: 8px 0; border-bottom: 1px solid #eee;">
            {activity_icon}
            <strong>{activity}</strong> - {detail} 
            <span style="color: #666; margin-left: auto;">{time}</span>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_campaign_page(icon_manager):
    """Render campaign management page with Tabler Icons"""
    campaign_icon = icon_manager.get_icon_html(HavenIcons.CAMPAIGN, 32, "white", "dark")
    st.markdown(f'''
    <div class="app-header">
        <h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">
            {campaign_icon}
            Campaign Management
        </h1>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("### Create New Campaign")
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.write("Start a new crowdfunding campaign to make a difference in your community.")
    
    if st.button("Create Campaign", use_container_width=True):
        st.success("Campaign creation feature coming soon!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_explore_page(icon_manager):
    """Render explore campaigns page with Tabler Icons"""
    explore_icon = icon_manager.get_icon_html(HavenIcons.EXPLORE, 32, "white", "dark")
    st.markdown(f'''
    <div class="app-header">
        <h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">
            {explore_icon}
            Explore Campaigns
        </h1>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("### Featured Campaigns")
    
    # Sample campaigns
    campaigns = [
        {"title": "Clean Water for Rural Communities", "raised": "₹85,000", "goal": "₹1,50,000", "supporters": 45},
        {"title": "Education Support Program", "raised": "₹1,22,000", "goal": "₹2,00,000", "supporters": 78},
        {"title": "Medical Equipment Fund", "raised": "₹68,000", "goal": "₹1,00,000", "supporters": 32}
    ]
    
    for campaign in campaigns:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown(f"**{campaign['title']}**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Raised", campaign['raised'])
        with col2:
            st.metric("Goal", campaign['goal'])
        with col3:
            st.metric("Supporters", campaign['supporters'])
        
        # Calculate progress
        raised_num = int(campaign['raised'].replace('₹', '').replace(',', ''))
        goal_num = int(campaign['goal'].replace('₹', '').replace(',', ''))
        progress = raised_num / goal_num
        st.progress(progress)
        
        if st.button(f"View Details", key=f"view_{campaign['title']}", use_container_width=True):
            st.info("Campaign details feature coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_search_page(icon_manager):
    """Render search page with Tabler Icons"""
    search_icon = icon_manager.get_icon_html(HavenIcons.SEARCH, 32, "white", "dark")
    st.markdown(f'''
    <div class="app-header">
        <h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">
            {search_icon}
            Search Campaigns
        </h1>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    
    # Search form
    search_query = st.text_input("Search for campaigns", placeholder="Enter keywords...")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", ["All", "Education", "Healthcare", "Environment", "Community"])
    with col2:
        location = st.text_input("Location", placeholder="City or region")
    
    if st.button("Search", use_container_width=True):
        if search_query:
            st.success(f"Searching for: {search_query}")
        else:
            st.warning("Please enter a search term")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_profile_page(icon_manager):
    """Render user profile page with dynamic Tabler Icons"""
    user_data = st.session_state.get('user_data', {})
    profile_icon_name = ProfileManager.get_profile_icon_name(user_data)
    profile_icon = icon_manager.get_icon_html(profile_icon_name, 32, "white", "dark")
    
    st.markdown(f'''
    <div class="app-header">
        <h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">
            {profile_icon}
            User Profile
        </h1>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### Account Information")
    
    # Show profile completion status
    is_complete = ProfileManager.check_profile_completion(user_data)
    status_color = "#4CAF50" if is_complete else "#FF9800"
    status_text = "Complete" if is_complete else "Incomplete"
    status_icon = icon_manager.get_icon_html(profile_icon_name, 24, status_color, "light")
    
    st.markdown(f'''
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 15px;">
        {status_icon}
        <strong>Profile Status: <span style="color: {status_color};">{status_text}</span></strong>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Name", value=user_data.get('name', ''), disabled=True)
        st.text_input("Email", value=user_data.get('email', ''), disabled=True)
        st.text_input("Phone", value=user_data.get('phone', 'Not provided'), disabled=True)
    with col2:
        st.text_input("Account Type", value=user_data.get('account_type', 'Individual'), disabled=True)
        st.text_input("Address", value=user_data.get('address', 'Not provided'), disabled=True)
        if 'registration_time' in user_data:
            st.text_input("Member Since", value=user_data['registration_time'].strftime('%Y-%m-%d'), disabled=True)
    
    if not is_complete:
        st.warning("⚠️ Complete your profile to unlock all features and get a filled profile icon!")
    
    if st.button("Edit Profile", use_container_width=True):
        st.info("Profile editing feature coming soon!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== MAIN APPLICATION =====
def main():
    """Main application function"""
    st.set_page_config(
        page_title="Haven - Crowdfunding Platform",
        page_icon="❤️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize Tabler Icon Manager
    icon_manager = TablerIconManager()
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'translation_enabled' not in st.session_state:
        st.session_state.translation_enabled = False
    
    # Check authentication and manage body class
    if not check_authentication():
        # Hide sidebar for unauthenticated users
        st.markdown('''
        <script>
        document.body.classList.remove('authenticated');
        </script>
        ''', unsafe_allow_html=True)
        
        # Show registration or login page
        if st.session_state.get('show_register', False):
            render_register_page(icon_manager)
        else:
            render_welcome_page(icon_manager)
    else:
        # Show sidebar for authenticated users
        st.markdown('''
        <script>
        document.body.classList.add('authenticated');
        </script>
        ''', unsafe_allow_html=True)
        
        # Render navigation
        render_navigation(icon_manager)
        
        # Render current page
        current_page = st.session_state.get('current_page', 'home')
        
        if current_page == 'home':
            render_home_page(icon_manager)
        elif current_page == 'campaign':
            render_campaign_page(icon_manager)
        elif current_page == 'explore':
            render_explore_page(icon_manager)
        elif current_page == 'search':
            render_search_page(icon_manager)
        elif current_page == 'profile':
            render_profile_page(icon_manager)
        elif current_page == 'trending':
            render_home_page(icon_manager)  # Trending uses same as home
        else:
            render_home_page(icon_manager)

if __name__ == "__main__":
    main()

