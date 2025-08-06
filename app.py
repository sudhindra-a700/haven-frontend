import streamlit as st
import requests
import json
import os
from datetime import datetime
import io
import base64

# Note: This app uses Tabler Icons via pytablericons package
# Install with: pip install pytablericons
# For deployment, add 'pytablericons' to requirements.txt

try:
    from pytablericons import TablerIcons, OutlineIcon, FilledIcon
    TABLER_AVAILABLE = True
except ImportError:
    TABLER_AVAILABLE = False
    st.error("⚠️ pytablericons package not installed. Please install with: pip install pytablericons")

# ===== TABLER ICONS MANAGER =====
class TablerIconManager:
    """Professional Tabler Icons manager for HAVEN application"""
    
    def __init__(self):
        self.default_size = 20
        self.default_color = '#4CAF50'  # Light green theme
        self.default_stroke = 2.0
        self.cache = {}
    
    def get_icon(self, icon, size=None, color=None, stroke_width=None):
        """Get a Tabler icon with caching for performance"""
        if not TABLER_AVAILABLE:
            return None
            
        size = size or self.default_size
        color = color or self.default_color
        stroke_width = stroke_width or self.default_stroke
        
        # Create cache key
        cache_key = f"{icon}_{size}_{color}_{stroke_width}"
        
        if cache_key not in self.cache:
            try:
                self.cache[cache_key] = TablerIcons.load(
                    icon, 
                    size=size, 
                    color=color, 
                    stroke_width=stroke_width
                )
            except Exception as e:
                st.error(f"Error loading icon {icon}: {e}")
                return None
        
        return self.cache[cache_key]
    
    def icon_to_base64(self, icon_image):
        """Convert PIL image to base64 for HTML embedding"""
        if icon_image is None:
            return ""
        
        buffer = io.BytesIO()
        icon_image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def render_icon_text(self, icon, text, size=None, color=None):
        """Render icon with text in columns"""
        icon_img = self.get_icon(icon, size=size, color=color)
        if icon_img:
            col1, col2 = st.columns([1, 10])
            with col1:
                st.image(icon_img, width=size or self.default_size)
            with col2:
                st.write(text)
        else:
            st.write(f"📍 {text}")  # Fallback emoji
    
    def get_icon_html(self, icon, size=None, color=None):
        """Get icon as HTML img tag"""
        icon_img = self.get_icon(icon, size=size, color=color)
        if icon_img:
            icon_b64 = self.icon_to_base64(icon_img)
            size_px = size or self.default_size
            return f'<img src="{icon_b64}" width="{size_px}" height="{size_px}" style="vertical-align: middle; margin-right: 8px;">'
        return "📍"  # Fallback emoji

# Initialize icon manager
icon_manager = TablerIconManager()

# ===== ICON DEFINITIONS =====
class HavenIcons:
    """Centralized icon definitions for HAVEN application"""
    
    # Navigation Icons
    HOME = OutlineIcon.HOME if TABLER_AVAILABLE else None
    CAMPAIGN = OutlineIcon.TARGET if TABLER_AVAILABLE else None
    EXPLORE = OutlineIcon.COMPASS if TABLER_AVAILABLE else None
    SEARCH = OutlineIcon.SEARCH if TABLER_AVAILABLE else None
    PROFILE = OutlineIcon.USER if TABLER_AVAILABLE else None
    
    # Authentication Icons
    LOGIN = OutlineIcon.LOGIN if TABLER_AVAILABLE else None
    LOGOUT = OutlineIcon.LOGOUT if TABLER_AVAILABLE else None
    REGISTER = OutlineIcon.USER_PLUS if TABLER_AVAILABLE else None
    
    # Action Icons
    UPLOAD = OutlineIcon.UPLOAD if TABLER_AVAILABLE else None
    DOWNLOAD = OutlineIcon.DOWNLOAD if TABLER_AVAILABLE else None
    EDIT = OutlineIcon.EDIT if TABLER_AVAILABLE else None
    DELETE = OutlineIcon.TRASH if TABLER_AVAILABLE else None
    SAVE = OutlineIcon.DEVICE_FLOPPY if TABLER_AVAILABLE else None
    
    # Status Icons
    SUCCESS = FilledIcon.CIRCLE_CHECK if TABLER_AVAILABLE else None
    WARNING = FilledIcon.ALERT_TRIANGLE if TABLER_AVAILABLE else None
    ERROR = FilledIcon.CIRCLE_X if TABLER_AVAILABLE else None
    INFO = FilledIcon.INFO_CIRCLE if TABLER_AVAILABLE else None
    
    # Document Icons
    DOCUMENT = OutlineIcon.FILE_TEXT if TABLER_AVAILABLE else None
    CERTIFICATE = OutlineIcon.AWARD if TABLER_AVAILABLE else None
    VERIFICATION = OutlineIcon.SHIELD_CHECK if TABLER_AVAILABLE else None
    
    # Social Icons
    GOOGLE = OutlineIcon.BRAND_GOOGLE if TABLER_AVAILABLE else None
    FACEBOOK = OutlineIcon.BRAND_FACEBOOK if TABLER_AVAILABLE else None
    
    # General Icons
    GLOBE = OutlineIcon.WORLD if TABLER_AVAILABLE else None
    LOCK = OutlineIcon.LOCK if TABLER_AVAILABLE else None
    HEART = OutlineIcon.HEART if TABLER_AVAILABLE else None
    STAR = OutlineIcon.STAR if TABLER_AVAILABLE else None
    MAIL = OutlineIcon.MAIL if TABLER_AVAILABLE else None
    PHONE = OutlineIcon.PHONE if TABLER_AVAILABLE else None
    CALENDAR = OutlineIcon.CALENDAR if TABLER_AVAILABLE else None
    CLOCK = OutlineIcon.CLOCK if TABLER_AVAILABLE else None
    MONEY = OutlineIcon.CURRENCY_DOLLAR if TABLER_AVAILABLE else None
    CHART = OutlineIcon.CHART_LINE if TABLER_AVAILABLE else None

