# Haven Crowdfunding Platform - DIAGNOSTIC VERSION
# This version includes detailed logging and error messages to identify OAuth issues

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
import time
import jwt

# ================================
# DIAGNOSTIC CONFIGURATION
# ================================

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

# DIAGNOSTIC: Show environment variables (safely)
st.sidebar.markdown("### 🔧 Diagnostic Info")
st.sidebar.markdown(f"**Backend URL**: {BACKEND_URL[:30] + '...' if BACKEND_URL and len(BACKEND_URL) > 30 else BACKEND_URL or 'NOT SET'}")
st.sidebar.markdown(f"**API Base**: {API_BASE[:30] + '...' if API_BASE and len(API_BASE) > 30 else API_BASE or 'NOT SET'}")
st.sidebar.markdown(f"**Google Client ID**: {'SET' if GOOGLE_CLIENT_ID else 'NOT SET'}")
st.sidebar.markdown(f"**Facebook App ID**: {'SET' if FACEBOOK_APP_ID else 'NOT SET'}")

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

# ================================
# DIAGNOSTIC FUNCTIONS
# ================================

def diagnostic_backend_test():
    """Test backend connectivity with detailed diagnostics"""
    st.sidebar.markdown("### 🔍 Backend Tests")
    
    if not BACKEND_URL:
        st.sidebar.error("❌ Backend URL not configured")
        return False
    
    try:
        # Test basic connectivity
        st.sidebar.info("Testing basic connectivity...")
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ Backend is reachable")
        else:
            st.sidebar.warning(f"⚠️ Backend returned {response.status_code}")
    except Exception as e:
        st.sidebar.error(f"❌ Backend unreachable: {str(e)}")
        return False
    
    # Test OAuth endpoints
    if API_BASE:
        try:
            st.sidebar.info("Testing Google OAuth endpoint...")
            response = requests.get(f"{API_BASE}/auth/google/login", params={"user_type": "individual"}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "auth_url" in data:
                    st.sidebar.success("✅ Google OAuth endpoint working")
                else:
                    st.sidebar.error("❌ Google OAuth response missing auth_url")
                    st.sidebar.json(data)
            else:
                st.sidebar.error(f"❌ Google OAuth failed: {response.status_code}")
                st.sidebar.text(response.text)
        except Exception as e:
            st.sidebar.error(f"❌ Google OAuth error: {str(e)}")
        
        try:
            st.sidebar.info("Testing Facebook OAuth endpoint...")
            response = requests.get(f"{API_BASE}/auth/facebook/login", params={"user_type": "individual"}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "auth_url" in data:
                    st.sidebar.success("✅ Facebook OAuth endpoint working")
                else:
                    st.sidebar.error("❌ Facebook OAuth response missing auth_url")
                    st.sidebar.json(data)
            else:
                st.sidebar.error(f"❌ Facebook OAuth failed: {response.status_code}")
                st.sidebar.text(response.text)
        except Exception as e:
            st.sidebar.error(f"❌ Facebook OAuth error: {str(e)}")
    
    return True

# ================================
# OAUTH FUNCTIONS WITH DIAGNOSTICS
# ================================

def get_oauth_login_url_diagnostic(provider: str, user_type: str = "individual") -> Optional[str]:
    """Get OAuth login URL with detailed diagnostics"""
    st.write(f"🔍 **Diagnostic: Getting {provider} OAuth URL**")
    
    if not API_BASE:
        st.error("❌ API_BASE is not configured")
        return None
    
    endpoint = f"/auth/{provider}/login"
    url = f"{API_BASE}{endpoint}"
    params = {"user_type": user_type}
    
    st.write(f"📡 Making request to: `{url}`")
    st.write(f"📋 Parameters: `{params}`")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        st.write(f"📊 Response status: `{response.status_code}`")
        
        if response.status_code == 200:
            try:
                data = response.json()
                st.write("📄 Response data:")
                st.json(data)
                
                auth_url = data.get("auth_url")
                if auth_url:
                    st.success(f"✅ {provider} OAuth URL generated successfully!")
                    return auth_url
                else:
                    st.error(f"❌ Response missing 'auth_url' field")
                    return None
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON response: {str(e)}")
                st.text(f"Raw response: {response.text}")
                return None
        else:
            st.error(f"❌ HTTP {response.status_code} error")
            st.text(f"Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Connection error - Backend service unavailable")
        return None
    except requests.exceptions.Timeout:
        st.error("❌ Request timeout")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None

def handle_oauth_callback():
    """Handle OAuth callback with diagnostics"""
    try:
        query_params = st.experimental_get_query_params()
        
        if query_params:
            st.write("🔍 **Diagnostic: URL Parameters Found**")
            st.json(query_params)
        
        if "auth" in query_params:
            auth_status = query_params["auth"][0]
            st.write(f"🔍 **Diagnostic: Auth status = {auth_status}**")
            
            if auth_status == "success" and "token" in query_params:
                jwt_token = query_params["token"][0]
                st.write(f"🔍 **Diagnostic: JWT token received (length: {len(jwt_token)})**")
                
                try:
                    decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})
                    st.write("🔍 **Diagnostic: Decoded token:**")
                    st.json(decoded_token)
                    
                    user_data = {
                        "id": decoded_token.get("user_id"),
                        "email": decoded_token.get("email"),
                        "first_name": decoded_token.get("name", "").split(" ")[0] if decoded_token.get("name") else "User",
                        "last_name": " ".join(decoded_token.get("name", "").split(" ")[1:]) if decoded_token.get("name") else "",
                        "provider": decoded_token.get("provider"),
                        "user_type": decoded_token.get("user_type", "individual")
                    }
                    
                    login_user(user_data, jwt_token)
                    st.experimental_set_query_params()
                    st.success(f"✅ Successfully signed in with {decoded_token.get('provider', 'OAuth')}!")
                    st.balloons()
                    st.session_state[SESSION_KEYS['current_page']] = 'home'
                    time.sleep(1)
                    st.experimental_rerun()
                    
                except jwt.InvalidTokenError as e:
                    st.error(f"❌ Invalid JWT token: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error processing token: {str(e)}")
                    
            elif auth_status == "error":
                provider = query_params.get("provider", ["Unknown"])[0]
                error_message = query_params.get("message", ["Unknown error"])[0]
                st.error(f"❌ {provider.title()} authentication failed: {error_message}")
                st.experimental_set_query_params()
                
    except Exception as e:
        st.error(f"❌ OAuth callback error: {str(e)}")

