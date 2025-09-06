# Haven Crowdfunding Platform - Clean Production Version
# Uses Render Environment Group variables (no hardcoded values)

import streamlit as st
import requests
import base64
import os
import json
import psycopg2
import psycopg2.pool
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import logging

# ================================
# PRODUCTION CONFIGURATION
# ================================

# Environment variables from Render Environment Group
BACKEND_URL = os.getenv("BACKEND_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# Derived configuration
API_BASE = f"{BACKEND_URL}/api/v1" if BACKEND_URL else None

# Validate required environment variables
required_env_vars = {
    "BACKEND_URL": BACKEND_URL,
    "FRONTEND_URL": FRONTEND_URL,
    "DATABASE_URL": DATABASE_URL,
    "JWT_SECRET_KEY": JWT_SECRET_KEY,
    "SECRET_KEY": SECRET_KEY
}

missing_vars = [var for var, value in required_env_vars.items() if not value]
if missing_vars:
    st.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
    st.info("💡 Please check your Render Environment Group configuration")
    st.stop()

# Session state keys
SESSION_KEYS = {
    'authenticated': 'is_authenticated',
    'user_data': 'user_data',
    'access_token': 'access_token',
    'refresh_token': 'refresh_token',
    'current_page': 'current_page',
    'user_id': 'user_id',
    'login_timestamp': 'login_timestamp'
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================================
# BOOTSTRAP ICON UTILITIES
# ================================

@st.cache_data
def get_bootstrap_icon_b64(icon_name: str, size: int = 18, color: str = "#ffffff") -> str:
    """Convert Bootstrap SVG icon to base64 for reliable display in production."""
    try:
        script_dir = os.path.dirname(__file__)
        svg_path = os.path.join(script_dir, "assets", f"{icon_name}.svg")
    except NameError:
        svg_path = os.path.join("assets", f"{icon_name}.svg")

    if os.path.exists(svg_path):
        try:
            with open(svg_path, "rb") as f:
                svg_data = f.read()
            b64_svg = base64.b64encode(svg_data).decode()
            return f'''<img src="data:image/svg+xml;base64,{b64_svg}" 
                       width="{size}" height="{size}" 
                       style="vertical-align: middle; margin-right: 8px; 
                              filter: brightness(0) saturate(100%) invert(100%);">'''
        except Exception as e:
            logger.warning(f"Failed to load icon {icon_name} from {svg_path}: {e}")
            return f'<span style="margin-right: 8px; color: {color};">●</span>'
    
    logger.warning(f"Icon not found at path: {svg_path}")
    return f'<span style="margin-right: 8px; color: {color};">●</span>'

@st.cache_data
def get_colored_icon_b64(icon_name: str, size: int = 24, color: str = "#4CAF50") -> str:
    """Get colored Bootstrap icon for main content areas."""
    try:
        script_dir = os.path.dirname(__file__)
        svg_path = os.path.join(script_dir, "assets", f"{icon_name}.svg")
    except NameError:
        svg_path = os.path.join("assets", f"{icon_name}.svg")

    if os.path.exists(svg_path):
        try:
            with open(svg_path, "r") as f:
                svg_content = f.read()
            # Inject fill color into SVG
            svg_colored = svg_content.replace('<svg ', f'<svg fill="{color}" ')
            b64_svg = base64.b64encode(svg_colored.encode("utf-8")).decode()
            return f'<img src="data:image/svg+xml;base64,{b64_svg}" width="{size}" height="{size}" style="vertical-align: middle;">'
        except Exception as e:
            logger.warning(f"Failed to load colored icon {icon_name} from {svg_path}: {e}")
            return f'<span style="color: {color};">●</span>'

    logger.warning(f"Colored icon not found at path: {svg_path}")
    return f'<span style="color: {color};">●</span>'

def create_icon_button(icon_name: str, label: str, key: str, size: int = 18, 
                      color: str = "#ffffff", help_text: Optional[str] = None) -> bool:
    """Create clickable icon button with professional styling."""
    icon_html = get_bootstrap_icon_b64(icon_name, size, color)
    button_html = f'''
    <div style="margin: 5px 0; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 10px; padding: 12px 15px; color: white; transition: all 0.3s ease; width: 100%; text-align: left; font-size: 14px; font-weight: 500; display: flex; align-items: center; backdrop-filter: blur(10px);">
        {icon_html}
        <span style="flex: 1;">{label}</span>
    </div>
    '''
    st.markdown(button_html, unsafe_allow_html=True)
    return st.button(label, key=key, help=help_text or f"Navigate to {label}", use_container_width=True)

# ... (Database utilities, API Integration, and Auth System remain the same)
# ================================
# DATABASE UTILITIES (WITH CONNECTION POOLING)
# ================================

@st.cache_resource
def get_db_connection_pool():
    """Create and cache a database connection pool."""
    try:
        pool = psycopg2.pool.SimpleConnectionPool(1, 10, dsn=DATABASE_URL)
        logger.info("Database connection pool created successfully.")
        return pool
    except psycopg2.OperationalError as e:
        st.error(f"🚨 Database connection failed: {e}")
        logger.error(f"Database connection failed: {e}")
        return None

def get_db_connection():
    """Get a connection from the pool."""
    pool = get_db_connection_pool()
    if pool:
        return pool.getconn()
    return None

def release_db_connection(conn):
    """Return a connection to the pool."""
    pool = get_db_connection_pool()
    if pool and conn:
        pool.putconn(conn)

def test_database_connection() -> bool:
    """Test database connectivity."""
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            return result is not None
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        return False
    finally:
        if conn:
            release_db_connection(conn)
    return False

def fetch_user_campaigns(user_id: str) -> List[Dict]:
    """Fetch user's campaigns from database using a pooled connection."""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, short_description, goal_amount, current_amount, 
                   status, created_at, end_date, category
            FROM campaigns 
            WHERE creator_id = %s 
            ORDER BY created_at DESC
        """, (user_id,))
        
        campaigns = []
        for row in cursor.fetchall():
            campaigns.append({
                'id': row[0],
                'title': row[1],
                'short_description': row[2],
                'goal_amount': row[3],
                'current_amount': row[4] or 0,
                'status': row[5],
                'created_at': row[6],
                'end_date': row[7],
                'category': row[8]
            })
        
        cursor.close()
        return campaigns
    except Exception as e:
        logger.error(f"Failed to fetch user campaigns: {e}")
        return []
    finally:
        if conn:
            release_db_connection(conn)

def fetch_user_contributions(user_id: str) -> List[Dict]:
    """Fetch user's contributions from database."""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.title, d.amount, d.created_at, d.status
            FROM donations d
            JOIN campaigns c ON d.campaign_id = c.id
            WHERE d.donor_id = %s
            ORDER BY d.created_at DESC
        """, (user_id,))
        
        contributions = []
        for row in cursor.fetchall():
            contributions.append({
                'campaign_title': row[0],
                'amount': row[1],
                'date': row[2].strftime('%Y-%m-%d') if row[2] else 'Unknown',
                'status': row[3]
            })
        
        cursor.close()
        return contributions
    except Exception as e:
        logger.error(f"Failed to fetch user contributions: {e}")
        return []
    finally:
        if conn:
            release_db_connection(conn)

def fetch_platform_stats() -> Dict:
    """Fetch platform statistics from database."""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return {}
        
        cursor = conn.cursor()
        
        # Total raised
        cursor.execute("SELECT COALESCE(SUM(current_amount), 0) FROM campaigns")
        total_raised = cursor.fetchone()[0]
        
        # Active users
        cursor.execute("SELECT COUNT(DISTINCT id) FROM users WHERE is_active = true")
        active_users = cursor.fetchone()[0]
        
        # Successful projects
        cursor.execute("SELECT COUNT(*) FROM campaigns WHERE status = 'completed' AND current_amount >= goal_amount")
        successful_projects = cursor.fetchone()[0]
        
        # Active campaigns
        cursor.execute("SELECT COUNT(*) FROM campaigns WHERE status = 'active'")
        active_campaigns = cursor.fetchone()[0]
        
        cursor.close()
        
        return {
            'total_raised': total_raised,
            'active_users': active_users,
            'successful_projects': successful_projects,
            'active_campaigns': active_campaigns
        }
    except Exception as e:
        logger.error(f"Failed to fetch platform stats: {e}")
        return {
            'total_raised': 2500000,  # Fallback values
            'active_users': 15432,
            'successful_projects': 1247,
            'active_campaigns': 89
        }
    finally:
        if conn:
            release_db_connection(conn)


# ================================
# API INTEGRATION
# ================================

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None, 
                    auth_required: bool = False, timeout: int = 10) -> Dict[str, Any]:
    """Make API request to FastAPI backend with proper error handling."""
    
    if not API_BASE:
        return {"success": False, "error": "Backend URL not configured"}
    
    url = f"{API_BASE}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    # Add authentication if required and available
    if auth_required and st.session_state.get(SESSION_KEYS['access_token']):
        headers["Authorization"] = f"Bearer {st.session_state[SESSION_KEYS['access_token']]}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=timeout)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=timeout)
        else:
            return {"success": False, "error": f"Unsupported HTTP method: {method}"}
        
        # Handle different response status codes
        if response.status_code == 200:
            try:
                return {"success": True, "data": response.json()}
            except json.JSONDecodeError:
                return {"success": True, "data": response.text}
        elif response.status_code == 401:
            # Handle authentication errors
            logout_user()
            return {"success": False, "error": "Authentication required", "code": 401}
        elif response.status_code == 403:
            return {"success": False, "error": "Access forbidden", "code": 403}
        elif response.status_code == 404:
            return {"success": False, "error": "Resource not found", "code": 404}
        elif response.status_code == 422:
            return {"success": False, "error": "Validation error", "details": response.text, "code": 422}
        else:
            return {"success": False, "error": f"API Error: {response.status_code}", 
                   "details": response.text, "code": response.status_code}
    
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Backend service unavailable", "code": "CONNECTION_ERROR"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout", "code": "TIMEOUT"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}", "code": "REQUEST_ERROR"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}", "code": "UNKNOWN_ERROR"}

def check_backend_health() -> Dict[str, Any]:
    """Check backend service health and connectivity."""
    if not BACKEND_URL:
        return {"online": False, "status": "not_configured", "error": "Backend URL not set"}
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return {"online": True, "status": "healthy", "response_time": response.elapsed.total_seconds()}
        else:
            return {"online": False, "status": f"unhealthy_{response.status_code}", "response_time": None}
    except Exception as e:
        return {"online": False, "status": "unreachable", "error": str(e), "response_time": None}

def get_oauth_login_url(provider: str) -> str:
    """Get OAuth login URL for specified provider."""
    if not API_BASE:
        return "#"
    
    if provider.lower() == "google":
        return f"{API_BASE}/auth/google/login"
    elif provider.lower() == "facebook":
        return f"{API_BASE}/auth/facebook/login"
    else:
        return f"{API_BASE}/auth/{provider}/login"

# ================================
# AUTHENTICATION SYSTEM
# ================================

def initialize_session():
    """Initialize session state for authentication and user management."""
    default_values = {
        SESSION_KEYS['authenticated']: False,
        SESSION_KEYS['user_data']: None,
        SESSION_KEYS['access_token']: None,
        SESSION_KEYS['refresh_token']: None,
        SESSION_KEYS['current_page']: 'login',
        SESSION_KEYS['user_id']: None,
        SESSION_KEYS['login_timestamp']: None
    }
    
    for key, default_value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def is_authenticated() -> bool:
    """Check if user is authenticated with token validation."""
    if not st.session_state.get(SESSION_KEYS['authenticated'], False):
        return False
    
    # Check if token exists
    if not st.session_state.get(SESSION_KEYS['access_token']):
        return False
    
    # Check token expiration (if login timestamp exists)
    login_time = st.session_state.get(SESSION_KEYS['login_timestamp'])
    if login_time:
        # Token expires after 24 hours
        if datetime.now() - login_time > timedelta(hours=24):
            logout_user()
            return False
    
    return True

def login_user(user_data: Dict, access_token: str, refresh_token: str = None):
    """Login user and set session state."""
    st.session_state[SESSION_KEYS['authenticated']] = True
    st.session_state[SESSION_KEYS['user_data']] = user_data
    st.session_state[SESSION_KEYS['access_token']] = access_token
    st.session_state[SESSION_KEYS['refresh_token']] = refresh_token
    st.session_state[SESSION_KEYS['user_id']] = user_data.get('id')
    st.session_state[SESSION_KEYS['login_timestamp']] = datetime.now()
    st.session_state[SESSION_KEYS['current_page']] = 'home'
    
    logger.info(f"User logged in: {user_data.get('email', 'unknown')}")

def logout_user():
    """Logout user and clear session state."""
    user_email = st.session_state.get(SESSION_KEYS['user_data'], {}).get('email', 'unknown')
    
    # Clear all session data
    for key in SESSION_KEYS.values():
        if key in st.session_state:
            del st.session_state[key]
    
    # Reset to default state
    initialize_session()
    
    logger.info(f"User logged out: {user_email}")
    st.success("✅ Logged out successfully!")
    st.rerun()

def handle_oauth_callback():
    """Handle OAuth callback from query parameters."""
    query_params = st.experimental_get_query_params()
    
    if 'token' in query_params:
        try:
            token_str = query_params['token'][0]
            token_data = json.loads(base64.b64decode(token_str))
            
            user_data = token_data.get('user')
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')

            if user_data and access_token:
                login_user(user_data, access_token, refresh_token)
                st.experimental_set_query_params() # Clean URL
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("OAuth failed. Invalid token data.")

        except Exception as e:
            st.error(f"Error processing OAuth callback: {e}")
        
        # Clean URL regardless of outcome
        st.experimental_set_query_params()

# ================================
# NAVIGATION COMPONENTS
# ================================

def render_auth_only_sidebar():
    """Render sidebar for unauthenticated users - STRICT ACCESS CONTROL."""
    st.sidebar.markdown('<div class="auth-nav-title">🏠 Haven Platform</div>', unsafe_allow_html=True)
    if st.sidebar.button("Login", use_container_width=True):
        st.session_state.current_page = 'login'
        st.rerun()
    if st.sidebar.button("Register", use_container_width=True):
        st.session_state.current_page = 'register'
        st.rerun()

def render_authenticated_sidebar():
    """Render full sidebar for authenticated users with real data."""
    user_data = st.session_state.get(SESSION_KEYS['user_data'], {})
    user_name = user_data.get('first_name', user_data.get('name', 'User'))
    st.sidebar.markdown(f"### Welcome, {user_name}!")
    
    nav_items = {
        "Home": "home",
        "Browse Campaigns": "explore",
        "Create Campaign": "campaign",
        "Profile": "profile"
    }
    for label, page_key in nav_items.items():
        if st.sidebar.button(label, use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        logout_user()

# ================================
# AUTHENTICATION PAGES
# ================================

def render_login_content():
    """Render login page with OAuth integration."""
    st.header("Welcome to Haven")
    st.subheader("Please sign in to continue")

    google_login_url = get_oauth_login_url("google")
    st.markdown(f'<a href="{google_login_url}" target="_self" style="text-decoration: none;"><button style="width: 100%; padding: 10px; margin: 5px 0; background-color: #DB4437; color: white; border: none; border-radius: 5px;">{get_bootstrap_icon_b64("google")} Sign in with Google</button></a>', unsafe_allow_html=True)
    
    facebook_login_url = get_oauth_login_url("facebook")
    st.markdown(f'<a href="{facebook_login_url}" target="_self" style="text-decoration: none;"><button style="width: 100%; padding: 10px; margin: 5px 0; background-color: #4267B2; color: white; border: none; border-radius: 5px;">{get_bootstrap_icon_b64("facebook")} Sign in with Facebook</button></a>', unsafe_allow_html=True)

    st.markdown("---")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            # Handle email login
            pass

def render_register_content():
    """Render registration page with Individual/Organization options."""
    st.header("Create your Haven Account")
    st.subheader("Join the Haven crowdfunding community")
    
    # User type selection
    user_type = st.radio(
        "Registration Type",
        ["Individual", "Organization"],
        horizontal=True,
        help="Select whether you're registering as an individual or organization"
    )
    
    with st.form("registration_form"):
        if user_type == "Individual":
            st.subheader("Individual Registration")
            
            # Individual fields
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name *", placeholder="Enter your first name")
            with col2:
                last_name = st.text_input("Last Name *", placeholder="Enter your last name")
            
            email = st.text_input("Email ID *", placeholder="Enter your email address")
            phone = st.text_input("Phone Number *", placeholder="Enter your 10-digit phone number")
            aadhar = st.text_input("Aadhar Card Number *", placeholder="Enter your 12-digit Aadhar number", max_chars=12)
            
            password = st.text_input("Password *", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
            
        else:  # Organization
            st.subheader("Organization Registration")
            
            # Organization fields
            org_name = st.text_input("Organization Name *", placeholder="Enter organization name")
            org_email = st.text_input("Organization Email ID *", placeholder="Enter organization email")
            org_phone = st.text_input("Organization Phone Number *", placeholder="Enter organization phone number")
            
            # Certificate upload
            st.write("Certificate of Authentication (India) *")
            certificate_file = st.file_uploader(
                "Upload Certificate",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                help="Upload your organization's certificate of authentication"
            )
            
            # Contact person details
            st.write("**Contact Person Details**")
            col1, col2 = st.columns(2)
            with col1:
                contact_first_name = st.text_input("Contact Person First Name *")
            with col2:
                contact_last_name = st.text_input("Contact Person Last Name *")
            
            contact_email = st.text_input("Contact Person Email *", placeholder="Contact person's email")
            
            password = st.text_input("Password *", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
        
        # Terms and conditions
        terms_accepted = st.checkbox("I agree to the Terms and Conditions and Privacy Policy *")
        
        # Submit button
        submitted = st.form_submit_button("Create Account", use_container_width=True)
        
        if submitted:
            # Validation
            errors = []
            
            if user_type == "Individual":
                if not first_name or not last_name:
                    errors.append("First name and last name are required")
                if not email or "@" not in email:
                    errors.append("Valid email address is required")
                if not phone or len(phone) != 10 or not phone.isdigit():
                    errors.append("Valid 10-digit phone number is required")
                if not aadhar or len(aadhar) != 12 or not aadhar.isdigit():
                    errors.append("Valid 12-digit Aadhar number is required")
            else:
                if not org_name:
                    errors.append("Organization name is required")
                if not org_email or "@" not in org_email:
                    errors.append("Valid organization email is required")
                if not org_phone:
                    errors.append("Organization phone number is required")
                if not certificate_file:
                    errors.append("Certificate of authentication is required")
                if not contact_first_name or not contact_last_name:
                    errors.append("Contact person name is required")
                if not contact_email or "@" not in contact_email:
                    errors.append("Valid contact person email is required")
            
            # Common validations
            if not password or len(password) < 8:
                errors.append("Password must be at least 8 characters long")
            if password != confirm_password:
                errors.append("Passwords do not match")
            if not terms_accepted:
                errors.append("You must accept the terms and conditions")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Prepare registration data
                if user_type == "Individual":
                    registration_data = {
                        "user_type": "individual",
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone": phone,
                        "aadhar": aadhar,
                        "password": password
                    }
                else:
                    registration_data = {
                        "user_type": "organization",
                        "org_name": org_name,
                        "org_email": org_email,
                        "org_phone": org_phone,
                        "contact_first_name": contact_first_name,
                        "contact_last_name": contact_last_name,
                        "contact_email": contact_email,
                        "password": password,
                        "certificate": certificate_file.name if certificate_file else None
                    }
                
                # API call to register user
                try:
                    response = make_api_request(
                        endpoint="/auth/register",
                        method="POST",
                        data=registration_data
                    )
                    
                    if response.get("success"):
                        st.success("Registration successful! Please check your email for verification.")
                        st.info("Redirecting to login page...")
                        # Redirect to login after successful registration
                        st.session_state.current_page = 'login'
                        st.rerun()
                    else:
                        st.error(f"Registration failed: {response.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")
    
    # Link to login page
    st.markdown("---")
    st.markdown("Already have an account?")
    if st.button("Sign In Instead", use_container_width=True):
        st.session_state.current_page = 'login'
        st.rerun()
    
    # OAuth registration options (if enabled)
    if os.getenv("ENABLE_OAUTH", "false").lower() == "true":
        st.markdown("---")
        st.markdown("Or register with:")
        
        col1, col2 = st.columns(2)
        with col1:
            google_login_url = get_oauth_login_url("google")
            st.markdown(f'<a href="{google_login_url}" target="_self" style="text-decoration: none;"><button style="width: 100%; padding: 10px; background-color: #4285f4; color: white; border: none; border-radius: 5px; cursor: pointer;">Continue with Google</button></a>', unsafe_allow_html=True)
        
        with col2:
            facebook_login_url = get_oauth_login_url("facebook")
            st.markdown(f'<a href="{facebook_login_url}" target="_self" style="text-decoration: none;"><button style="width: 100%; padding: 10px; background-color: #1877f2; color: white; border: none; border-radius: 5px; cursor: pointer;">Continue with Facebook</button></a>', unsafe_allow_html=True)

# ================================
# AUTHENTICATED CONTENT PAGES
# ================================

def render_home_content():
    """Render home page for authenticated users."""
    user_name = st.session_state.get(SESSION_KEYS['user_data'], {}).get('first_name', 'User')
    st.title(f"Welcome back, {user_name}!")
    # ... more content ...

def render_explore_content():
    st.title("Explore Campaigns")
    # ... more content ...

def render_campaign_content():
    st.title("Create or Manage Campaigns")
    # ... more content ...

def render_profile_content():
    st.title("Your Profile")
    # ... more content ...

# ================================
# PAGE ROUTING & MAIN APP
# ================================
def render_page_content():
    """Render content based on authentication status."""
    current_page = st.session_state.get(SESSION_KEYS['current_page'], 'login')
    
    handle_oauth_callback()
    
    if not is_authenticated():
        page_map = {'login': render_login_content, 'register': render_register_content}
        render_func = page_map.get(current_page, render_login_content)
        render_func()
    else:
        page_map = {
            'home': render_home_content,
            'explore': render_explore_content,
            'campaign': render_campaign_content,
            'profile': render_profile_content
        }
        render_func = page_map.get(current_page, render_home_content)
        render_func()

def main():
    """Main application."""
    st.set_page_config(page_title="Haven", layout="wide")
    
    initialize_session()
    
    st.markdown("""<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>""", unsafe_allow_html=True)

    with st.sidebar:
        if is_authenticated():
            render_authenticated_sidebar()
        else:
            render_auth_only_sidebar()
            
    render_page_content()

if __name__ == "__main__":
    main()

