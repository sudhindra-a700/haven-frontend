"""
UPDATED Enhanced Authentication Utilities for HAVEN Workflow-Based Frontend
Integrates with the fixed OAuth authentication system
Handles OAuth and email authentication with role-based registration and access control
"""

import streamlit as st
import requests
import logging
import hashlib
import secrets
import time
from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timedelta

# Import the fixed OAuth integration
from oauth_integration import (
    OAuthManager, 
    check_authentication_status, 
    get_user_info, 
    logout,
    handle_oauth_callback
)

logger = logging.getLogger(__name__)

class AuthenticationManager:
    """UPDATED: Manages authentication state and operations for workflow-based frontend with role-based access"""
    
    def __init__(self):
        # Use fixed OAuth manager
        self.oauth_manager = OAuthManager()
        self.backend_url = self.oauth_manager.backend_url
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 5
        
        # Initialize authentication state
        self.initialize_auth_state()
        
        logger.info("UPDATED AuthenticationManager initialized with fixed OAuth integration")
    
    def _get_backend_url(self) -> str:
        """UPDATED: Get backend URL from fixed OAuth configuration"""
        return self.oauth_manager.backend_url
    
    def initialize_auth_state(self):
        """UPDATED: Initialize authentication-related session state with role-based fields"""
        
        # OAuth-related state (compatible with fixed OAuth integration)
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        
        if 'auth_provider' not in st.session_state:
            st.session_state.auth_provider = None
        
        if 'user_type' not in st.session_state:
            st.session_state.user_type = None
        
        if 'auth_time' not in st.session_state:
            st.session_state.auth_time = None
        
        # Legacy authentication state (for backward compatibility)
        if 'auth_token' not in st.session_state:
            st.session_state.auth_token = None
        
        if 'auth_expires' not in st.session_state:
            st.session_state.auth_expires = 0
        
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
        
        if 'last_login_attempt' not in st.session_state:
            st.session_state.last_login_attempt = 0
        
        if 'oauth_state' not in st.session_state:
            st.session_state.oauth_state = None
        
        # Role-based authentication state
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        
        if 'is_registered' not in st.session_state:
            st.session_state.is_registered = False
        
        if 'registration_type' not in st.session_state:
            st.session_state.registration_type = None
        
        if 'user_authenticated' not in st.session_state:
            st.session_state.user_authenticated = False
        
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
    
    def check_authentication(self) -> bool:
        """UPDATED: Check if user is currently authenticated using fixed OAuth system"""
        
        # First check OAuth authentication status
        oauth_authenticated = check_authentication_status()
        
        if oauth_authenticated:
            # Update legacy session state for backward compatibility
            st.session_state.user_authenticated = True
            
            # Get user info from OAuth system
            user_info = get_user_info()
            if user_info:
                st.session_state.user_role = user_info.get('user_type', 'individual')
                st.session_state.auth_provider = user_info.get('provider')
            
            return True
        
        # Check legacy token authentication (for backward compatibility)
        if not st.session_state.user_authenticated:
            return False
        
        # Check token expiration
        if st.session_state.auth_token:
            return self._validate_token(st.session_state.auth_token)
        
        return True
    
    def logout_user(self):
        """UPDATED: Logout user and clear all session state"""
        
        # Use fixed OAuth logout
        logout()
        
        # Clear legacy session state
        st.session_state.auth_token = None
        st.session_state.auth_expires = 0
        st.session_state.user_authenticated = False
        st.session_state.user_role = None
        st.session_state.is_registered = False
        st.session_state.registration_type = None
        st.session_state.user_data = None
        st.session_state.oauth_state = None
        
        logger.info("User logged out successfully")
        return False
    
    def _validate_token(self, token: str) -> bool:
        """UPDATED: Validate authentication token with backend using fixed API endpoints"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            # Use fixed API endpoint with /api/v1 prefix
            response = requests.get(
                f"{self.backend_url}/api/v1/auth/registration-status",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # Update session state with latest user info
                st.session_state.user_role = data.get('role')
                st.session_state.is_registered = data.get('is_registered', False)
                st.session_state.registration_type = data.get('registration_type')
                return True
            else:
                return False
                
        except Exception as e:
            logger.warning(f"Token validation failed: {e}")
            return False
    
    def login_user(self, method: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """UPDATED: Login user with specified method (OAuth or email)"""
        
        self.initialize_auth_state()
        
        # Check rate limiting
        if not self._check_rate_limit():
            return False, "Too many login attempts. Please try again later."
        
        try:
            if method == 'email':
                return self._login_with_email(credentials)
            elif method in ['google', 'facebook']:
                return self._login_with_oauth(method, credentials)
            else:
                return False, "Unsupported login method"
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False, f"Login failed: {str(e)}"
    
    def _check_rate_limit(self) -> bool:
        """Check if user has exceeded login attempt rate limit"""
        current_time = time.time()
        
        # Reset attempts if enough time has passed
        if current_time - st.session_state.last_login_attempt > 300:  # 5 minutes
            st.session_state.login_attempts = 0
        
        if st.session_state.login_attempts >= self.max_login_attempts:
            return False
        
        st.session_state.last_login_attempt = current_time
        st.session_state.login_attempts += 1
        return True
    
    def _login_with_email(self, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """UPDATED: Login with email using fixed API endpoints"""
        
        email = credentials.get('email')
        password = credentials.get('password')
        user_type = credentials.get('user_type', 'individual')
        
        if not email or not password:
            return False, "Email and password are required"
        
        try:
            # Use fixed API endpoint with /api/v1 prefix
            response = requests.post(
                f"{self.backend_url}/api/v1/auth/email/login",
                json={
                    'email': email,
                    'password': password,
                    'user_type': user_type
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Update session state
                st.session_state.auth_token = data.get('access_token')
                st.session_state.auth_expires = time.time() + self.session_timeout
                st.session_state.user_authenticated = True
                st.session_state.user_role = user_type
                st.session_state.user_data = data.get('user_data')
                st.session_state.login_attempts = 0
                
                logger.info(f"Email login successful for user: {email}")
                return True, data
            else:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('detail', 'Login failed')
                return False, error_msg
                
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to authentication server"
        except requests.exceptions.Timeout:
            return False, "Authentication server timeout"
        except Exception as e:
            logger.error(f"Email login error: {e}")
            return False, f"Login failed: {str(e)}"
    
    def _login_with_oauth(self, provider: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """UPDATED: Login with OAuth using fixed OAuth integration"""
        
        user_type = credentials.get('user_type', 'individual')
        
        try:
            # Use fixed OAuth manager
            if provider == 'google':
                auth_url = self.oauth_manager.initiate_google_login(user_type)
            elif provider == 'facebook':
                auth_url = self.oauth_manager.initiate_facebook_login(user_type)
            else:
                return False, f"Unsupported OAuth provider: {provider}"
            
            if auth_url:
                # Store OAuth state
                st.session_state.oauth_state = {
                    'provider': provider,
                    'user_type': user_type,
                    'initiated_at': time.time()
                }
                
                return True, {'auth_url': auth_url, 'provider': provider}
            else:
                return False, f"Failed to initiate {provider} authentication"
                
        except Exception as e:
            logger.error(f"OAuth login error: {e}")
            return False, f"OAuth login failed: {str(e)}"
    
    def register_user(self, registration_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """UPDATED: Register user with fixed API endpoints"""
        
        try:
            # Use fixed API endpoint with /api/v1 prefix
            response = requests.post(
                f"{self.backend_url}/api/v1/auth/register",
                json=registration_data,
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                
                # Update session state
                st.session_state.is_registered = True
                st.session_state.registration_type = registration_data.get('user_type')
                st.session_state.user_data = data.get('user_data')
                
                logger.info(f"User registration successful: {registration_data.get('email')}")
                return True, data
            else:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('detail', 'Registration failed')
                return False, error_msg
                
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to registration server"
        except requests.exceptions.Timeout:
            return False, "Registration server timeout"
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, f"Registration failed: {str(e)}"
    
    def get_registration_status(self) -> Dict[str, Any]:
        """UPDATED: Get user registration status using fixed API endpoints"""
        
        if not self.check_authentication():
            return {'error': 'User not authenticated'}
        
        try:
            headers = {}
            
            # Use OAuth authentication if available
            if st.session_state.authenticated and st.session_state.auth_token:
                headers['Authorization'] = f'Bearer {st.session_state.auth_token}'
            
            # Use fixed API endpoint with /api/v1 prefix
            response = requests.get(
                f"{self.backend_url}/api/v1/auth/registration-status",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Failed to get registration status'}
                
        except Exception as e:
            logger.error(f"Registration status check error: {e}")
            return {'error': f'Registration status check failed: {str(e)}'}
    
    def require_authentication(self, redirect_to_login: bool = True) -> bool:
        """UPDATED: Decorator-like function to require authentication"""
        
        if not self.check_authentication():
            if redirect_to_login:
                st.warning("🔐 Please log in to access this feature")
                st.stop()
            return False
        return True
    
    def require_role(self, required_roles: list, redirect_to_login: bool = True) -> bool:
        """UPDATED: Require specific user roles"""
        
        if not self.require_authentication(redirect_to_login):
            return False
        
        user_role = st.session_state.user_role
        if user_role not in required_roles:
            st.error(f"❌ Access denied. Required roles: {', '.join(required_roles)}")
            st.stop()
            return False
        
        return True
    
    def get_user_role(self) -> Optional[str]:
        """Get current user role"""
        if self.check_authentication():
            return st.session_state.user_role
        return None
    
    def get_user_data(self) -> Optional[Dict[str, Any]]:
        """Get current user data"""
        if self.check_authentication():
            return st.session_state.user_data
        return None
    
    def is_organization(self) -> bool:
        """Check if current user is an organization"""
        return self.get_user_role() == 'organization'
    
    def is_individual(self) -> bool:
        """Check if current user is an individual"""
        return self.get_user_role() == 'individual'

# Utility functions for easy access
def get_auth_manager() -> AuthenticationManager:
    """Get or create authentication manager instance"""
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthenticationManager()
    return st.session_state.auth_manager

def require_auth(redirect_to_login: bool = True) -> bool:
    """Require authentication for current page"""
    auth_manager = get_auth_manager()
    return auth_manager.require_authentication(redirect_to_login)

def require_role(roles: list, redirect_to_login: bool = True) -> bool:
    """Require specific roles for current page"""
    auth_manager = get_auth_manager()
    return auth_manager.require_role(roles, redirect_to_login)

def get_current_user_role() -> Optional[str]:
    """Get current user role"""
    auth_manager = get_auth_manager()
    return auth_manager.get_user_role()

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    auth_manager = get_auth_manager()
    return auth_manager.check_authentication()

