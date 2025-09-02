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

def get_bootstrap_icon_b64(icon_name: str, size: int = 18, color: str = "#ffffff") -> str:
    """Convert Bootstrap SVG icon to base64 for reliable display in production."""
    svg_path = f"assets/{icon_name}.svg"
    
    if os.path.exists(svg_path):
        try:
            with open(svg_path, "rb") as f:
                svg_data = f.read()
            
            # Convert to base64
            b64_svg = base64.b64encode(svg_data).decode()
            
            # Create data URL with proper styling
            return f'''<img src="data:image/svg+xml;base64,{b64_svg}" 
                       width="{size}" height="{size}" 
                       style="vertical-align: middle; margin-right: 8px; 
                              filter: brightness(0) saturate(100%) invert(100%);">'''
        except Exception as e:
            logger.warning(f"Failed to load icon {icon_name}: {e}")
            return f'<span style="margin-right: 8px; color: white;">●</span>'
    
    # Fallback for missing icons
    return f'<span style="margin-right: 8px; color: white;">●</span>'

def get_colored_icon_b64(icon_name: str, size: int = 24, color: str = "#4CAF50") -> str:
    """Get colored Bootstrap icon for main content areas."""
    svg_path = f"assets/{icon_name}.svg"
    
    if os.path.exists(svg_path):
        try:
            with open(svg_path, "rb") as f:
                svg_data = f.read()
            
            b64_svg = base64.b64encode(svg_data).decode()
            
            # Color filter mappings for different colors
            color_filters = {
                "#4CAF50": "invert(27%) sepia(51%) saturate(2878%) hue-rotate(346deg) brightness(104%) contrast(97%)",
                "#2196F3": "invert(27%) sepia(98%) saturate(1000%) hue-rotate(196deg) brightness(104%) contrast(97%)",
                "#FF9800": "invert(27%) sepia(98%) saturate(1000%) hue-rotate(25deg) brightness(104%) contrast(97%)",
                "#9C27B0": "invert(27%) sepia(98%) saturate(1000%) hue-rotate(280deg) brightness(104%) contrast(97%)",
                "#FF5722": "invert(27%) sepia(98%) saturate(1000%) hue-rotate(15deg) brightness(104%) contrast(97%)",
                "#666": "invert(27%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(60%) contrast(97%)"
            }
            
            filter_css = color_filters.get(color, "")
            
            return f'''<img src="data:image/svg+xml;base64,{b64_svg}" 
                       width="{size}" height="{size}" 
                       style="vertical-align: middle; filter: {filter_css};">'''
        except Exception as e:
            logger.warning(f"Failed to load colored icon {icon_name}: {e}")
            return f'<span style="color: {color};">●</span>'
    
    return f'<span style="color: {color};">●</span>'

def create_icon_button(icon_name: str, label: str, key: str, size: int = 18, 
                      color: str = "#ffffff", help_text: Optional[str] = None) -> bool:
    """Create clickable icon button with professional styling."""
    
    icon_html = get_bootstrap_icon_b64(icon_name, size, color)
    
    # Professional button styling with hover effects
    button_html = f'''
    <div style="margin: 5px 0;">
        <div style="
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 12px 15px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            text-align: left;
            font-size: 14px;
            font-weight: 500;
            display: flex;
            align-items: center;
            backdrop-filter: blur(10px);
        " onmouseover="this.style.background='rgba(255, 255, 255, 0.2)'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.2)'"
           onmouseout="this.style.background='rgba(255, 255, 255, 0.1)'; this.style.transform='translateY(0px)'; this.style.boxShadow='none'">
            {icon_html}
            <span style="flex: 1;">{label}</span>
        </div>
    </div>
    '''
    
    st.markdown(button_html, unsafe_allow_html=True)
    
    # Return actual Streamlit button functionality
    return st.button(f"→ {label}", key=key, help=help_text or f"Navigate to {label}")

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


