"""
FIXED OAuth Integration for HAVEN Crowdfunding Platform Frontend
This file contains the corrected OAuth implementation that fixes:
1. Correct API endpoint paths (/api/v1)
2. Proper error handling and user feedback
3. Environment variable usage
4. OAuth callback handling
"""

import streamlit as st
import requests
import os
import logging
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any
import time

# Configure logging
logger = logging.getLogger(__name__)

class OAuthManager:
    """OAuth Manager for handling Google and Facebook authentication"""
    
    def __init__(self):
        # Use corrected environment variable name
        self.backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8501")
        
        # Remove trailing slash if present
        if self.backend_url.endswith('/'):
            self.backend_url = self.backend_url[:-1]
        
        # OAuth configuration
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.facebook_app_id = os.getenv("FACEBOOK_APP_ID")  # Fixed variable name
        
        logger.info(f"OAuth Manager initialized with backend: {self.backend_url}")
    
    def check_oauth_config(self) -> Dict[str, bool]:
        """Check if OAuth is properly configured"""
        return {
            "backend_url_set": bool(self.backend_url),
            "google_configured": bool(self.google_client_id),
            "facebook_configured": bool(self.facebook_app_id),
            "oauth_enabled": os.getenv("FEATURES_OAUTH_ENABLED", "false").lower() == "true"
        }
    
    def test_backend_connection(self) -> bool:
        """Test connection to backend"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Backend connection test failed: {e}")
            return False
    
    def initiate_google_login(self, user_type: str = "individual") -> Optional[str]:
        """
        FIXED: Initiate Google OAuth login
        - Uses correct API endpoint path (/api/v1)
        - Proper error handling
        - Returns auth URL for popup window
        """
        try:
            # Use fixed API endpoint path
            endpoint = f"{self.backend_url}/api/v1/auth/google/login"
            
            response = requests.get(
                endpoint,
                params={"user_type": user_type},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get("auth_url")
                
                if auth_url:
                    logger.info(f"Google OAuth URL generated for user_type: {user_type}")
                    return auth_url
                else:
                    st.error("❌ No authentication URL received from server")
                    return None
            else:
                error_msg = f"Server error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", error_msg)
                except:
                    pass
                
                st.error(f"❌ Failed to initiate Google login: {error_msg}")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to authentication server. Please check if the backend is running.")
            return None
        except requests.exceptions.Timeout:
            st.error("❌ Authentication server timeout. Please try again.")
            return None
        except Exception as e:
            logger.error(f"Google OAuth initiation error: {e}")
            st.error(f"❌ Google OAuth request failed: {str(e)}")
            return None
    
    def initiate_facebook_login(self, user_type: str = "individual") -> Optional[str]:
        """
        FIXED: Initiate Facebook OAuth login
        - Uses correct API endpoint path (/api/v1)
        - Proper error handling
        - Returns auth URL for popup window
        """
        try:
            # Use fixed API endpoint path
            endpoint = f"{self.backend_url}/api/v1/auth/facebook/login"
            
            response = requests.get(
                endpoint,
                params={"user_type": user_type},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                auth_url = data.get("auth_url")
                
                if auth_url:
                    logger.info(f"Facebook OAuth URL generated for user_type: {user_type}")
                    return auth_url
                else:
                    st.error("❌ No authentication URL received from server")
                    return None
            else:
                error_msg = f"Server error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", error_msg)
                except:
                    pass
                
                st.error(f"❌ Failed to initiate Facebook login: {error_msg}")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to authentication server. Please check if the backend is running.")
            return None
        except requests.exceptions.Timeout:
            st.error("❌ Authentication server timeout. Please try again.")
            return None
        except Exception as e:
            logger.error(f"Facebook OAuth initiation error: {e}")
            st.error(f"❌ Facebook OAuth request failed: {str(e)}")
            return None
    
    def check_auth_status(self) -> Dict[str, Any]:
        """Check authentication status from backend"""
        try:
            response = requests.get(f"{self.backend_url}/api/v1/auth/status", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Unable to check authentication status"}
        except Exception as e:
            logger.error(f"Auth status check failed: {e}")
            return {"error": f"Authentication status check failed: {str(e)}"}

def render_oauth_buttons(user_type: str = "individual"):
    """
    FIXED: Render OAuth login buttons with proper styling and error handling
    - Improved user experience
    - Better error messages
    - Popup window support
    """
    oauth_manager = OAuthManager()
    
    # Check OAuth configuration
    config_status = oauth_manager.check_oauth_config()
    
    if not config_status["oauth_enabled"]:
        st.warning("⚠️ OAuth authentication is currently disabled")
        return
    
    if not config_status["backend_url_set"]:
        st.error("❌ Backend URL not configured")
        return
    
    # Test backend connection
    if not oauth_manager.test_backend_connection():
        st.error("❌ Cannot connect to authentication server")
        st.info("💡 Please ensure the backend service is running and accessible")
        return
    
    st.markdown("### 🔐 Social Login")
    st.markdown("Choose your preferred login method:")
    
    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if config_status["google_configured"]:
            if st.button(
                "🔍 Continue with Google", 
                key=f"google_login_{user_type}", 
                use_container_width=True,
                type="primary"
            ):
                with st.spinner("🔄 Connecting to Google..."):
                    auth_url = oauth_manager.initiate_google_login(user_type)
                    
                    if auth_url:
                        # Store OAuth state in session
                        st.session_state.oauth_state = {
                            "provider": "google",
                            "user_type": user_type,
                            "initiated_at": time.time()
                        }
                        
                        # Display success message and instructions
                        st.success("✅ Google login URL generated successfully!")
                        
                        # Create expandable section with instructions
                        with st.expander("📋 Login Instructions", expanded=True):
                            st.markdown("""
                            **How to complete Google login:**
                            1. Click the link below to open Google authentication
                            2. Sign in with your Google account
                            3. Grant permissions to the application
                            4. You will be redirected back automatically
                            """)
                            
                            # Display clickable link
                            st.markdown(f"🔗 **[Click here to login with Google]({auth_url})**")
                            
                            # JavaScript to open popup (if browser supports it)
                            st.components.v1.html(f"""
                            <script>
                            function openGoogleLogin() {{
                                window.open('{auth_url}', 'google_login', 'width=500,height=600,scrollbars=yes,resizable=yes');
                            }}
                            </script>
                            <button onclick="openGoogleLogin()" style="
                                background-color: #4285f4;
                                color: white;
                                border: none;
                                padding: 10px 20px;
                                border-radius: 5px;
                                cursor: pointer;
                                font-size: 16px;
                                margin-top: 10px;
                            ">🚀 Open in Popup Window</button>
                            """, height=80)
        else:
            st.button("🔍 Google Login", disabled=True, use_container_width=True)
            st.caption("⚠️ Google OAuth not configured")
    
    with col2:
        if config_status["facebook_configured"]:
            if st.button(
                "📘 Continue with Facebook", 
                key=f"facebook_login_{user_type}", 
                use_container_width=True,
                type="primary"
            ):
                with st.spinner("🔄 Connecting to Facebook..."):
                    auth_url = oauth_manager.initiate_facebook_login(user_type)
                    
                    if auth_url:
                        # Store OAuth state in session
                        st.session_state.oauth_state = {
                            "provider": "facebook",
                            "user_type": user_type,
                            "initiated_at": time.time()
                        }
                        
                        # Display success message and instructions
                        st.success("✅ Facebook login URL generated successfully!")
                        
                        # Create expandable section with instructions
                        with st.expander("📋 Login Instructions", expanded=True):
                            st.markdown("""
                            **How to complete Facebook login:**
                            1. Click the link below to open Facebook authentication
                            2. Sign in with your Facebook account
                            3. Grant permissions to the application
                            4. You will be redirected back automatically
                            """)
                            
                            # Display clickable link
                            st.markdown(f"🔗 **[Click here to login with Facebook]({auth_url})**")
                            
                            # JavaScript to open popup (if browser supports it)
                            st.components.v1.html(f"""
                            <script>
                            function openFacebookLogin() {{
                                window.open('{auth_url}', 'facebook_login', 'width=500,height=600,scrollbars=yes,resizable=yes');
                            }}
                            </script>
                            <button onclick="openFacebookLogin()" style="
                                background-color: #1877f2;
                                color: white;
                                border: none;
                                padding: 10px 20px;
                                border-radius: 5px;
                                cursor: pointer;
                                font-size: 16px;
                                margin-top: 10px;
                            ">🚀 Open in Popup Window</button>
                            """, height=80)
        else:
            st.button("📘 Facebook Login", disabled=True, use_container_width=True)
            st.caption("⚠️ Facebook OAuth not configured")
    
    # Display configuration status for debugging
    if st.checkbox("🔧 Show OAuth Configuration Status", key=f"show_config_{user_type}"):
        st.json(config_status)

def handle_oauth_callback():
    """
    FIXED: Handle OAuth callback from URL parameters
    - Improved error handling
    - Better user feedback
    - Proper session management
    """
    # Check URL parameters for OAuth callback
    query_params = st.experimental_get_query_params()
    
    if "auth" in query_params:
        auth_status = query_params["auth"][0]
        provider = query_params.get("provider", ["unknown"])[0]
        user_type = query_params.get("user_type", ["individual"])[0]
        
        if auth_status == "success":
            # Clear URL parameters
            st.experimental_set_query_params()
            
            # Display success message
            st.success(f"🎉 {provider.title()} authentication successful! Welcome to Haven!")
            st.balloons()
            
            # Update session state
            st.session_state.authenticated = True
            st.session_state.auth_provider = provider
            st.session_state.user_type = user_type
            st.session_state.auth_time = time.time()
            
            # Clear OAuth state
            if "oauth_state" in st.session_state:
                del st.session_state.oauth_state
            
            # Auto-redirect to dashboard after a short delay
            time.sleep(2)
            st.experimental_rerun()
            
        elif auth_status == "error":
            # Clear URL parameters
            st.experimental_set_query_params()
            
            error_message = query_params.get("message", ["Unknown error"])[0]
            
            # Display error message
            st.error(f"❌ {provider.title()} authentication failed: {error_message}")
            
            # Provide helpful suggestions
            st.info("""
            💡 **Troubleshooting tips:**
            - Make sure you have a stable internet connection
            - Try clearing your browser cache and cookies
            - Ensure popup blockers are disabled
            - Contact support if the problem persists
            """)
            
            # Clear OAuth state
            if "oauth_state" in st.session_state:
                del st.session_state.oauth_state

def check_authentication_status():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_user_info():
    """Get authenticated user information"""
    if check_authentication_status():
        return {
            "provider": st.session_state.get("auth_provider"),
            "user_type": st.session_state.get("user_type"),
            "auth_time": st.session_state.get("auth_time")
        }
    return None

def logout():
    """Logout user and clear session"""
    # Clear authentication state
    if "authenticated" in st.session_state:
        del st.session_state.authenticated
    if "auth_provider" in st.session_state:
        del st.session_state.auth_provider
    if "user_type" in st.session_state:
        del st.session_state.user_type
    if "auth_time" in st.session_state:
        del st.session_state.auth_time
    if "oauth_state" in st.session_state:
        del st.session_state.oauth_state
    
    st.success("👋 You have been logged out successfully!")
    st.experimental_rerun()

