"""
HAVEN Crowdfunding Platform - Fixed Bootstrap Icons Implementation
Resolves AttributeError and CSS display issues
"""

import streamlit as st
import requests
import time
import uuid
from datetime import datetime, timedelta

# ============================================================================
# SIMPLIFIED BOOTSTRAP ICONS SYSTEM (Fixed)
# ============================================================================

class BootstrapIcons:
    """Simplified Bootstrap Icons using Unicode symbols that work reliably"""
    
    # Navigation Icons
    HOME = "🏠"
    CAMPAIGN = "🎯"
    EXPLORE = "🧭"
    SEARCH = "🔍"
    PROFILE = "👤"
    
    # Action Icons
    LOGIN = "🔑"
    LOGOUT = "🚪"
    REGISTER = "📝"
    UPLOAD = "📤"
    DOWNLOAD = "📥"
    CREATE = "➕"
    EDIT = "✏️"
    DELETE = "🗑️"
    SAVE = "💾"
    SHARE = "📤"
    COPY = "📋"
    
    # Status Icons
    SUCCESS = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    INFO = "ℹ️"
    PENDING = "⏳"
    
    # Document Icons
    DOCUMENT = "📄"
    CERTIFICATE = "🏆"
    VERIFICATION = "✔️"
    FILE_PDF = "📄"
    FILE_IMAGE = "🖼️"
    
    # Social Icons
    GOOGLE = "🇬"
    FACEBOOK = "🇫"
    
    # General Icons
    LANGUAGE = "🌐"
    SECURITY = "🔒"
    HEART = "❤️"
    STAR = "⭐"
    PLUS = "➕"
    MINUS = "➖"
    EMAIL = "📧"
    PHONE = "📞"
    LOCATION = "📍"
    CALENDAR = "📅"
    CLOCK = "🕐"
    MONEY = "💰"
    CHART = "📊"
    GRAPH = "📈"
    SHIELD = "🛡️"
    BELL = "🔔"
    BOOKMARK = "🔖"
    TAG = "🏷️"
    FILTER = "🔽"
    SORT = "🔀"
    SETTINGS = "⚙️"
    HELP = "❓"
    CLOSE = "❌"
    MENU = "☰"
    ARROW_LEFT = "←"
    ARROW_RIGHT = "→"
    ARROW_UP = "↑"
    ARROW_DOWN = "↓"
    EYE = "👁️"
    EYE_SLASH = "🙈"
    LOCK = "🔒"
    UNLOCK = "🔓"
    PERSON = "👤"
    BUILDING = "🏢"

icons = BootstrapIcons()

