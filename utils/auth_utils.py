"""
Authentication utilities for HAVEN Crowdfunding Platform
Matches the repository structure of sudhindra-a700/haven-frontend
"""

import streamlit as st
import requests
import hashlib
import time
from typing import Dict, Any, Optional, Tuple
import logging
from .config import get_config, get_api_endpoint

logger = logging.getLogger(__name__)

class AuthenticationManager:
    """Manages user authentication and session handling"""
    
    def __init__(self):
        self.config = get_config()
        self.session_timeout = self.config.get('security.session_timeout', 3600)
        self.max_login_attempts = self.config.get('security.max_login_attempts', 5)
    
    def login(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Authenticate user with email and password
        Returns: (success, message, user_data)
        """
        try:
            # Check login attempts
            if self._is_login_blocked(email):
                return False, "Too many failed login attempts. Please try again later.", None
            
            # Validate input
            if not email or not password:
                return False, "Email and password are required.", None
            
            if not self._is_valid_email(email):
                return False, "Please enter a valid email address.", None
            
            # Hash password for security
            password_hash = self._hash_password(password)
            
            # Prepare login data
            login_data = {
                'email': email,
                'password': password_hash,
                'timestamp': int(time.time())
            }
            
            # Call backend API
            if self.config.is_development_mode() or self.config.get('development.mock_api', False):
                # Mock authentication for development
                success, message, user_data = self._mock_login(email, password)
            else:
                # Real API call
                success, message, user_data = self._api_login(login_data)
            
            # Handle login result
            if success:
                self._create_session(user_data)
                self._clear_login_attempts(email)
                logger.info(f"User {email} logged in successfully")
            else:
                self._record_login_attempt(email)
                logger.warning(f"Failed login attempt for {email}: {message}")
            
            return success, message, user_data
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False, "Login failed due to a system error. Please try again.", None
    
    def oauth_login(self, provider: str, oauth_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Authenticate user with OAuth provider
        Returns: (success, message, user_data)
        """
        try:
            if not self.config.is_oauth_enabled():
                return False, "OAuth authentication is not enabled.", None
            
            # Validate OAuth data
            if not oauth_data.get('email') or not oauth_data.get('id'):
                return False, "Invalid OAuth data received.", None
            
            # Prepare OAuth login data
            login_data = {
                'provider': provider,
                'oauth_id': oauth_data.get('id'),
                'email': oauth_data.get('email'),
                'name': oauth_data.get('name', ''),
                'avatar': oauth_data.get('picture', ''),
                'timestamp': int(time.time())
            }
            
            # Call backend API
            if self.config.is_development_mode():
                # Mock OAuth for development
                success, message, user_data = self._mock_oauth_login(login_data)
            else:
                # Real API call
                success, message, user_data = self._api_oauth_login(login_data)
            
            if success:
                self._create_session(user_data)
                logger.info(f"User {oauth_data.get('email')} logged in via {provider}")
            
            return success, message, user_data
            
        except Exception as e:
            logger.error(f"OAuth login error: {e}")
            return False, "OAuth login failed. Please try again.", None
    
    def register(self, user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Register new user
        Returns: (success, message, user_data)
        """
        try:
            # Validate registration data
            validation_result = self._validate_registration_data(user_data)
            if not validation_result[0]:
                return validation_result
            
            # Hash password
            if 'password' in user_data:
                user_data['password'] = self._hash_password(user_data['password'])
            
            # Add timestamp
            user_data['timestamp'] = int(time.time())
            
            # Call backend API
            if self.config.is_development_mode():
                # Mock registration for development
                success, message, registered_user = self._mock_register(user_data)
            else:
                # Real API call
                success, message, registered_user = self._api_register(user_data)
            
            if success:
                self._create_session(registered_user)
                logger.info(f"User {user_data.get('email')} registered successfully")
            
            return success, message, registered_user
            
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, "Registration failed due to a system error. Please try again.", None
    
    def logout(self):
        """Logout current user and clear session"""
        try:
            user_email = st.session_state.get('user', {}).get('email', 'Unknown')
            
            # Clear session state
            self._clear_session()
            
            # Call backend logout API if needed
            if not self.config.is_development_mode():
                try:
                    self._api_logout()
                except Exception as e:
                    logger.warning(f"Backend logout API call failed: {e}")
            
            logger.info(f"User {user_email} logged out")
            
        except Exception as e:
            logger.error(f"Logout error: {e}")
    
    def check_authentication(self) -> bool:
        """Check if user is authenticated and session is valid"""
        try:
            if not st.session_state.get('authenticated', False):
                return False
            
            # Check session timeout
            login_time = st.session_state.get('login_time', 0)
            current_time = time.time()
            
            if current_time - login_time > self.session_timeout:
                self._clear_session()
                logger.info("Session expired")
                return False
            
            # Update last activity time
            st.session_state.last_activity = current_time
            
            return True
            
        except Exception as e:
            logger.error(f"Authentication check error: {e}")
            return False
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user data"""
        if self.check_authentication():
            return st.session_state.get('user', {})
        return None
    
    def _create_session(self, user_data: Dict[str, Any]):
        """Create user session"""
        current_time = time.time()
        
        st.session_state.authenticated = True
        st.session_state.user = user_data
        st.session_state.login_time = current_time
        st.session_state.last_activity = current_time
        st.session_state.current_page = 'home'
    
    def _clear_session(self):
        """Clear user session"""
        st.session_state.authenticated = False
        st.session_state.user = {}
        st.session_state.current_page = 'login'
        
        # Clear other session data
        for key in ['login_time', 'last_activity', 'oauth_state']:
            if key in st.session_state:
                del st.session_state[key]
    
    def _is_login_blocked(self, email: str) -> bool:
        """Check if login is blocked due to too many attempts"""
        attempts_key = f"login_attempts_{email}"
        attempts = st.session_state.get(attempts_key, [])
        
        # Remove old attempts (older than 1 hour)
        current_time = time.time()
        attempts = [t for t in attempts if current_time - t < 3600]
        st.session_state[attempts_key] = attempts
        
        return len(attempts) >= self.max_login_attempts
    
    def _record_login_attempt(self, email: str):
        """Record failed login attempt"""
        attempts_key = f"login_attempts_{email}"
        attempts = st.session_state.get(attempts_key, [])
        attempts.append(time.time())
        st.session_state[attempts_key] = attempts
    
    def _clear_login_attempts(self, email: str):
        """Clear login attempts for successful login"""
        attempts_key = f"login_attempts_{email}"
        if attempts_key in st.session_state:
            del st.session_state[attempts_key]
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _hash_password(self, password: str) -> str:
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _validate_registration_data(self, user_data: Dict[str, Any]) -> Tuple[bool, str, None]:
        """Validate user registration data"""
        required_fields = ['name', 'email', 'password']
        
        for field in required_fields:
            if not user_data.get(field):
                return False, f"{field.title()} is required.", None
        
        if not self._is_valid_email(user_data['email']):
            return False, "Please enter a valid email address.", None
        
        password = user_data['password']
        min_length = self.config.get('security.password_min_length', 8)
        
        if len(password) < min_length:
            return False, f"Password must be at least {min_length} characters long.", None
        
        return True, "Validation passed.", None
    
    def _mock_login(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Mock login for development"""
        # Simple mock authentication
        if "@" in email and len(password) >= 6:
            user_data = {
                'id': 'mock_user_123',
                'name': email.split('@')[0].title(),
                'email': email,
                'avatar': '👤',
                'role': 'user',
                'verified': True
            }
            return True, "Login successful!", user_data
        else:
            return False, "Invalid email or password.", None
    
    def _mock_oauth_login(self, oauth_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Mock OAuth login for development"""
        user_data = {
            'id': f"mock_{oauth_data['provider']}_{oauth_data['oauth_id']}",
            'name': oauth_data.get('name', 'OAuth User'),
            'email': oauth_data['email'],
            'avatar': oauth_data.get('avatar', '👤'),
            'role': 'user',
            'verified': True,
            'oauth_provider': oauth_data['provider']
        }
        return True, f"{oauth_data['provider'].title()} login successful!", user_data
    
    def _mock_register(self, user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Mock registration for development"""
        registered_user = {
            'id': f"mock_user_{int(time.time())}",
            'name': user_data['name'],
            'email': user_data['email'],
            'avatar': '👤',
            'role': 'user',
            'verified': False
        }
        return True, "Registration successful!", registered_user
    
    def _api_login(self, login_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Call backend login API"""
        try:
            url = get_api_endpoint('auth') + '/login'
            response = requests.post(url, json=login_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return True, result.get('message', 'Login successful!'), result.get('user')
            else:
                error_msg = response.json().get('detail', 'Login failed.')
                return False, error_msg, None
                
        except requests.RequestException as e:
            logger.error(f"API login error: {e}")
            return False, "Unable to connect to authentication service.", None
    
    def _api_oauth_login(self, oauth_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Call backend OAuth login API"""
        try:
            url = get_api_endpoint('auth') + '/oauth/login'
            response = requests.post(url, json=oauth_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return True, result.get('message', 'OAuth login successful!'), result.get('user')
            else:
                error_msg = response.json().get('detail', 'OAuth login failed.')
                return False, error_msg, None
                
        except requests.RequestException as e:
            logger.error(f"API OAuth login error: {e}")
            return False, "Unable to connect to authentication service.", None
    
    def _api_register(self, user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Call backend registration API"""
        try:
            url = get_api_endpoint('auth') + '/register'
            response = requests.post(url, json=user_data, timeout=30)
            
            if response.status_code == 201:
                result = response.json()
                return True, result.get('message', 'Registration successful!'), result.get('user')
            else:
                error_msg = response.json().get('detail', 'Registration failed.')
                return False, error_msg, None
                
        except requests.RequestException as e:
            logger.error(f"API registration error: {e}")
            return False, "Unable to connect to registration service.", None
    
    def _api_logout(self):
        """Call backend logout API"""
        try:
            url = get_api_endpoint('auth') + '/logout'
            user_id = st.session_state.get('user', {}).get('id')
            
            if user_id:
                response = requests.post(url, json={'user_id': user_id}, timeout=10)
                if response.status_code != 200:
                    logger.warning(f"Backend logout failed: {response.status_code}")
                    
        except requests.RequestException as e:
            logger.warning(f"Backend logout API error: {e}")

# Global authentication manager instance
auth_manager = AuthenticationManager()

def login(email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Login user with email and password"""
    return auth_manager.login(email, password)

def oauth_login(provider: str, oauth_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Login user with OAuth"""
    return auth_manager.oauth_login(provider, oauth_data)

def register(user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Register new user"""
    return auth_manager.register(user_data)

def logout_user():
    """Logout current user"""
    auth_manager.logout()

def check_authentication() -> bool:
    """Check if user is authenticated"""
    return auth_manager.check_authentication()

def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current user data"""
    return auth_manager.get_current_user()

def require_authentication():
    """Decorator/function to require authentication"""
    if not check_authentication():
        st.error("Please log in to access this page.")
        st.stop()

def is_admin() -> bool:
    """Check if current user is admin"""
    user = get_current_user()
    return user and user.get('role') == 'admin'