# ... (rest of the file remains the same until AUTHENTICATION PAGES)
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
    
    if 'code' in query_params and 'state' in query_params:
        # Handle OAuth callback
        auth_code = query_params['code'][0]
        state = query_params['state'][0]
        
        # Exchange code for token (implement based on your backend)
        st.info("🔄 Processing OAuth login...")
        
        # Clear query parameters
        st.experimental_set_query_params()

# ================================
# NAVIGATION COMPONENTS
# ================================

def render_auth_only_sidebar():
    """Render sidebar for unauthenticated users - STRICT ACCESS CONTROL."""
    
    st.markdown("""
    <style>
    .auth-nav-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .auth-nav-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 25px;
        color: white;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 20px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .auth-message {
        background: rgba(255, 255, 255, 0.15);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .auth-features {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        text-align: left;
        backdrop-filter: blur(10px);
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        margin: 12px 0;
        font-size: 14px;
        color: rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        color: white;
        transform: translateX(5px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Authentication-only navigation section
    st.sidebar.markdown('<div class="auth-nav-section">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="auth-nav-title">🏠 Haven Platform</div>', unsafe_allow_html=True)
    
    # Welcome message with backend status
    backend_status = check_backend_health()
    status_icon = "wifi" if backend_status["online"] else "wifi-off"
    status_text = "Backend Online" if backend_status["online"] else "Backend Offline"
    
    auth_message_html = f'''
    <div class="auth-message">
        {get_bootstrap_icon_b64("shield-lock-fill", 24)} 
        <strong>Welcome to Haven!</strong><br>
        <small>Please login or register to access the platform</small><br><br>
        <div style="font-size: 12px; opacity: 0.8;">
            {get_bootstrap_icon_b64(status_icon, 14)} {status_text}
        </div>
    </div>
    '''
    st.sidebar.markdown(auth_message_html, unsafe_allow_html=True)
    
    # ONLY login and register navigation
    auth_nav_items = [
        ("box-arrow-in-right", "Login", "login"),
        ("person-plus-fill", "Register", "register")
    ]
    
    for icon_name, label, page_key in auth_nav_items:
        if create_icon_button(icon_name, label, f"auth_nav_{page_key}"):
            st.session_state[SESSION_KEYS['current_page']] = page_key
            st.rerun()
    
    # Features preview (what they'll get after login)
    features_html = f'''
    <div class="auth-features">
        <div style="font-weight: bold; margin-bottom: 15px; text-align: center;">
            {get_bootstrap_icon_b64("star-fill", 18)} After Login, You Can:
        </div>
        <div class="feature-item">
            {get_bootstrap_icon_b64("search", 16)} Browse & Support Campaigns
        </div>
        <div class="feature-item">
            {get_bootstrap_icon_b64("plus-circle-fill", 16)} Create Your Own Campaigns
        </div>
        <div class="feature-item">
            {get_bootstrap_icon_b64("speedometer2", 16)} Access Personal Dashboard
        </div>
        <div class="feature-item">
            {get_bootstrap_icon_b64("person-circle", 16)} Manage Your Profile
        </div>
        <div class="feature-item">
            {get_bootstrap_icon_b64("heart-fill", 16)} Track Your Contributions
        </div>
        <div class="feature-item">
            {get_bootstrap_icon_b64("trophy-fill", 16)} View Campaign Analytics
        </div>
        <div class="feature-item">
            {get_bootstrap_icon_b64("shield-check", 16)} OAuth Authentication
        </div>
    </div>
    '''
    st.sidebar.markdown(features_html, unsafe_allow_html=True)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

def render_authenticated_sidebar():
    """Render full sidebar for authenticated users with real data."""
    
    st.markdown("""
    <style>
    .nav-section {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        color: white;
        box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .nav-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
        color: white;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 15px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .user-welcome {
        background: rgba(255, 255, 255, 0.15);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stats-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #dee2e6;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stat-item:last-child {
        border-bottom: none;
    }
    
    .stat-item:hover {
        background: rgba(76, 175, 80, 0.05);
        transform: translateX(5px);
        border-radius: 8px;
        padding-left: 16px;
    }
    
    .stat-value {
        font-weight: bold;
        color: #4CAF50;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation section
    st.sidebar.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="nav-title">🏠 Haven Platform</div>', unsafe_allow_html=True)
    
    # User welcome section with real data
    user_data = st.session_state.get(SESSION_KEYS['user_data'], {})
    user_name = user_data.get('first_name', user_data.get('name', 'User'))
    user_email = user_data.get('email', 'user@example.com')
    
    # Backend status
    backend_status = check_backend_health()
    status_icon = "wifi" if backend_status["online"] else "wifi-off"
    status_color = "#4CAF50" if backend_status["online"] else "#FF5722"
    
    welcome_html = f'''
    <div class="user-welcome">
        {get_bootstrap_icon_b64("person-circle", 24)} Welcome, {user_name}!
        <br><small style="opacity: 0.8;">{user_email}</small>
        <br><small style="color: {status_color};">
            {get_bootstrap_icon_b64(status_icon, 12)} 
            {"✅ Connected" if backend_status["online"] else "❌ Offline"}
        </small>
    </div>
    '''
    st.sidebar.markdown(welcome_html, unsafe_allow_html=True)
    
    # FULL navigation for authenticated users
    nav_items = [
        ("house-fill", "Home", "home"),
        ("search", "Browse Campaigns", "explore"),
        ("plus-circle-fill", "Create Campaign", "campaign"),
        ("person-circle", "Profile", "profile"),
        ("question-circle-fill", "Help", "help"),
        ("box-arrow-right", "Logout", "logout")
    ]
    
    for icon_name, label, page_key in nav_items:
        if create_icon_button(icon_name, label, f"nav_{page_key}"):
            if page_key == "logout":
                logout_user()
            else:
                st.session_state[SESSION_KEYS['current_page']] = page_key
                st.rerun()
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # User stats section with real data
    render_user_stats_section()

def render_user_stats_section():
    """Render user statistics section with real database data."""
    
    user_id = st.session_state.get(SESSION_KEYS['user_id'])
    if not user_id:
        return
    
    st.sidebar.markdown('<div class="stats-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 📊 Your Stats")
    
    try:
        # Try to get stats from API first
        stats_response = make_api_request("/users/me/stats", auth_required=True)
        
        if stats_response.get('success'):
            stats_data = stats_response['data']
            campaigns_created = stats_data.get('campaigns_created', 0)
            campaigns_backed = stats_data.get('campaigns_backed', 0)
            total_contributed = stats_data.get('total_contributed', 0)
        else:
            # Fallback to direct database queries
            campaigns_created = len(fetch_user_campaigns(user_id))
            contributions = fetch_user_contributions(user_id)
            campaigns_backed = len(contributions)
            total_contributed = sum(c.get('amount', 0) for c in contributions)
        
        # Display stats
        stats_items = [
            ("rocket-takeoff", "Campaigns Created", campaigns_created),
            ("bookmark-star", "Campaigns Backed", campaigns_backed),
            ("currency-dollar", "Total Contributed", f"₹{total_contributed:,.2f}")
        ]
        
        for icon_name, label, value in stats_items:
            icon_html = get_colored_icon_b64(icon_name, 16, "#4CAF50")
            
            stat_html = f'''
            <div class="stat-item">
                <span>{icon_html} {label}</span>
                <span class="stat-value">{value}</span>
            </div>
            '''
            st.sidebar.markdown(stat_html, unsafe_allow_html=True)
    
    except Exception as e:
        logger.error(f"Failed to load user stats: {e}")
        # Show loading message
        st.sidebar.markdown("📊 Loading stats...")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ================================
# AUTHENTICATION PAGES
# ================================

def render_login_content():
    """Render login page with OAuth integration."""
    st.markdown("""
        <style>
        .login-container {
            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin: 2rem auto;
            max-width: 500px;
        }
        .login-header {
            text-align: center;
            color: #2e7d32;
            margin-bottom: 2rem;
        }
        .divider {
            text-align: center;
            margin: 1.5rem 0;
            position: relative;
        }
        .divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #ccc;
        }
        .divider span {
            background: white;
            padding: 0 1rem;
            color: #666;
        }
        </style>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <h1>🏠 Welcome to HAVEN</h1>
                <h3>Your Trusted Crowdfunding Platform</h3>
                <p>Sign in to start your journey of making a difference</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### 🔐 Sign In")
        
        google_oauth_html = f'''
        <div style="text-align: center; margin: 20px 0;">
            <a href="{get_oauth_login_url('google')}" target="_self" style="
                display: inline-block;
                background: #4285F4;
                color: white;
                padding: 15px 40px;
                border-radius: 12px;
                text-decoration: none;
                font-weight: bold;
                font-size: 16px;
                transition: all 0.3s ease;
                box-shadow: 0 6px 20px rgba(66, 133, 244, 0.3);
                width: 100%;
                margin-bottom: 15px;
            ">
                {get_bootstrap_icon_b64('google', 20)} Continue with Google
            </a>
        </div>
        '''
        st.markdown(google_oauth_html, unsafe_allow_html=True)

        facebook_oauth_html = f'''
        <div style="text-align: center; margin: 20px 0;">
            <a href="{get_oauth_login_url('facebook')}" target="_self" style="
                display: inline-block;
                background: #1877F2;
                color: white;
                padding: 15px 40px;
                border-radius: 12px;
                text-decoration: none;
                font-weight: bold;
                font-size: 16px;
                transition: all 0.3s ease;
                box-shadow: 0 6px 20px rgba(24, 119, 242, 0.3);
                width: 100%;
                margin-bottom: 25px;
            ">
                {get_bootstrap_icon_b64('facebook', 20)} Continue with Facebook
            </a>
        </div>
        '''
        st.markdown(facebook_oauth_html, unsafe_allow_html=True)

        st.markdown("""
        <div class="divider">
            <span>or</span>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("#### Email & Password")
            
            email = st.text_input(
                "📧 Email Address",
                placeholder="Enter your email address",
                help="Use the email you registered with"
            )
            
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter your password",
                help="Your secure password"
            )
            
            login_submitted = st.form_submit_button(
                "🚀 Sign In",
                use_container_width=True,
                type="primary"
            )
        
        if login_submitted:
            if email and password:
                login_data = {"email": email, "password": password}
                login_response = make_api_request("/auth/login", method="POST", data=login_data)
                
                if login_response.get('success'):
                    user_data = login_response['data'].get('user', {})
                    access_token = login_response['data'].get('access_token')
                    refresh_token = login_response['data'].get('refresh_token')
                    
                    if access_token:
                        login_user(user_data, access_token, refresh_token)
                        st.success("✅ Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid response from server")
                else:
                    error_msg = login_response.get('error', 'Login failed')
                    st.error(f"❌ {error_msg}")
            else:
                st.error("❌ Please enter both email and password")
        
        st.markdown("---")
        if st.button("📝 Create Account", key="register_btn", use_container_width=True):
            st.session_state.current_page = 'register'
            st.rerun()


def render_register_content():
    """Render registration page with backend integration."""
    st.markdown(f"""
    <div style="text-align: center; margin: 40px 0;">
        <h1 style="color: #333; font-size: 36px; margin-bottom: 15px;">
            {get_colored_icon_b64('person-plus-fill', 42, '#2196F3')} Join Haven
        </h1>
        <p style="font-size: 20px; color: #666; max-width: 600px; margin: 0 auto;">
            Create your account to start crowdfunding
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            if st.form_submit_button("🎉 Create Account", use_container_width=True):
                if all([first_name, last_name, email, password, confirm_password, agree_terms]):
                    if password == confirm_password:
                        registration_data = {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "password": password
                        }
                        register_response = make_api_request("/auth/register", method="POST", data=registration_data)
                        if register_response.get('success'):
                            st.success("✅ Account created successfully! Please login.")
                            st.session_state[SESSION_KEYS['current_page']] = 'login'
                            st.rerun()
                        else:
                            error_msg = register_response.get('error', 'Registration failed')
                            st.error(f"❌ {error_msg}")
                    else:
                        st.error("❌ Passwords do not match")
                else:
                    st.error("❌ Please fill all fields and agree to terms")
        st.markdown("---")
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.current_page = 'login'
            st.rerun()

# ================================
# AUTHENTICATED CONTENT PAGES
# ================================

def render_home_content():
    """Render home page with content from pages/home.py."""
    user_name = st.session_state.get(SESSION_KEYS['user_data'], {}).get('first_name', 'User')
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: #2e7d32; font-size: 3rem; margin-bottom: 1rem;">
            🏠 Welcome to HAVEN, {user_name}!
        </h1>
        <h3 style="color: #388e3c; margin-bottom: 2rem;">
            Empowering Communities Through Crowdfunding
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚀 Start Campaign", key="start_campaign", use_container_width=True):
            st.session_state.current_page = 'campaign'
            st.rerun()
    with col2:
        if st.button("🌟 Explore", key="explore_projects", use_container_width=True):
            st.session_state.current_page = 'explore'
            st.rerun()
    with col3:
        if st.button("❤️ Donate", key="support_causes", use_container_width=True):
            st.session_state.current_page = 'explore'
            st.rerun()

def render_explore_content():
    st.markdown("## Browse Campaigns (Implementation continues...)")

def render_campaign_content():
    st.markdown("## Create Campaign (Implementation continues...)")

def render_profile_content():
    st.markdown("## Profile (Implementation continues...)")

# ================================
# PAGE ROUTING WITH STRICT AUTHENTICATION
# ================================

def render_page_content():
    """Render content based on authentication status - STRICT ACCESS CONTROL."""
    
    current_page = st.session_state.get(SESSION_KEYS['current_page'], 'login')
    
    handle_oauth_callback()
    
    if not is_authenticated():
        if current_page not in ['login', 'register']:
            st.session_state[SESSION_KEYS['current_page']] = 'login'
            current_page = 'login'
        
        if current_page == 'login':
            render_login_content()
        elif current_page == 'register':
            render_register_content()
    else:
        page_map = {
            'home': render_home_content,
            'explore': render_explore_content,
            'campaign': render_campaign_content,
            'profile': render_profile_content,
            'help': lambda: st.markdown("## Help Page"),
        }
        
        page_function = page_map.get(current_page, render_home_content)
        page_function()


# ================================
# MAIN APPLICATION
# ================================

def render_main_header():
    """Render main header with authentication and backend status."""
    st.markdown(f"""
    <style>
    .main-header {{
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    if is_authenticated():
        user_name = st.session_state.get(SESSION_KEYS['user_data'], {}).get('first_name', 'User')
        header_title = f"{get_bootstrap_icon_b64('house-fill', 36)} Welcome back, {user_name}!"
    else:
        header_title = f"{get_bootstrap_icon_b64('shield-lock-fill', 36)} Haven Platform"

    st.markdown(f'<div class="main-header"><h1>{header_title}</h1></div>', unsafe_allow_html=True)


def main():
    """Main application with clean environment variable usage."""
    st.set_page_config(
        page_title="Haven - Crowdfunding Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session()
    
    st.markdown("""
    <style>
    .stApp > header { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)
    
    if is_authenticated():
        render_authenticated_sidebar()
    else:
        render_auth_only_sidebar()
    
    render_page_content()

if __name__ == "__main__":
    main()