def get_clean_css():
    """Get clean CSS without Bootstrap Icons dependency"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Navigation Styles */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 6px;
        transition: all 0.2s ease;
        margin-bottom: 4px;
        text-decoration: none;
        color: #495057;
        font-weight: 500;
    }
    
    .nav-item:hover {
        background: #f8f9fa;
        color: #2e7d32;
    }
    
    .nav-item.active {
        background: #e8f5e8;
        color: #2e7d32;
        border-left: 3px solid #4caf50;
    }
    
    /* Button Styles */
    .btn-minimal {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        background: white;
        color: #495057;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .btn-minimal:hover {
        background: #f8f9fa;
        border-color: #adb5bd;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .btn-primary {
        background: #4caf50;
        border-color: #4caf50;
        color: white;
    }
    
    .btn-primary:hover {
        background: #45a049;
        border-color: #45a049;
    }
    
    /* Social Login Buttons */
    .btn-google {
        background: #4285f4;
        border-color: #4285f4;
        color: white;
    }
    
    .btn-google:hover {
        background: #3367d6;
        border-color: #3367d6;
    }
    
    .btn-facebook {
        background: #1877f2;
        border-color: #1877f2;
        color: white;
    }
    
    .btn-facebook:hover {
        background: #166fe5;
        border-color: #166fe5;
    }
    
    /* Card Styles */
    .card-minimal {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .card-minimal:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Form Styles */
    .form-group {
        margin-bottom: 16px;
    }
    
    .form-label {
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 500;
        color: #495057;
        margin-bottom: 6px;
    }
    
    /* Status Indicators */
    .status-success { color: #28a745; }
    .status-warning { color: #ffc107; }
    .status-error { color: #dc3545; }
    .status-info { color: #17a2b8; }
    
    /* Document Upload Styles */
    .upload-area {
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        background: #f8f9fa;
        transition: all 0.2s ease;
    }
    
    .upload-area:hover {
        border-color: #4caf50;
        background: #e8f5e8;
    }
    
    /* Language Selector */
    .language-selector {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 12px;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        background: white;
        font-size: 14px;
    }
    
    /* Header Styles */
    .header-minimal {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 0;
        border-bottom: 1px solid #dee2e6;
        margin-bottom: 20px;
    }
    
    .header-title {
        font-size: 24px;
        font-weight: 600;
        color: #2e7d32;
        margin: 0;
    }
    
    /* Welcome Section */
    .welcome-section {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        border-radius: 12px;
        margin-bottom: 30px;
    }
    
    .welcome-title {
        font-size: 32px;
        font-weight: 700;
        color: #2e7d32;
        margin-bottom: 8px;
    }
    
    .welcome-subtitle {
        font-size: 16px;
        color: #4a5568;
        margin-bottom: 0;
    }
    
    /* Action Cards */
    .action-card {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    
    .action-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #4caf50;
    }
    
    .action-card-icon {
        font-size: 48px;
        color: #4caf50;
        margin-bottom: 16px;
    }
    
    .action-card-title {
        font-size: 18px;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 8px;
    }
    
    .action-card-description {
        font-size: 14px;
        color: #718096;
        line-height: 1.5;
    }
    
    /* Icon Styles */
    .icon-text {
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .icon-large {
        font-size: 24px;
    }
    
    .icon-medium {
        font-size: 18px;
    }
    
    .icon-small {
        font-size: 14px;
    }
    </style>
    """

# ============================================================================
# AUTHENTICATION UTILITIES
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    if 'language' not in st.session_state:
        st.session_state.language = 'English'
    
    if 'show_login_form' not in st.session_state:
        st.session_state.show_login_form = False

def authenticate_user(email, password):
    """Simulate user authentication"""
    if email and password:
        return {
            'id': str(uuid.uuid4()),
            'email': email,
            'first_name': email.split('@')[0].title(),
            'account_type': 'individual',
            'verified': True,
            'login_time': datetime.now()
        }
    return None

def oauth_login(provider):
    """Simulate OAuth login"""
    return {
        'id': str(uuid.uuid4()),
        'email': f'user@{provider.lower()}.com',
        'first_name': f'{provider} User',
        'account_type': 'individual',
        'verified': True,
        'oauth_provider': provider,
        'login_time': datetime.now()
    }

# ============================================================================
# TRANSLATION SYSTEM
# ============================================================================

