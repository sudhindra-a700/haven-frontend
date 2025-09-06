""" 
Updated OAuth Integration for HAVEN Crowdfunding Platform Frontend

This file contains the corrected OAuth implementation that works with the new backend API
and properly handles the popup-based OAuth flow for Streamlit applications.
"""

import streamlit as st
import requests
import os
import logging
import time
import jwt
import json
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs

# Configure logging
logger = logging.getLogger(__name__)

class OAuthManager:
    """OAuth Manager for handling Google and Facebook authentication with Streamlit"""
    
    def __init__(self):
        # Use environment variables with fallbacks
        self.backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8501")
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.facebook_app_id = os.getenv("FACEBOOK_APP_ID")
        
        # Ensure backend URL doesn't end with slash
        if self.backend_url.endswith('/'):
            self.backend_url = self.backend_url[:-1]
        
        logger.info(f"OAuth Manager initialized with backend: {self.backend_url}")

    def check_oauth_config(self) -> Dict[str, bool]:
        """Check if OAuth is properly configured"""
        try:
            response = requests.get(f"{self.backend_url}/api/v1/auth/status", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"oauth_enabled": False, "error": f"Backend returned {response.status_code}"}
        except requests.exceptions.ConnectionError:
            return {"oauth_enabled": False, "error": "Cannot connect to backend"}
        except Exception as e:
            logger.error(f"Auth status check failed: {str(e)}")
            return {"oauth_enabled": False, "error": str(e)}

    def test_backend_connection(self) -> bool:
        """Test connection to backend"""
        try:
            response = requests.get(f"{self.backend_url}/api/v1/auth/status", timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Backend connection test failed: {str(e)}")
            return False

    def initiate_google_login(self, user_type: str = "individual") -> Optional[str]:
        """Get Google OAuth URL from backend API"""
        try:
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
            st.error(f"❌ Cannot connect to authentication server at {self.backend_url}")
            return None
        except requests.exceptions.Timeout:
            st.error(f"❌ Authentication server timeout. Please try again.")
            return None
        except Exception as e:
            logger.error(f"Google OAuth initiation error: {str(e)}")
            st.error(f"❌ Failed to initiate Google login: {str(e)}")
            return None

    def initiate_facebook_login(self, user_type: str = "individual") -> Optional[str]:
        """Get Facebook OAuth URL from backend API"""
        try:
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
            st.error(f"❌ Cannot connect to authentication server at {self.backend_url}")
            return None
        except requests.exceptions.Timeout:
            st.error(f"❌ Authentication server timeout. Please try again.")
            return None
        except Exception as e:
            logger.error(f"Facebook OAuth initiation error: {str(e)}")
            st.error(f"❌ Failed to initiate Facebook login: {str(e)}")
            return None

    def handle_oauth_callback(self) -> bool:
        """Handle OAuth callback parameters from URL"""
        try:
            # Check for OAuth callback parameters in URL
            query_params = st.query_params()
            
            if "auth" in query_params:
                auth_status = query_params["auth"][0]
                
                if auth_status == "success":
                    # Handle successful OAuth
                    if "token" in query_params:
                        jwt_token = query_params["token"][0]
                        
                        # Decode and validate JWT token
                        try:
                            # Note: In production, use proper JWT validation with secret key
                            decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})
                            
                            # Store authentication data in session
                            st.session_state.authenticated = True
                            st.session_state.jwt_token = jwt_token
                            st.session_state.user_data = {
                                "id": decoded_token.get("user_id"),
                                "email": decoded_token.get("email"),
                                "name": decoded_token.get("name"),
                                "provider": decoded_token.get("provider"),
                                "user_type": decoded_token.get("user_type")
                            }
                            
                            # Clear OAuth state
                            if hasattr(st.session_state, 'oauth_state'):
                                del st.session_state.oauth_state
                            
                            # Clear URL parameters
                            st.query_params.clear()
                            
                            st.success(f"✅ Successfully signed in with {decoded_token.get('provider', 'OAuth')}!")
                            st.balloons()
                            
                            # Set current page to dashboard
                            st.session_state.current_page = "dashboard"
                            
                            # Trigger page rerun to update UI
                            time.sleep(2)
                            st.experimental_rerun()
                            
                            return True
                            
                        except jwt.InvalidTokenError:
                            st.error("❌ Invalid authentication token received")
                            return False
                    else:
                        st.error("❌ No authentication token received")
                        return False
                        
                elif auth_status == "error":
                    # Handle OAuth error
                    provider = query_params.get("provider", ["Unknown"])[0]
                    error_message = query_params.get("message", ["Unknown error"])[0]
                    
                    st.error(f"❌ {provider.title()} authentication failed: {error_message}")
                    
                    # Clear URL parameters
                    st.experimental_set_query_params()
                    
                    return False
            
            return False
            
        except Exception as e:
            logger.error(f"OAuth callback handling error: {str(e)}")
            st.error(f"❌ Error processing authentication: {str(e)}")
            return False

    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return getattr(st.session_state, 'authenticated', False)

    def get_user_data(self) -> Optional[Dict[str, Any]]:
        """Get current user data"""
        if self.is_authenticated():
            return getattr(st.session_state, 'user_data', None)
        return None

    def logout(self):
        """Logout current user"""
        # Clear authentication state
        for key in ['authenticated', 'jwt_token', 'user_data', 'oauth_state', 'current_page']:
            if hasattr(st.session_state, key):
                delattr(st.session_state, key)
        
        st.success("✅ Successfully logged out!")
        st.experimental_rerun()

