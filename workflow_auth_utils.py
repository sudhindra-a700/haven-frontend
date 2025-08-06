"""
Enhanced Authentication Utilities for HAVEN Workflow-Based Frontend
Handles OAuth and email authentication with role-based registration and access control
"""

import streamlit as st
import requests
import logging
from typing import Dict, Any, Tuple, Optional
import time
import hashlib
import secrets
from datetime import datetime

logger = logging.getLogger(__name__)

class AuthenticationManager:
    """Manages authentication state and operations for workflow-based frontend with role-based access"""
    
    def __init__(self):
        self.backend_url = self._get_backend_url()
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 5
    
    def _get_backend_url(self) -> str:
        """Get backend URL from configuration"""
        try:
            return st.secrets.get("BACKEND_URL", "http://localhost:8000")
        except:
            return "http://localhost:8000"
    
    def initialize_auth_state(self):
        """Initialize authentication-related session state with role-based fields"""
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
        
        # NEW: Role-based authentication state
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
        """Check if user is currently authenticated"""
        if not st.session_state.user_authenticated:
            return False
        
        # Check token expiration
        if st.session_state.auth_expires < time.time():
            self.logout_user()
            return False
        
        # Validate token with backend if available
        if st.session_state.auth_token:
            return self._validate_token(st.session_state.auth_token)
        
        return True
    
    def _validate_token(self, token: str) -> bool:
        """Validate authentication token with backend"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
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
            return False
        except Exception as e:
            logger.warning(f"Token validation failed: {e}")
            return False
    
    def login_user(self, method: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """Login user with specified method"""
        self.initialize_auth_state()
        
        # Check rate limiting
        if not self._check_rate_limit():
            return False, "Too many login attempts. Please try again later."
        
        try:
            if method == 'email':
                return self._login_email(credentials)
            elif method == 'google':
                return self._login_oauth('google', credentials)
            elif method == 'facebook':
                return self._login_oauth('facebook', credentials)
            else:
                return False, f"Unsupported login method: {method}"
        
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
        
        return True
    
    def _login_email(self, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """Login with email and password"""
        try:
            # Record login attempt
            st.session_state.login_attempts += 1
            st.session_state.last_login_attempt = time.time()
            
            # Make login request to backend
            response = requests.post(
                f"{self.backend_url}/api/v1/auth/login",
                json={
                    "email": credentials.get('email'),
                    "password": credentials.get('password')
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self._set_auth_session(data)
                return True, "Login successful"
            elif response.status_code == 401:
                return False, "Invalid email or password"
            elif response.status_code == 403:
                return False, "Account not activated or registration incomplete"
            else:
                return False, f"Login failed: {response.text}"
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Login request failed: {e}")
            return False, "Unable to connect to authentication server"
    
    def _login_oauth(self, provider: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
        """Login with OAuth provider"""
        try:
            # Record login attempt
            st.session_state.login_attempts += 1
            st.session_state.last_login_attempt = time.time()
            
            # Make OAuth login request to backend
            response = requests.post(
                f"{self.backend_url}/api/v1/oauth/{provider}/callback",
                json=credentials,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self._set_auth_session(data)
                return True, f"{provider.title()} login successful"
            else:
                return False, f"{provider.title()} login failed"
        
        except requests.exceptions.RequestException as e:
            logger.error(f"OAuth login failed: {e}")
            return False, f"Unable to connect to {provider.title()} authentication"
    
    def _set_auth_session(self, auth_data: Dict[str, Any]):
        """Set authentication session data"""
        st.session_state.auth_token = auth_data.get('access_token')
        st.session_state.auth_expires = time.time() + self.session_timeout
        st.session_state.user_authenticated = True
        st.session_state.user_data = auth_data.get('user', {})
        st.session_state.user_role = auth_data.get('user', {}).get('role')
        st.session_state.is_registered = auth_data.get('user', {}).get('is_registered', False)
        
        # Determine registration type based on role
        if st.session_state.user_role == 'individual':
            st.session_state.registration_type = 'individual'
        elif st.session_state.user_role == 'organization':
            st.session_state.registration_type = 'organization'
        
        # Reset login attempts on successful login
        st.session_state.login_attempts = 0
    
    def logout_user(self):
        """Logout user and clear session"""
        st.session_state.auth_token = None
        st.session_state.auth_expires = 0
        st.session_state.user_authenticated = False
        st.session_state.user_data = None
        st.session_state.user_role = None
        st.session_state.is_registered = False
        st.session_state.registration_type = None
        st.session_state.oauth_state = None
    
    # NEW: Registration methods
    
    def register_individual(self, registration_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Register a new individual user"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/auth/register/individual",
                json=registration_data,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                self._set_auth_session(data)
                return True, "Individual registration successful"
            elif response.status_code == 400:
                error_data = response.json()
                return False, error_data.get('detail', 'Registration failed')
            else:
                return False, f"Registration failed: {response.text}"
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Individual registration failed: {e}")
            return False, "Unable to connect to registration server"
    
    def register_organization(self, registration_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Register a new organization user"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/auth/register/organization",
                json=registration_data,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                self._set_auth_session(data)
                return True, "Organization registration successful"
            elif response.status_code == 400:
                error_data = response.json()
                return False, error_data.get('detail', 'Registration failed')
            else:
                return False, f"Registration failed: {response.text}"
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Organization registration failed: {e}")
            return False, "Unable to connect to registration server"
    
    def get_registration_status(self) -> Dict[str, Any]:
        """Get current user's registration status"""
        if not st.session_state.auth_token:
            return {"needs_registration": True, "available_types": ["individual", "organization"]}
        
        try:
            headers = {'Authorization': f'Bearer {st.session_state.auth_token}'}
            response = requests.get(
                f"{self.backend_url}/api/v1/auth/registration-status",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"needs_registration": True, "available_types": ["individual", "organization"]}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get registration status: {e}")
            return {"needs_registration": True, "available_types": ["individual", "organization"]}
    
    # NEW: Role-based access control methods
    
    def is_individual(self) -> bool:
        """Check if current user is an individual"""
        return st.session_state.user_role == 'individual' and st.session_state.is_registered
    
    def is_organization(self) -> bool:
        """Check if current user is an organization"""
        return st.session_state.user_role == 'organization' and st.session_state.is_registered
    
    def is_admin(self) -> bool:
        """Check if current user is an admin"""
        return st.session_state.user_role == 'admin'
    
    def is_moderator(self) -> bool:
        """Check if current user is a moderator or admin"""
        return st.session_state.user_role in ['moderator', 'admin']
    
    def can_donate(self) -> bool:
        """Check if current user can donate (individuals only)"""
        return self.is_individual()
    
    def can_create_campaigns(self) -> bool:
        """Check if current user can create campaigns (organizations only)"""
        return self.is_organization()
    
    def needs_registration(self) -> bool:
        """Check if current user needs to complete registration"""
        return st.session_state.user_authenticated and not st.session_state.is_registered
    
    def get_user_role_display(self) -> str:
        """Get user role for display purposes"""
        role_map = {
            'individual': 'Individual Donor',
            'organization': 'Organization',
            'admin': 'Administrator',
            'moderator': 'Moderator'
        }
        return role_map.get(st.session_state.user_role, 'Unknown')
    
    def get_allowed_features(self) -> Dict[str, bool]:
        """Get features allowed for current user role"""
        if not st.session_state.user_authenticated:
            return {
                'view_campaigns': True,
                'donate': False,
                'create_campaigns': False,
                'manage_campaigns': False,
                'admin_panel': False
            }
        
        if self.is_individual():
            return {
                'view_campaigns': True,
                'donate': True,
                'create_campaigns': False,
                'manage_campaigns': False,
                'admin_panel': False
            }
        elif self.is_organization():
            return {
                'view_campaigns': True,
                'donate': False,
                'create_campaigns': True,
                'manage_campaigns': True,
                'admin_panel': False
            }
        elif self.is_admin():
            return {
                'view_campaigns': True,
                'donate': False,
                'create_campaigns': True,
                'manage_campaigns': True,
                'admin_panel': True
            }
        else:
            return {
                'view_campaigns': True,
                'donate': False,
                'create_campaigns': False,
                'manage_campaigns': False,
                'admin_panel': False
            }