TRANSLATIONS = {
    'English': {
        'welcome_title': 'Welcome to HAVEN',
        'welcome_subtitle': 'Empowering communities to support causes that matter',
        'get_started': 'Get Started',
        'existing_user': 'Existing User',
        'new_user': 'New User',
        'sign_in': 'Sign In',
        'create_account': 'Create Account',
        'email': 'Email',
        'password': 'Password',
        'login': 'Login',
        'register': 'Register',
        'home': 'Home',
        'campaign': 'Campaign',
        'explore': 'Explore',
        'search': 'Search',
        'profile': 'Profile',
        'logout': 'Logout',
        'language': 'Language',
        'individual': 'Individual',
        'organization': 'Organization',
        'full_name': 'Full Name',
        'phone': 'Phone Number',
        'confirm_password': 'Confirm Password',
        'organization_name': 'Organization Name',
        'organization_type': 'Organization Type',
        'registration_number': 'Registration Number',
        'description': 'Description',
        'pan_card': 'PAN Card',
        'aadhaar_card': 'Aadhaar Card',
        'bank_statement': 'Bank Statement',
        'address_proof': 'Address Proof',
        'registration_certificate': 'Registration Certificate',
        'tax_exemption': 'Tax Exemption Certificate',
        'financial_statements': 'Financial Statements',
        'board_resolution': 'Board Resolution',
        'fcra_certificate': 'FCRA Certificate',
        'upload_document': 'Upload Document',
        'required': 'Required',
        'optional': 'Optional',
        'terms_conditions': 'I agree to the Terms and Conditions',
        'kyc_consent': 'I consent to KYC verification',
        'data_processing': 'I agree to data processing',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'success': 'Success',
        'error': 'Error',
        'warning': 'Warning',
        'info': 'Information'
    },
    'हिंदी': {
        'welcome_title': 'HAVEN में आपका स्वागत है',
        'welcome_subtitle': 'समुदायों को महत्वपूर्ण कारणों का समर्थन करने के लिए सशक्त बनाना',
        'get_started': 'शुरू करें',
        'existing_user': 'मौजूदा उपयोगकर्ता',
        'new_user': 'नया उपयोगकर्ता',
        'sign_in': 'साइन इन करें',
        'create_account': 'खाता बनाएं',
        'email': 'ईमेल',
        'password': 'पासवर्ड',
        'login': 'लॉगिन',
        'register': 'पंजीकरण',
        'home': 'होम',
        'campaign': 'अभियान',
        'explore': 'खोजें',
        'search': 'खोज',
        'profile': 'प्रोफ़ाइल',
        'logout': 'लॉगआउट',
        'language': 'भाषा'
    },
    'தமிழ்': {
        'welcome_title': 'HAVEN இல் உங்களை வரவேற்கிறோம்',
        'welcome_subtitle': 'முக்கியமான காரணங்களை ஆதரிக்க சமூகங்களை அதிகாரப்படுத்துதல்',
        'get_started': 'தொடங்குங்கள்',
        'existing_user': 'ஏற்கனவே உள்ள பயனர்',
        'new_user': 'புதிய பயனர்',
        'sign_in': 'உள்நுழைக',
        'create_account': 'கணக்கை உருவாக்கவும்',
        'email': 'மின்னஞ்சல்',
        'password': 'கடவுச்சொல்',
        'login': 'உள்நுழைக',
        'register': 'பதிவு செய்யவும்',
        'home': 'முகப்பு',
        'campaign': 'பிரச்சாரம்',
        'explore': 'ஆராயுங்கள்',
        'search': 'தேடல்',
        'profile': 'சுயவிவரம்',
        'logout': 'வெளியேறு',
        'language': 'மொழி'
    },
    'తెలుగు': {
        'welcome_title': 'HAVEN కి స్వాగతం',
        'welcome_subtitle': 'ముఖ్యమైన కారణాలకు మద్దతు ఇవ్వడానికి కమ్యూనిటీలను శక్తివంతం చేయడం',
        'get_started': 'ప్రారంభించండి',
        'existing_user': 'ఇప్పటికే ఉన్న వినియోగదారు',
        'new_user': 'కొత్త వినియోగదారు',
        'sign_in': 'సైన్ ఇన్ చేయండి',
        'create_account': 'ఖాతా సృష్టించండి',
        'email': 'ఇమెయిల్',
        'password': 'పాస్‌వర్డ్',
        'login': 'లాగిన్',
        'register': 'నమోదు',
        'home': 'హోమ్',
        'campaign': 'ప్రచారం',
        'explore': 'అన్వేషించండి',
        'search': 'వెతకండి',
        'profile': 'ప్రొఫైల్',
        'logout': 'లాగ్ అవుట్',
        'language': 'భాష'
    }
}

def get_text(key, language='English'):
    """Get translated text"""
    return TRANSLATIONS.get(language, TRANSLATIONS['English']).get(key, key)

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_language_selector():
    """Render language selector with globe icon"""
    languages = ['English', 'हिंदी', 'தமிழ்', 'తెలుగు']
    
    st.markdown(f"""
    <div class="language-selector">
        <span style="font-size: 16px;">{icons.LANGUAGE}</span>
        <span>{get_text('language', st.session_state.language)}</span>
    </div>
    """, unsafe_allow_html=True)
    
    selected_language = st.selectbox(
        "",
        languages,
        index=languages.index(st.session_state.language),
        key="language_selector",
        label_visibility="collapsed"
    )
    
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