# ================================
# SIMPLIFIED AUTHENTICATION SYSTEM
# ================================

def initialize_session():
    """Initialize session state"""
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
    """Check if user is authenticated"""
    return st.session_state.get(SESSION_KEYS['authenticated'], False)

def login_user(user_data: Dict, access_token: str, refresh_token: str = None):
    """Login user and set session state"""
    st.session_state[SESSION_KEYS['authenticated']] = True
    st.session_state[SESSION_KEYS['user_data']] = user_data
    st.session_state[SESSION_KEYS['access_token']] = access_token
    st.session_state[SESSION_KEYS['refresh_token']] = refresh_token
    st.session_state[SESSION_KEYS['user_id']] = user_data.get('id')
    st.session_state[SESSION_KEYS['login_timestamp']] = datetime.now()
    st.session_state[SESSION_KEYS['current_page']] = 'home'

def logout_user():
    """Logout user"""
    for key in SESSION_KEYS.values():
        if key in st.session_state:
            del st.session_state[key]
    st.session_state[SESSION_KEYS['current_page']] = 'login'
    st.session_state[SESSION_KEYS['authenticated']] = False
    st.success("✅ Successfully logged out!")
    st.rerun()

def get_current_user() -> Optional[Dict]:
    """Get current authenticated user data"""
    if is_authenticated():
        return st.session_state.get(SESSION_KEYS['user_data'])
    return None

# ================================
# DIAGNOSTIC LOGIN PAGE
# ================================