def render_oauth_buttons(user_type: str = "individual"):
    """Render OAuth login buttons with improved Streamlit integration"""
    oauth_manager = OAuthManager()
    
    # Check OAuth configuration
    config_status = oauth_manager.check_oauth_config()
    
    if not config_status.get("oauth_enabled", False):
        st.warning("⚠️ OAuth authentication is currently disabled")
        if "error" in config_status:
            st.error(f"Error: {config_status['error']}")
        st.info("💡 Please ensure the backend service is running and accessible")
        return
    
    st.markdown("### 🔐 Social Login")
    st.markdown("Choose your preferred login method:")
    
    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if config_status.get("google_configured", False):
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
                        
                        # JavaScript to open popup and handle response
                        popup_html = f"""
                        <script>
                        function openGoogleLogin() {{
                            const popup = window.open('{auth_url}', 'google_login', 'width=500,height=600,scrollbars=yes,resizable=yes');
                            
                            // Listen for messages from popup
                            window.addEventListener('message', function(event) {{
                                if (event.data.type === 'OAUTH_SUCCESS') {{
                                    popup.close();
                                    // Redirect to success URL with token
                                    const token = event.data.data.token;
                                    window.location.href = window.location.origin + '?auth=success&token=' + encodeURIComponent(token);
                                }} else if (event.data.type === 'OAUTH_ERROR') {{
                                    popup.close();
                                    // Redirect to error URL
                                    const error = event.data.data.error;
                                    window.location.href = window.location.origin + '?auth=error&provider=google&message=' + encodeURIComponent(error);
                                }}
                            }});
                            
                            // Check if popup was closed manually
                            const checkClosed = setInterval(function() {{
                                if (popup.closed) {{
                                    clearInterval(checkClosed);
                                    console.log('Popup was closed');
                                }}
                            }}, 1000);
                        }}
                        </script>
                        <button onclick="openGoogleLogin()" style="
                            background-color: #4285f4;
                            color: white;
                            border: none;
                            padding: 12px 24px;
                            border-radius: 6px;
                            cursor: pointer;
                            font-size: 16px;
                            font-weight: 500;
                            margin-top: 10px;
                            width: 100%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            gap: 8px;
                        ">
                            <span>🔍</span> Open Google Login Popup
                        </button>
                        """
                        st.components.v1.html(popup_html, height=80)
        else:
            st.caption("🔍 Google OAuth not configured")
    
    with col2:
        if config_status.get("facebook_configured", False):
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
                        
                        # JavaScript to open popup and handle response
                        popup_html = f"""
                        <script>
                        function openFacebookLogin() {{
                            const popup = window.open('{auth_url}', 'facebook_login', 'width=500,height=600,scrollbars=yes,resizable=yes');
                            
                            // Listen for messages from popup
                            window.addEventListener('message', function(event) {{
                                if (event.data.type === 'OAUTH_SUCCESS') {{
                                    popup.close();
                                    // Redirect to success URL with token
                                    const token = event.data.data.token;
                                    window.location.href = window.location.origin + '?auth=success&token=' + encodeURIComponent(token);
                                }} else if (event.data.type === 'OAUTH_ERROR') {{
                                    popup.close();
                                    // Redirect to error URL
                                    const error = event.data.data.error;
                                    window.location.href = window.location.origin + '?auth=error&provider=facebook&message=' + encodeURIComponent(error);
                                }}
                            }});
                            
                            // Check if popup was closed manually
                            const checkClosed = setInterval(function() {{
                                if (popup.closed) {{
                                    clearInterval(checkClosed);
                                    console.log('Popup was closed');
                                }}
                            }}, 1000);
                        }}
                        </script>
                        <button onclick="openFacebookLogin()" style="
                            background-color: #1877f2;
                            color: white;
                            border: none;
                            padding: 12px 24px;
                            border-radius: 6px;
                            cursor: pointer;
                            font-size: 16px;
                            font-weight: 500;
                            margin-top: 10px;
                            width: 100%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            gap: 8px;
                        ">
                            <span>📘</span> Open Facebook Login Popup
                        </button>
                        """
                        st.components.v1.html(popup_html, height=80)
        else:
            st.caption("📘 Facebook OAuth not configured")