def render_navigation():
    """Render sidebar navigation with icons"""
    if not st.session_state.authenticated:
        return
    
    st.sidebar.markdown("### Navigation")
    
    nav_items = [
        ('home', icons.HOME, get_text('home', st.session_state.language)),
        ('campaign', icons.CAMPAIGN, get_text('campaign', st.session_state.language)),
        ('explore', icons.EXPLORE, get_text('explore', st.session_state.language)),
        ('search', icons.SEARCH, get_text('search', st.session_state.language)),
        ('profile', icons.PROFILE, get_text('profile', st.session_state.language))
    ]
    
    for page_key, icon, label in nav_items:
        is_active = st.session_state.current_page == page_key
        
        if is_active:
            st.sidebar.markdown(f"""
            <div class="nav-item active">
                <span style="font-size: 18px;">{icon}</span>
                <span>{label}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.sidebar.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
    
    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button(f"{icons.LOGOUT} {get_text('logout', st.session_state.language)}", key="logout_btn", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_data = {}
        st.session_state.current_page = 'login'
        st.rerun()

def render_social_login_button(provider, icon, btn_class):
    """Render social login button with icon"""
    if st.button(f"{icon} Continue with {provider}", key=f"{provider.lower()}_login", use_container_width=True):
        user_data = oauth_login(provider)
        if user_data:
            st.session_state.authenticated = True
            st.session_state.user_data = user_data
            st.session_state.current_page = 'home'
            st.success(f"Successfully logged in with {provider}!")
            time.sleep(1)
            st.rerun()

def render_document_upload_section(title, icon, required=True, help_text=""):
    """Render document upload section with icon"""
    status_text = get_text('required', st.session_state.language) if required else get_text('optional', st.session_state.language)
    status_color = "#dc3545" if required else "#6c757d"
    
    st.markdown(f"""
    <div class="form-label">
        <span style="font-size: 16px; color: #4caf50;">{icon}</span>
        <span>{title}</span>
        <span style="color: {status_color}; font-size: 12px;">({status_text})</span>
    </div>
    """, unsafe_allow_html=True)
    
    if help_text:
        st.markdown(f"<small style='color: #6c757d;'>{help_text}</small>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        key=f"upload_{title.lower().replace(' ', '_')}",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # Size in MB
        if file_size > 5:
            st.error(f"{icons.ERROR} File size exceeds 5MB limit")
        else:
            st.success(f"{icons.SUCCESS} {uploaded_file.name} uploaded successfully ({file_size:.1f}MB)")
    
    return uploaded_file

# ============================================================================
# PAGE COMPONENTS
# ============================================================================

def render_login_page():
    """Render login page with icons"""
    # Welcome section
    st.markdown(f"""
    <div class="welcome-section">
        <div class="welcome-title">
            <span style="font-size: 32px; margin-right: 10px;">{icons.HOME}</span>
            {get_text('welcome_title', st.session_state.language)}
        </div>
        <p class="welcome-subtitle">{get_text('welcome_subtitle', st.session_state.language)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selector
    render_language_selector()
    
    # Get Started section
    st.markdown(f"""
    <div class="header-minimal">
        <span style="font-size: 24px; color: #4caf50;">{icons.LOGIN}</span>
        <h2 class="header-title">{get_text('get_started', st.session_state.language)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="action-card">
            <div class="action-card-icon">
                <span style="font-size: 48px;">{icons.LOGIN}</span>
            </div>
            <div class="action-card-title">{get_text('existing_user', st.session_state.language)}</div>
            <div class="action-card-description">Sign in to your existing account</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(get_text('sign_in', st.session_state.language), key="show_login", use_container_width=True):
            st.session_state.show_login_form = True
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="action-card">
            <div class="action-card-icon">
                <span style="font-size: 48px;">{icons.REGISTER}</span>
            </div>
            <div class="action-card-title">{get_text('new_user', st.session_state.language)}</div>
            <div class="action-card-description">Create a new account to get started</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(get_text('create_account', st.session_state.language), key="show_register", use_container_width=True):
            st.session_state.current_page = 'register'
            st.rerun()
    
    # Show login form if requested
    if st.session_state.get('show_login_form', False):
        st.markdown("---")
        render_login_form()

def render_login_form():
    """Render login form with icons"""
    st.markdown(f"""
    <div class="header-minimal">
        <span style="font-size: 20px; color: #4caf50;">{icons.LOGIN}</span>
        <h3 style="margin: 0; color: #2e7d32;">{get_text('sign_in', st.session_state.language)}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        # Email field
        st.markdown(f"""
        <div class="form-label">
            <span style="font-size: 16px; color: #4caf50;">{icons.EMAIL}</span>
            <span>{get_text('email', st.session_state.language)}</span>
        </div>
        """, unsafe_allow_html=True)
        email = st.text_input("", placeholder="your.email@example.com", key="login_email", label_visibility="collapsed")
        
        # Password field
        st.markdown(f"""
        <div class="form-label">
            <span style="font-size: 16px; color: #4caf50;">{icons.LOCK}</span>
            <span>{get_text('password', st.session_state.language)}</span>
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input("", type="password", placeholder="Enter your password", key="login_password", label_visibility="collapsed")
        
        # Login button
        if st.form_submit_button(get_text('login', st.session_state.language), use_container_width=True):
            if email and password:
                user_data = authenticate_user(email, password)
                if user_data:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.current_page = 'home'
                    st.success(f"{icons.SUCCESS} Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"{icons.ERROR} Invalid credentials")
            else:
                st.error(f"{icons.WARNING} Please fill in all fields")
    
    # Social login options
    st.markdown("---")
    st.markdown("**Or continue with:**")
    
    col1, col2 = st.columns(2)
    with col1:
        render_social_login_button("Google", icons.GOOGLE, "btn-google")
    with col2:
        render_social_login_button("Facebook", icons.FACEBOOK, "btn-facebook")

def render_register_page():
    """Render registration page with icons"""
    st.markdown(f"""
    <div class="welcome-section">
        <div class="welcome-title">
            <span style="font-size: 32px; margin-right: 10px;">{icons.REGISTER}</span>
            {get_text('create_account', st.session_state.language)}
        </div>
        <p class="welcome-subtitle">Help not just some people, but Help Humanity</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Account type selection
    st.markdown(f"""
    <div class="header-minimal">
        <span style="font-size: 20px; color: #4caf50;">{icons.PERSON}</span>
        <h3 style="margin: 0; color: #2e7d32;">Account Type</h3>
    </div>
    """, unsafe_allow_html=True)
    
    account_type = st.radio(
        "",
        ["Individual", "Organization"],
        key="account_type",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if account_type == "Individual":
        render_individual_registration()
    else:
        render_organization_registration()

def render_individual_registration():
    """Render individual registration form with icons"""
    st.markdown(f"""
    <div class="header-minimal">
        <span style="font-size: 20px; color: #4caf50;">{icons.PERSON}</span>
        <h4 style="margin: 0; color: #2e7d32;">Individual Account Registration</h4>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("individual_register"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Full Name
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.PERSON}</span>
                <span>{get_text('full_name', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            full_name = st.text_input("", placeholder="Enter your full name", key="ind_full_name", label_visibility="collapsed")
            
            # Email
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.EMAIL}</span>
                <span>{get_text('email', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            email = st.text_input("", placeholder="your.email@example.com", key="ind_email", label_visibility="collapsed")
            
            # Password
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.LOCK}</span>
                <span>{get_text('password', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            password = st.text_input("", type="password", placeholder="Create a strong password", key="ind_password", label_visibility="collapsed")
        
        with col2:
            # Phone
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.PHONE}</span>
                <span>{get_text('phone', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            phone = st.text_input("", placeholder="+91 9876543210", key="ind_phone", label_visibility="collapsed")
            
            # Confirm Password
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.LOCK}</span>
                <span>{get_text('confirm_password', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            confirm_password = st.text_input("", type="password", placeholder="Confirm your password", key="ind_confirm_password", label_visibility="collapsed")
        
        # Document verification section
        st.markdown("---")
        st.markdown(f"""
        <div class="header-minimal">
            <span style="font-size: 20px; color: #4caf50;">{icons.VERIFICATION}</span>
            <h4 style="margin: 0; color: #2e7d32;">Document Verification</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            pan_card = render_document_upload_section(
                get_text('pan_card', st.session_state.language),
                icons.CERTIFICATE,
                required=True,
                help_text="Government-issued PAN card for tax identification"
            )
            
            bank_statement = render_document_upload_section(
                get_text('bank_statement', st.session_state.language),
                icons.DOCUMENT,
                required=False,
                help_text="Recent 3-month bank statement (optional)"
            )
        
        with col2:
            aadhaar_card = render_document_upload_section(
                get_text('aadhaar_card', st.session_state.language),
                icons.CERTIFICATE,
                required=True,
                help_text="Aadhaar card for identity verification"
            )
            
            address_proof = render_document_upload_section(
                get_text('address_proof', st.session_state.language),
                icons.DOCUMENT,
                required=False,
                help_text="Utility bill or rental agreement (optional)"
            )
        
        # Consent checkboxes
        st.markdown("---")
        terms_accepted = st.checkbox(f"{icons.VERIFICATION} {get_text('terms_conditions', st.session_state.language)}")
        kyc_consent = st.checkbox(f"{icons.SHIELD} {get_text('kyc_consent', st.session_state.language)}")
        data_consent = st.checkbox(f"{icons.SECURITY} {get_text('data_processing', st.session_state.language)}")
        
        # Submit button
        if st.form_submit_button(get_text('register', st.session_state.language), use_container_width=True):
            if all([full_name, email, password, phone, confirm_password, pan_card, aadhaar_card, terms_accepted, kyc_consent, data_consent]):
                if password == confirm_password:
                    # Create user account
                    user_data = {
                        'id': str(uuid.uuid4()),
                        'email': email,
                        'first_name': full_name.split()[0],
                        'full_name': full_name,
                        'phone': phone,
                        'account_type': 'individual',
                        'verified': False,
                        'registration_time': datetime.now()
                    }
                    
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.current_page = 'home'
                    st.success(f"{icons.SUCCESS} Registration successful! Your documents are under review.")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"{icons.ERROR} Passwords do not match")
            else:
                st.error(f"{icons.WARNING} Please fill in all required fields and upload required documents")

def render_organization_registration():
    """Render organization registration form with icons"""
    st.markdown(f"""
    <div class="header-minimal">
        <span style="font-size: 20px; color: #4caf50;">{icons.BUILDING}</span>
        <h4 style="margin: 0; color: #2e7d32;">Organization Account Registration</h4>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("organization_register"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Organization Name
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.BUILDING}</span>
                <span>{get_text('organization_name', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            org_name = st.text_input("", placeholder="Enter organization name", key="org_name", label_visibility="collapsed")
            
            # Organization Type
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.TAG}</span>
                <span>{get_text('organization_type', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            org_type = st.selectbox("", ["", "NGO", "Startup", "Charity", "Foundation", "Trust"], key="org_type", label_visibility="collapsed")
            
            # Contact Email
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.EMAIL}</span>
                <span>{get_text('email', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            email = st.text_input("", placeholder="organization@example.com", key="org_email", label_visibility="collapsed")
        
        with col2:
            # Registration Number
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.CERTIFICATE}</span>
                <span>{get_text('registration_number', st.session_state.language)}</span>
            </div>
            """, unsafe_allow_html=True)
            reg_number = st.text_input("", placeholder="Official registration number", key="org_reg_number", label_visibility="collapsed")
            
            # Contact Phone
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.PHONE}</span>
                <span>{get_text('phone', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            phone = st.text_input("", placeholder="+91 9876543210", key="org_phone", label_visibility="collapsed")
            
            # Password
            st.markdown(f"""
            <div class="form-label">
                <span style="font-size: 16px; color: #4caf50;">{icons.LOCK}</span>
                <span>{get_text('password', st.session_state.language)} *</span>
            </div>
            """, unsafe_allow_html=True)
            password = st.text_input("", type="password", placeholder="Create a strong password", key="org_password", label_visibility="collapsed")
        
        # Description
        st.markdown(f"""
        <div class="form-label">
            <span style="font-size: 16px; color: #4caf50;">{icons.DOCUMENT}</span>
            <span>{get_text('description', st.session_state.language)} *</span>
        </div>
        """, unsafe_allow_html=True)
        description = st.text_area("", placeholder="Describe your organization's mission and activities", key="org_description", label_visibility="collapsed")
        
        # Document verification section
        st.markdown("---")
        st.markdown(f"""
        <div class="header-minimal">
            <span style="font-size: 20px; color: #4caf50;">{icons.VERIFICATION}</span>
            <h4 style="margin: 0; color: #2e7d32;">Organization Documents</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            reg_certificate = render_document_upload_section(
                get_text('registration_certificate', st.session_state.language),
                icons.CERTIFICATE,
                required=True,
                help_text="Society Registration, Trust Deed, or Company Incorporation"
            )
            
            org_pan = render_document_upload_section(
                "Organization PAN Card",
                icons.CERTIFICATE,
                required=True,
                help_text="PAN card issued in organization's name"
            )
            
            financial_statements = render_document_upload_section(
                get_text('financial_statements', st.session_state.language),
                icons.CHART,
                required=False,
                help_text="Audited financial statements (last 2 years)"
            )
        
        with col2:
            tax_exemption = render_document_upload_section(
                get_text('tax_exemption', st.session_state.language),
                icons.CERTIFICATE,
                required=True,
                help_text="12A/80G certificate for NGOs or relevant tax documents"
            )
            
            board_resolution = render_document_upload_section(
                get_text('board_resolution', st.session_state.language),
                icons.DOCUMENT,
                required=False,
                help_text="Board resolution authorizing contact person"
            )
            
            fcra_certificate = render_document_upload_section(
                get_text('fcra_certificate', st.session_state.language),
                icons.CERTIFICATE,
                required=False,
                help_text="For NGOs receiving foreign contributions"
            )
        
        # Consent checkboxes
        st.markdown("---")
        terms_accepted = st.checkbox(f"{icons.VERIFICATION} {get_text('terms_conditions', st.session_state.language)}")
        kyc_consent = st.checkbox(f"{icons.SHIELD} {get_text('kyc_consent', st.session_state.language)}")
        data_consent = st.checkbox(f"{icons.SECURITY} {get_text('data_processing', st.session_state.language)}")
        
        # Submit button
        if st.form_submit_button(get_text('register', st.session_state.language), use_container_width=True):
            if all([org_name, org_type, email, phone, password, description, reg_certificate, tax_exemption, org_pan, terms_accepted, kyc_consent, data_consent]):
                # Create organization account
                user_data = {
                    'id': str(uuid.uuid4()),
                    'email': email,
                    'organization_name': org_name,
                    'organization_type': org_type,
                    'phone': phone,
                    'description': description,
                    'registration_number': reg_number,
                    'account_type': 'organization',
                    'verified': False,
                    'registration_time': datetime.now()
                }
                
                st.session_state.authenticated = True
                st.session_state.user_data = user_data
                st.session_state.current_page = 'home'
                st.success(f"{icons.SUCCESS} Organization registration successful! Your documents are under review.")
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"{icons.WARNING} Please fill in all required fields and upload required documents")

def render_home_page():
    """Render home dashboard with icons"""
    user_data = st.session_state.user_data
    
    # Welcome header
    account_type = user_data.get('account_type', 'individual')
    display_name = user_data.get('organization_name') if account_type == 'organization' else user_data.get('first_name', 'User')
    
    st.markdown(f"""
    <div class="welcome-section">
        <div class="welcome-title">
            <span style="font-size: 32px; margin-right: 10px;">{icons.HOME}</span>
            Welcome back, {display_name}!
        </div>
        <p class="welcome-subtitle">Your impact dashboard and quick actions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown(f"""
    <div class="header-minimal">
        <span style="font-size: 20px; color: #4caf50;">⚡</span>
        <h3 style="margin: 0; color: #2e7d32;">Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="action-card">
            <div class="action-card-icon">
                <span style="font-size: 48px;">{icons.CAMPAIGN}</span>
            </div>
            <div class="action-card-title">Create Campaign</div>
            <div class="action-card-description">Start a new fundraising campaign</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Create Campaign", key="create_campaign", use_container_width=True):
            st.session_state.current_page = 'campaign'
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="action-card">
            <div class="action-card-icon">
                <span style="font-size: 48px;">{icons.EXPLORE}</span>
            </div>
            <div class="action-card-title">Browse Campaigns</div>
            <div class="action-card-description">Discover causes to support</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Browse Campaigns", key="browse_campaigns", use_container_width=True):
            st.session_state.current_page = 'explore'
            st.rerun()
    
    with col3:
        st.markdown(f"""
        <div class="action-card">
            <div class="action-card-icon">
                <span style="font-size: 48px;">{icons.HEART}</span>
            </div>
            <div class="action-card-title">Make Donation</div>
            <div class="action-card-description">Support a cause directly</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Make Donation", key="make_donation", use_container_width=True):
            st.session_state.current_page = 'search'
            st.rerun()
    
    # User stats
    st.markdown("---")
    st.markdown(f"""
    <div class="header-minimal">
        <span style="font-size: 20px; color: #4caf50;">{icons.CHART}</span>
        <h3 style="margin: 0; color: #2e7d32;">Your Impact</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=f"{icons.CAMPAIGN} Campaigns Created",
            value="0",
            delta="Start your first campaign"
        )
    
    with col2:
        st.metric(
            label=f"{icons.MONEY} Total Raised",
            value="₹0",
            delta="Begin fundraising"
        )
    
    with col3:
        st.metric(
            label=f"{icons.HEART} Donations Made",
            value="0",
            delta="Support a cause"
        )
    
    with col4:
        st.metric(
            label=f"{icons.STAR} Impact Score",
            value="0",
            delta="Build your reputation"
        )

def render_other_pages():
    """Render placeholder pages with icons"""
    page_configs = {
        'campaign': {
            'icon': icons.CAMPAIGN,
            'title': 'Campaign Management',
            'description': 'Create and manage your fundraising campaigns'
        },
        'explore': {
            'icon': icons.EXPLORE,
            'title': 'Explore Campaigns',
            'description': 'Discover and browse active campaigns'
        },
        'search': {
            'icon': icons.SEARCH,
            'title': 'Search & Filter',
            'description': 'Find specific campaigns and causes'
        },
        'profile': {
            'icon': icons.PROFILE,
            'title': 'User Profile',
            'description': 'Manage your account and settings'
        }
    }
    
    current_page = st.session_state.current_page
    config = page_configs.get(current_page, {})
    
    st.markdown(f"""
    <div class="welcome-section">
        <div class="welcome-title">
            <span style="font-size: 32px; margin-right: 10px;">{config.get('icon', icons.INFO)}</span>
            {config.get('title', 'Page')}
        </div>
        <p class="welcome-subtitle">{config.get('description', 'Page description')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"{icons.INFO} This page is under development. Full functionality will be available soon.")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="HAVEN - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load clean CSS
    st.markdown(get_clean_css(), unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Render navigation (only if authenticated)
    render_navigation()
    
    # Main content area
    if not st.session_state.authenticated:
        if st.session_state.current_page == 'register':
            render_register_page()
        else:
            render_login_page()
    else:
        if st.session_state.current_page == 'home':
            render_home_page()
        else:
            render_other_pages()

if __name__ == "__main__":
    main()