def render_diagnostic_login_content():
    """Render diagnostic login page"""
    st.header("Welcome to Haven - DIAGNOSTIC MODE")
    st.subheader("Please sign in to continue")
    
    # Run diagnostics
    diagnostic_backend_test()
    
    # Add OAuth callback handling
    handle_oauth_callback()

    # OAuth buttons section
    st.markdown("### 🔐 Social Login - DIAGNOSTIC MODE")
    
    # Show detailed OAuth testing
    st.markdown("#### 🔍 OAuth URL Generation Test")
    
    # Test Google OAuth
    st.markdown("**Testing Google OAuth:**")
    google_auth_url = get_oauth_login_url_diagnostic("google", "individual")
    
    if google_auth_url:
        st.markdown(f"🔗 **Google OAuth URL Generated:**")
        st.code(google_auth_url)
        
        # Create working button
        google_button_html = f"""
        <script>
        function openGoogleLogin() {{
            const popup = window.open('{google_auth_url}', 'google_login', 'width=500,height=600,scrollbars=yes,resizable=yes');
            
            window.addEventListener('message', function(event) {{
                if (event.data.type === 'OAUTH_SUCCESS') {{
                    popup.close();
                    const token = event.data.data.token;
                    window.location.href = window.location.origin + '?auth=success&token=' + encodeURIComponent(token);
                }} else if (event.data.type === 'OAUTH_ERROR') {{
                    popup.close();
                    const error = event.data.data.error;
                    window.location.href = window.location.origin + '?auth=error&provider=google&message=' + encodeURIComponent(error);
                }}
            }}, false);
        }}
        </script>
        
        <button onclick="openGoogleLogin()" style="
            background-color: #EA4335;
            color: white;
            border: none;
            padding: 15px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 10px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            transition: background-color 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        " onmouseover="this.style.backgroundColor='#d93025'" onmouseout="this.style.backgroundColor='#EA4335'">
            G Sign in With Google
        </button>
        """
        st.components.v1.html(google_button_html, height=70)
    else:
        st.error("❌ Google OAuth URL generation failed")
    
    st.markdown("---")
    
    # Test Facebook OAuth
    st.markdown("**Testing Facebook OAuth:**")
    facebook_auth_url = get_oauth_login_url_diagnostic("facebook", "individual")
    
    if facebook_auth_url:
        st.markdown(f"🔗 **Facebook OAuth URL Generated:**")
        st.code(facebook_auth_url)
        
        # Create working button
        facebook_button_html = f"""
        <script>
        function openFacebookLogin() {{
            const popup = window.open('{facebook_auth_url}', 'facebook_login', 'width=500,height=600,scrollbars=yes,resizable=yes');
            
            window.addEventListener('message', function(event) {{
                if (event.data.type === 'OAUTH_SUCCESS') {{
                    popup.close();
                    const token = event.data.data.token;
                    window.location.href = window.location.origin + '?auth=success&token=' + encodeURIComponent(token);
                }} else if (event.data.type === 'OAUTH_ERROR') {{
                    popup.close();
                    const error = event.data.data.error;
                    window.location.href = window.location.origin + '?auth=error&provider=facebook&message=' + encodeURIComponent(error);
                }}
            }}, false);
        }}
        </script>
        
        <button onclick="openFacebookLogin()" style="
            background-color: #1877F2;
            color: white;
            border: none;
            padding: 15px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 10px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            transition: background-color 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        " onmouseover="this.style.backgroundColor='#166fe5'" onmouseout="this.style.backgroundColor='#1877F2'">
            f Sign in With Facebook
        </button>
        """
        st.components.v1.html(facebook_button_html, height=70)
    else:
        st.error("❌ Facebook OAuth URL generation failed")

    st.markdown("---")
    st.markdown("### 📧 Email Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            st.info("Email login not implemented in diagnostic mode")

# ================================
# SIMPLE AUTHENTICATED PAGES
# ================================

def render_home_content():
    """Render home page"""
    user_name = st.session_state.get(SESSION_KEYS['user_data'], {}).get('first_name', 'User')
    st.title(f"Welcome back, {user_name}!")
    st.success("🎉 OAuth authentication successful!")
    
    st.markdown("### User Data:")
    user_data = get_current_user()
    if user_data:
        st.json(user_data)

def render_register_content():
    """Render registration page"""
    st.header("Create your Haven Account")
    st.info("Registration page - not implemented in diagnostic mode")

# ================================
# SIDEBAR
# ================================

def render_sidebar():
    """Render sidebar"""
    if is_authenticated():
        user_data = get_current_user()
        if user_data:
            st.sidebar.markdown("### 👤 Profile")
            st.sidebar.markdown(f"**{user_data.get('first_name', 'User')} {user_data.get('last_name', '')}**")
            st.sidebar.markdown(f"📧 {user_data.get('email', 'No email')}")
            
            if st.sidebar.button("Logout", use_container_width=True):
                logout_user()
    else:
        st.sidebar.markdown("### 🏠 Haven")
        st.sidebar.markdown("*Diagnostic Mode*")
        
        if st.sidebar.button("Sign In", use_container_width=True):
            st.session_state.current_page = 'login'
            st.rerun()
        if st.sidebar.button("Register", use_container_width=True):
            st.session_state.current_page = 'register'
            st.rerun()

# ================================
# MAIN APP
# ================================

def render_page_content():
    """Render content based on authentication status"""
    current_page = st.session_state.get(SESSION_KEYS['current_page'], 'login')
    
    if not is_authenticated():
        if current_page == 'register':
            render_register_content()
        else:
            render_diagnostic_login_content()
    else:
        render_home_content()

def main():
    """Main application"""
    st.set_page_config(
        page_title="Haven - Diagnostic Mode", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session()
    
    with st.sidebar:
        render_sidebar()
        
    render_page_content()

if __name__ == "__main__":
    main()