# ===== CONFIGURATION =====
class Config:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID", "")
    TRANSLATION_ENABLED = os.getenv("TRANSLATION_ENABLED", "true").lower() == "true"
    OAUTH_ENABLED = os.getenv("OAUTH_ENABLED", "true").lower() == "true"

# ===== STYLING =====
def load_custom_css():
    """Load custom CSS for HAVEN with light green theme"""
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
    
    /* Button styling */
    .custom-button {
        background: var(--primary-color);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        text-decoration: none;
        font-weight: 500;
    }
    
    .custom-button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
    }
    
    .secondary-button {
        background: var(--secondary-color);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .secondary-button:hover {
        background: #1976D2;
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
    
    /* Status message styling */
    .status-success {
        background: #E8F5E8;
        border: 1px solid #4CAF50;
        color: #2E7D32;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .status-warning {
        background: #FFF3E0;
        border: 1px solid #FF9800;
        color: #E65100;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .status-error {
        background: #FFEBEE;
        border: 1px solid #F44336;
        color: #C62828;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Social login buttons */
    .google-button {
        background: #4285f4;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        justify-content: center;
        margin: 8px 0;
    }
    
    .google-button:hover {
        background: #3367d6;
    }
    
    .facebook-button {
        background: #1877f2;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        justify-content: center;
        margin: 8px 0;
    }
    
    .facebook-button:hover {
        background: #166fe5;
    }
    
    /* Link styling */
    .auth-link {
        color: var(--primary-color);
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .auth-link:hover {
        color: var(--primary-dark);
        text-decoration: underline;
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
        
        .custom-button, .google-button, .facebook-button {
            padding: 14px 20px;
            font-size: 16px;
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

# ===== NAVIGATION FUNCTIONS =====
def render_navigation():
    """Render navigation sidebar with Tabler icons"""
    if not check_authentication():
        return
    
    st.sidebar.markdown("### Navigation")
    
    # Navigation items with Tabler icons
    nav_items = [
        (HavenIcons.HOME, "Home", "home"),
        (HavenIcons.CAMPAIGN, "Campaign", "campaign"),
        (HavenIcons.EXPLORE, "Explore", "explore"),
        (HavenIcons.SEARCH, "Search", "search"),
        (HavenIcons.PROFILE, "Profile", "profile")
    ]
    
    for icon, label, page in nav_items:
        if TABLER_AVAILABLE and icon:
            icon_img = icon_manager.get_icon(icon, size=20, color='#4CAF50')
            col1, col2 = st.sidebar.columns([1, 4])
            with col1:
                if icon_img:
                    st.image(icon_img, width=20)
                else:
                    st.write("📍")
            with col2:
                if st.button(label, key=f"nav_{page}", use_container_width=True):
                    st.session_state.current_page = page
        else:
            # Fallback without icons
            if st.sidebar.button(f"📍 {label}", key=f"nav_{page}"):
                st.session_state.current_page = page
    
    # Logout button
    st.sidebar.markdown("---")
    if TABLER_AVAILABLE and HavenIcons.LOGOUT:
        icon_img = icon_manager.get_icon(HavenIcons.LOGOUT, size=20, color='#F44336')
        col1, col2 = st.sidebar.columns([1, 4])
        with col1:
            if icon_img:
                st.image(icon_img, width=20)
            else:
                st.write("🚪")
        with col2:
            if st.button("Logout", key="logout_btn", use_container_width=True):
                logout_user()
                st.rerun()
    else:
        if st.sidebar.button("🚪 Logout", key="logout_btn"):
            logout_user()
            st.rerun()

# ===== PAGE FUNCTIONS =====
def render_welcome_page():
    """Render welcome page with login options"""
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    
    # Header with icon
    if TABLER_AVAILABLE and HavenIcons.HEART:
        icon_html = icon_manager.get_icon_html(HavenIcons.HEART, size=32, color='white')
        st.markdown(f'<h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">{icon_html}Welcome to Haven</h1>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 style="margin: 0;">❤️ Welcome to Haven</h1>', unsafe_allow_html=True)
    
    st.markdown('<p style="margin: 10px 0 0 0; opacity: 0.9;">Empowering Communities Through Transparent Crowdfunding</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Login options
        st.markdown("### Choose Your Login Method")
        
        # Google Login Button
        if TABLER_AVAILABLE and HavenIcons.GOOGLE:
            google_icon = icon_manager.get_icon_html(HavenIcons.GOOGLE, size=20, color='white')
            google_button = f'''
            <button class="google-button" onclick="alert('Google OAuth integration required')">
                {google_icon}Continue with Google
            </button>
            '''
        else:
            google_button = '''
            <button class="google-button" onclick="alert('Google OAuth integration required')">
                🇬 Continue with Google
            </button>
            '''
        st.markdown(google_button, unsafe_allow_html=True)
        
        # Facebook Login Button
        if TABLER_AVAILABLE and HavenIcons.FACEBOOK:
            facebook_icon = icon_manager.get_icon_html(HavenIcons.FACEBOOK, size=20, color='white')
            facebook_button = f'''
            <button class="facebook-button" onclick="alert('Facebook OAuth integration required')">
                {facebook_icon}Continue with Facebook
            </button>
            '''
        else:
            facebook_button = '''
            <button class="facebook-button" onclick="alert('Facebook OAuth integration required')">
                🇫 Continue with Facebook
            </button>
            '''
        st.markdown(facebook_button, unsafe_allow_html=True)
        
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
                        # Simulate login
                        login_user(email, {"email": email, "login_method": "email"})
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
            st.markdown('<p style="text-align: center;">Already have an account? <a href="#" class="auth-link" onclick="window.location.reload()">Sign in here</a></p>', unsafe_allow_html=True)
        else:
            if st.button("Don't have an account? Register here", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_register_page():
    """Render registration page with Tabler icons"""
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    
    # Header with icon
    if TABLER_AVAILABLE and HavenIcons.REGISTER:
        icon_html = icon_manager.get_icon_html(HavenIcons.REGISTER, size=32, color='white')
        st.markdown(f'<h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">{icon_html}Create Your Account</h1>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 style="margin: 0;">📝 Create Your Account</h1>', unsafe_allow_html=True)
    
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
            
            # Document upload sections with Tabler icons
            col_doc1, col_doc2 = st.columns(2)
            
            with col_doc1:
                if TABLER_AVAILABLE and HavenIcons.DOCUMENT:
                    icon_html = icon_manager.get_icon_html(HavenIcons.DOCUMENT, size=24, color='#4CAF50')
                    st.markdown(f'<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">{icon_html}<strong>Identity Proof</strong></div>', unsafe_allow_html=True)
                else:
                    st.markdown("📄 **Identity Proof**")
                
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
                if TABLER_AVAILABLE and HavenIcons.CERTIFICATE:
                    icon_html = icon_manager.get_icon_html(HavenIcons.CERTIFICATE, size=24, color='#4CAF50')
                    st.markdown(f'<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">{icon_html}<strong>Address Proof</strong> <span style="color: #666;">(Optional)</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown("🏆 **Address Proof** *(Optional)*")
                
                st.markdown('<div class="upload-area">', unsafe_allow_html=True)
                address_doc = st.file_uploader(
                    "Upload Address Document",
                    type=['pdf', 'jpg', 'jpeg', 'png'],
                    help="Utility bill or rental agreement (optional)",
                    key="address_upload"
                )
                st.markdown("Utility bill or rental agreement (optional)", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Additional documents for organizations
            if account_type == "Organization":
                st.markdown("### Organization Documents")
                
                col_org1, col_org2 = st.columns(2)
                
                with col_org1:
                    if TABLER_AVAILABLE and HavenIcons.VERIFICATION:
                        icon_html = icon_manager.get_icon_html(HavenIcons.VERIFICATION, size=24, color='#4CAF50')
                        st.markdown(f'<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">{icon_html}<strong>Registration Certificate</strong></div>', unsafe_allow_html=True)
                    else:
                        st.markdown("✔️ **Registration Certificate**")
                    
                    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
                    reg_cert = st.file_uploader(
                        "Upload Registration Certificate",
                        type=['pdf', 'jpg', 'jpeg', 'png'],
                        help="Official organization registration",
                        key="reg_cert_upload"
                    )
                    st.markdown("Official organization registration", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_org2:
                    if TABLER_AVAILABLE and HavenIcons.DOCUMENT:
                        icon_html = icon_manager.get_icon_html(HavenIcons.DOCUMENT, size=24, color='#4CAF50')
                        st.markdown(f'<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">{icon_html}<strong>Bank Statement</strong> <span style="color: #666;">(Optional)</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown("📄 **Bank Statement** *(Optional)*")
                    
                    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
                    bank_statement = st.file_uploader(
                        "Upload Bank Statement",
                        type=['pdf', 'jpg', 'jpeg', 'png'],
                        help="Recent 3-month bank statement (optional)",
                        key="bank_statement_upload"
                    )
                    st.markdown("Recent 3-month bank statement (optional)", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Terms and conditions
            st.markdown("### Terms and Conditions")
            
            terms_agreed = st.checkbox("✅ I agree to the Terms and Conditions")
            kyc_consent = st.checkbox("🔵 I consent to KYC verification")
            data_processing = st.checkbox("🔒 I agree to data processing")
            
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
                    # Simulate successful registration
                    login_user(email, {
                        "name": full_name,
                        "email": email,
                        "account_type": account_type,
                        "registration_time": datetime.now()
                    })
                    st.success("✅ Registration successful! Welcome to Haven!")
                    st.rerun()
        
        # Navigation link
        st.markdown("---")
        if st.button("Already have an account? Sign in here", use_container_width=True):
            st.session_state.show_register = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_home_page():
    """Render home dashboard with Tabler icons"""
    user_data = st.session_state.get('user_data', {})
    user_name = user_data.get('name', st.session_state.get('username', 'User'))
    
    # Header
    if TABLER_AVAILABLE and HavenIcons.HOME:
        icon_html = icon_manager.get_icon_html(HavenIcons.HOME, size=32, color='#4CAF50')
        st.markdown(f'<div class="app-header"><h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">{icon_html}Welcome back, {user_name}!</h1></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="app-header"><h1 style="margin: 0;">🏠 Welcome back, {user_name}!</h1></div>', unsafe_allow_html=True)
    
    # Dashboard content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        if TABLER_AVAILABLE and HavenIcons.CAMPAIGN:
            icon_manager.render_icon_text(HavenIcons.CAMPAIGN, "My Campaigns", size=24, color='#4CAF50')
        else:
            st.write("🎯 **My Campaigns**")
        st.metric("Active", "3", "+1")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        if TABLER_AVAILABLE and HavenIcons.MONEY:
            icon_manager.render_icon_text(HavenIcons.MONEY, "Total Raised", size=24, color='#2196F3')
        else:
            st.write("💰 **Total Raised**")
        st.metric("Amount", "$12,450", "+$2,100")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        if TABLER_AVAILABLE and HavenIcons.HEART:
            icon_manager.render_icon_text(HavenIcons.HEART, "Supporters", size=24, color='#FF5722')
        else:
            st.write("❤️ **Supporters**")
        st.metric("Count", "89", "+12")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity
    st.markdown("### Recent Activity")
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    
    activities = [
        ("New donation received", "$50", "2 hours ago"),
        ("Campaign milestone reached", "75% funded", "1 day ago"),
        ("Document verified", "Identity confirmed", "3 days ago")
    ]
    
    for activity, detail, time in activities:
        if TABLER_AVAILABLE and HavenIcons.CLOCK:
            icon_html = icon_manager.get_icon_html(HavenIcons.CLOCK, size=16, color='#666')
            st.markdown(f'<div style="display: flex; align-items: center; gap: 8px; padding: 8px 0; border-bottom: 1px solid #eee;">{icon_html}<strong>{activity}</strong> - {detail} <span style="color: #666; margin-left: auto;">{time}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f"🕐 **{activity}** - {detail} *({time})*")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_campaign_page():
    """Render campaign management page"""
    if TABLER_AVAILABLE and HavenIcons.CAMPAIGN:
        icon_html = icon_manager.get_icon_html(HavenIcons.CAMPAIGN, size=32, color='#4CAF50')
        st.markdown(f'<div class="app-header"><h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">{icon_html}Campaign Management</h1></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="app-header"><h1 style="margin: 0;">🎯 Campaign Management</h1></div>', unsafe_allow_html=True)
    
    st.markdown("### Create New Campaign")
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.write("Start a new crowdfunding campaign to make a difference in your community.")
    
    if st.button("Create Campaign", use_container_width=True):
        st.success("Campaign creation feature coming soon!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_explore_page():
    """Render explore campaigns page"""
    if TABLER_AVAILABLE and HavenIcons.EXPLORE:
        icon_html = icon_manager.get_icon_html(HavenIcons.EXPLORE, size=32, color='#4CAF50')
        st.markdown(f'<div class="app-header"><h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">{icon_html}Explore Campaigns</h1></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="app-header"><h1 style="margin: 0;">🧭 Explore Campaigns</h1></div>', unsafe_allow_html=True)
    
    st.markdown("### Featured Campaigns")
    
    # Sample campaigns
    campaigns = [
        {"title": "Clean Water for Rural Communities", "raised": "$8,500", "goal": "$15,000", "supporters": 45},
        {"title": "Education Support Program", "raised": "$12,200", "goal": "$20,000", "supporters": 78},
        {"title": "Medical Equipment Fund", "raised": "$6,800", "goal": "$10,000", "supporters": 32}
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
        
        progress = int(campaign['raised'].replace('$', '').replace(',', '')) / int(campaign['goal'].replace('$', '').replace(',', ''))
        st.progress(progress)
        
        if st.button(f"View Details", key=f"view_{campaign['title']}", use_container_width=True):
            st.info("Campaign details feature coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_search_page():
    """Render search page"""
    if TABLER_AVAILABLE and HavenIcons.SEARCH:
        icon_html = icon_manager.get_icon_html(HavenIcons.SEARCH, size=32, color='#4CAF50')
        st.markdown(f'<div class="app-header"><h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">{icon_html}Search Campaigns</h1></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="app-header"><h1 style="margin: 0;">🔍 Search Campaigns</h1></div>', unsafe_allow_html=True)
    
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

def render_profile_page():
    """Render user profile page"""
    if TABLER_AVAILABLE and HavenIcons.PROFILE:
        icon_html = icon_manager.get_icon_html(HavenIcons.PROFILE, size=32, color='#4CAF50')
        st.markdown(f'<div class="app-header"><h1 style="margin: 0; display: flex; align-items: center; justify-content: center; gap: 10px;">{icon_html}User Profile</h1></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="app-header"><h1 style="margin: 0;">👤 User Profile</h1></div>', unsafe_allow_html=True)
    
    user_data = st.session_state.get('user_data', {})
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### Account Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Name", value=user_data.get('name', ''), disabled=True)
        st.text_input("Email", value=user_data.get('email', ''), disabled=True)
    with col2:
        st.text_input("Account Type", value=user_data.get('account_type', 'Individual'), disabled=True)
        if 'registration_time' in user_data:
            st.text_input("Member Since", value=user_data['registration_time'].strftime('%Y-%m-%d'), disabled=True)
    
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
    
    # Load custom CSS
    load_custom_css()
    
    # Check if pytablericons is available
    if not TABLER_AVAILABLE:
        st.warning("⚠️ For the best experience, install pytablericons: `pip install pytablericons`")
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    
    # Check authentication
    if not check_authentication():
        # Show registration or login page
        if st.session_state.get('show_register', False):
            render_register_page()
        else:
            render_welcome_page()
    else:
        # Render navigation
        render_navigation()
        
        # Render current page
        current_page = st.session_state.get('current_page', 'home')
        
        if current_page == 'home':
            render_home_page()
        elif current_page == 'campaign':
            render_campaign_page()
        elif current_page == 'explore':
            render_explore_page()
        elif current_page == 'search':
            render_search_page()
        elif current_page == 'profile':
            render_profile_page()
        else:
            render_home_page()

if __name__ == "__main__":
    main()