# Global authentication manager instance
auth_manager = AuthenticationManager()

# Utility functions for easy access
def initialize_auth():
    """Initialize authentication state"""
    auth_manager.initialize_auth_state()

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return auth_manager.check_authentication()

def login_user(method: str, credentials: Dict[str, Any]) -> Tuple[bool, Any]:
    """Login user"""
    return auth_manager.login_user(method, credentials)

def logout_user():
    """Logout user"""
    auth_manager.logout_user()

def register_individual(data: Dict[str, Any]) -> Tuple[bool, Any]:
    """Register individual user"""
    return auth_manager.register_individual(data)

def register_organization(data: Dict[str, Any]) -> Tuple[bool, Any]:
    """Register organization user"""
    return auth_manager.register_organization(data)

def get_registration_status() -> Dict[str, Any]:
    """Get registration status"""
    return auth_manager.get_registration_status()

def is_individual() -> bool:
    """Check if user is individual"""
    return auth_manager.is_individual()

def is_organization() -> bool:
    """Check if user is organization"""
    return auth_manager.is_organization()

def can_donate() -> bool:
    """Check if user can donate"""
    return auth_manager.can_donate()

def can_create_campaigns() -> bool:
    """Check if user can create campaigns"""
    return auth_manager.can_create_campaigns()

def needs_registration() -> bool:
    """Check if user needs registration"""
    return auth_manager.needs_registration()

def get_user_role_display() -> str:
    """Get user role display name"""
    return auth_manager.get_user_role_display()

def get_allowed_features() -> Dict[str, bool]:
    """Get allowed features for current user"""
    return auth_manager.get_allowed_features()