def check_authentication_status():
    """Check and handle authentication status"""
    oauth_manager = OAuthManager()
    
    # Handle OAuth callback if present
    oauth_manager.handle_oauth_callback()
    
    # Check if user is authenticated
    if oauth_manager.is_authenticated():
        user_data = oauth_manager.get_user_data()
        
        if user_data:
            return True
    
    return False

def require_authentication():
    """Decorator to require authentication for protected pages"""
    oauth_manager = OAuthManager()
    
    if not oauth_manager.is_authenticated():
        st.error("🔒 This page requires authentication")
        st.info("Please login to access this page")
        
        # Render login options
        render_oauth_buttons()
        
        # Stop execution
        st.stop()
    
    return oauth_manager.get_user_data()

def main_auth_flow():
    """Main authentication flow for standalone use"""
    st.title("🔐 HAVEN Authentication")
    
    # Check authentication status first
    if check_authentication_status():
        # User is authenticated, show main application access
        st.success("✅ You are authenticated!")
        
        oauth_manager = OAuthManager()
        user_data = oauth_manager.get_user_data()
        
        if user_data:
            st.write(f"Welcome, {user_data.get('name', 'User')}!")
            
            # Navigation buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🏠 Dashboard", use_container_width=True):
                    st.session_state.current_page = "dashboard"
                    st.experimental_rerun()
            
            with col2:
                if st.button("💰 Campaigns", use_container_width=True):
                    st.session_state.current_page = "campaigns"
                    st.experimental_rerun()
            
            with col3:
                if st.button("👤 Profile", use_container_width=True):
                    st.session_state.current_page = "profile"
                    st.experimental_rerun()
        
        return
    
    # User is not authenticated, show login options
    st.markdown("### Welcome to HAVEN Crowdfunding Platform")
    st.markdown("Please sign in to access your account and explore campaigns.")
    
    # User type selection
    user_type = st.selectbox(
        "Select your account type:",
        ["individual", "organization"],
        help="Choose whether you're signing in as an individual or representing an organization"
    )
    
    # Render OAuth buttons
    render_oauth_buttons(user_type)

if __name__ == "__main__":
    main_auth_flow()

