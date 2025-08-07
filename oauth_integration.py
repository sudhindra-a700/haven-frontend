"""
OAuth Integration for HAVEN Frontend
Handles Google and Facebook OAuth login with popup windows
"""

import streamlit as st
import requests
import logging
from typing import Dict, Any, Tuple, Optional
import time
import webbrowser
import urllib.parse

logger = logging.getLogger(__name__)

class OAuthManager:
    """Manages OAuth authentication for Google and Facebook"""
    
    def __init__(self, backend_url: str = "http://localhost:8000"):
        self.backend_url = backend_url
    
    def initiate_google_login(self, user_type: str = "individual") -> Dict[str, Any]:
        """Initiate Google OAuth login"""
        try:
            response = requests.get(
                f"{self.backend_url}/api/v1/google/login",
                params={"user_type": user_type},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Google OAuth initiation failed: {response.text}")
                return {"error": "Failed to initiate Google login"}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Google OAuth request failed: {e}")
            return {"error": "Unable to connect to authentication server"}
    
    def initiate_facebook_login(self, user_type: str = "individual") -> Dict[str, Any]:
        """Initiate Facebook OAuth login"""
        try:
            response = requests.get(
                f"{self.backend_url}/api/v1/facebook/login",
                params={"user_type": user_type},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Facebook OAuth initiation failed: {response.text}")
                return {"error": "Failed to initiate Facebook login"}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Facebook OAuth request failed: {e}")
            return {"error": "Unable to connect to authentication server"}
    
    def check_oauth_status(self, provider: str, user_id: str) -> Dict[str, Any]:
        """Check OAuth user status"""
        try:
            response = requests.get(
                f"{self.backend_url}/api/v1/status/{provider}/{user_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "User not found"}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"OAuth status check failed: {e}")
            return {"error": "Unable to check status"}

def render_oauth_buttons(user_type: str = "individual"):
    """Render OAuth login buttons with proper styling"""
    oauth_manager = OAuthManager()
    
    st.markdown("### 🔐 Social Login")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Continue with Google", key=f"google_login_{user_type}", use_container_width=True):
            with st.spinner("Initiating Google login..."):
                result = oauth_manager.initiate_google_login(user_type)
                
                if "auth_url" in result:
                    # Store OAuth state
                    st.session_state.oauth_provider = "google"
                    st.session_state.oauth_state = result.get("state")
                    st.session_state.oauth_user_type = user_type
                    
                    # Show instructions for popup
                    st.info("🔗 **Google Login Instructions:**\n\n"
                           "1. Click the link below to open Google login\n"
                           "2. Complete authentication in the new window\n"
                           "3. Return to this page after login")
                    
                    # Display clickable link
                    st.markdown(f"[🚀 **Open Google Login**]({result['auth_url']})")
                    
                    # JavaScript to open popup (if supported)
                    st.markdown(f"""
                    <script>
                    window.open('{result['auth_url']}', 'google_login', 'width=500,height=600');
                    </script>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.error(f"❌ Google login failed: {result.get('error', 'Unknown error')}")
    
    with col2:
        if st.button("📘 Continue with Facebook", key=f"facebook_login_{user_type}", use_container_width=True):
            with st.spinner("Initiating Facebook login..."):
                result = oauth_manager.initiate_facebook_login(user_type)
                
                if "auth_url" in result:
                    # Store OAuth state
                    st.session_state.oauth_provider = "facebook"
                    st.session_state.oauth_state = result.get("state")
                    st.session_state.oauth_user_type = user_type
                    
                    # Show instructions for popup
                    st.info("🔗 **Facebook Login Instructions:**\n\n"
                           "1. Click the link below to open Facebook login\n"
                           "2. Complete authentication in the new window\n"
                           "3. Return to this page after login")
                    
                    # Display clickable link
                    st.markdown(f"[🚀 **Open Facebook Login**]({result['auth_url']})")
                    
                    # JavaScript to open popup (if supported)
                    st.markdown(f"""
                    <script>
                    window.open('{result['auth_url']}', 'facebook_login', 'width=500,height=600');
                    </script>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.error(f"❌ Facebook login failed: {result.get('error', 'Unknown error')}")

def check_oauth_callback():
    """Check for OAuth callback parameters in URL"""
    # Check URL parameters for OAuth success/error
    try:
        query_params = st.query_params
    except:
        # Fallback for older Streamlit versions
        query_params = st.experimental_get_query_params()
    
    if "oauth_success" in query_params:
        provider = query_params.get("provider", "unknown")
        user_type = query_params.get("user_type", "individual")
        user_id = query_params.get("user_id", "")
        
        if isinstance(provider, list):
            provider = provider[0]
        if isinstance(user_type, list):
            user_type = user_type[0]
        if isinstance(user_id, list):
            user_id = user_id[0]
        
        if user_id:
            st.success(f"🎉 **{provider.title()} Login Successful!**\n\n"
                      f"Welcome! You've been registered as an {user_type}.\n"
                      f"User ID: {user_id}")
            
            # Set session state
            st.session_state.user_authenticated = True
            st.session_state.user_type = user_type
            st.session_state.user_role = user_type
            st.session_state.oauth_provider = provider
            st.session_state.user_id = user_id
            
            # Clear URL parameters
            try:
                st.query_params.clear()
            except:
                st.experimental_set_query_params()
            
            return True
    
    elif "oauth_error" in query_params:
        provider = query_params.get("provider", "unknown")
        message = query_params.get("message", "Unknown error")
        
        if isinstance(provider, list):
            provider = provider[0]
        if isinstance(message, list):
            message = message[0]
        
        st.error(f"❌ **{provider.title()} Login Failed**\n\n{urllib.parse.unquote(message)}")
        
        # Clear URL parameters
        try:
            st.query_params.clear()
        except:
            st.experimental_set_query_params()
    
    return False

def render_oauth_status():
    """Render OAuth login status if user is authenticated via OAuth"""
    if (st.session_state.get("user_authenticated") and 
        st.session_state.get("oauth_provider")):
        
        provider = st.session_state.oauth_provider
        user_type = st.session_state.get("user_type", "individual")
        user_id = st.session_state.get("user_id", "")
        
        st.success(f"✅ **Logged in via {provider.title()}**\n\n"
                  f"**Role:** {user_type.title()}\n"
                  f"**User ID:** {user_id}")
        
        if st.button("🚪 Logout", key="oauth_logout"):
            # Clear OAuth session
            for key in ["user_authenticated", "oauth_provider", "user_type", 
                       "user_role", "user_id", "oauth_state", "oauth_user_type"]:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.experimental_rerun()
        
        return True
    
    return False

