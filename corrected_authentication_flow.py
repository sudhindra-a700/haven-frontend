"""
CORRECTED Authentication Flow for HAVEN Crowdfunding Platform
Ensures proper sequence: Registration → Database Storage → Login → Navbar Access

This module provides the corrected authentication flow that:
1. Prevents navbar visibility until user is properly authenticated
2. Ensures user data is stored in database before allowing login
3. Handles both manual registration and OAuth social login
4. Integrates term simplification features
"""

import streamlit as st
import requests
import os
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthenticationManager:
    """Manages the complete authentication flow with proper database integration"""
    
    def __init__(self):
        self.backend_url = os.getenv('BACKEND_URL', 'https://haven-backend-9lw3.onrender.com')
        self.frontend_url = os.getenv('FRONTEND_URL', 'https://haven-frontend-65jr.onrender.com')
        
    def check_user_in_database(self, email: str, user_type: str) -> Tuple[bool, Optional[Dict]]:
        """
        Check if user exists in the appropriate database table
        
        Args:
            email: User's email address
            user_type: 'individual' or 'organization'
            
        Returns:
            Tuple of (exists, user_data)
        """
        try:
            # Determine the correct table based on user type
            table_name = "individuals" if user_type == "individual" else "organizations"
            
            response = requests.get(
                f"{self.backend_url}/api/v1/users/check-existence",
                params={
                    "email": email,
                    "table": table_name
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('exists', False), data.get('user_data')
            else:
                logger.error(f"Error checking user existence: {response.status_code}")
                return False, None
                
        except Exception as e:
            logger.error(f"Exception checking user in database: {e}")
            return False, None
    
    def register_user_in_database(self, user_data: Dict[str, Any]) -> bool:
        """
        Register user in the appropriate database table
        
        Args:
            user_data: Complete user registration data
            
        Returns:
            Success status
        """
        try:
            user_type = user_data.get('user_type', 'individual')
            
            # Prepare data for the correct table
            registration_data = {
                'email': user_data['email'],
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'user_type': user_type,
                'oauth_provider': user_data.get('oauth_provider'),
                'oauth_id': user_data.get('oauth_id'),
                'phone': user_data.get('phone', ''),
                'address': user_data.get('address', ''),
                'city': user_data.get('city', ''),
                'country': user_data.get('country', ''),
                'verification_status': 'pending',
                'created_at': datetime.now().isoformat()
            }
            
            # Add organization-specific fields if applicable
            if user_type == 'organization':
                registration_data.update({
                    'organization_name': user_data.get('organization_name', ''),
                    'organization_type': user_data.get('organization_type', ''),
                    'tax_id': user_data.get('tax_id', ''),
                    'registration_number': user_data.get('registration_number', ''),
                    'website': user_data.get('website', ''),
                    'description': user_data.get('description', '')
                })
            
            # Send registration request to backend
            response = requests.post(
                f"{self.backend_url}/api/v1/users/register",
                json=registration_data,
                timeout=15
            )
            
            if response.status_code == 201:
                logger.info(f"User {user_data['email']} registered successfully in database")
                return True
            else:
                logger.error(f"Registration failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Exception during user registration: {e}")
            return False
    
    def handle_oauth_callback(self) -> Optional[Dict[str, Any]]:
        """
        Handle OAuth callback and ensure user is in database
        
        Returns:
            User data if successful, None otherwise
        """
        try:
            # Check for OAuth callback parameters
            query_params = st.query_params()
            
            if 'code' in query_params and 'state' in query_params:
                auth_code = query_params['code'][0]
                state = query_params['state'][0]
                
                # Parse state to get provider and user_type
                try:
                    state_data = json.loads(state)
                    provider = state_data.get('provider')
                    user_type = state_data.get('user_type')
                except:
                    logger.error("Invalid state parameter in OAuth callback")
                    return None
                
                # Exchange code for user data
                user_data = self.exchange_oauth_code(auth_code, provider, user_type)
                
                if user_data:
                    # Check if user exists in database
                    exists, existing_data = self.check_user_in_database(
                        user_data['email'], 
                        user_type
                    )
                    
                    if not exists:
                        # Register user in database first
                        user_data['user_type'] = user_type
                        user_data['oauth_provider'] = provider
                        
                        if self.register_user_in_database(user_data):
                            logger.info(f"OAuth user {user_data['email']} registered in database")
                        else:
                            st.error("❌ Failed to register user in database. Please try again.")
                            return None
                    
                    # Store user data in session
                    st.session_state.user_data = user_data
                    st.session_state.authenticated = True
                    st.session_state.user_type = user_type
                    
                    # Clear OAuth parameters
                    st.query_params.clear()
                    
                    return user_data
                    
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            st.error(f"❌ OAuth authentication failed: {str(e)}")
        
        return None
    
    def exchange_oauth_code(self, code: str, provider: str, user_type: str) -> Optional[Dict[str, Any]]:
        """
        Exchange OAuth authorization code for user data
        
        Args:
            code: OAuth authorization code
            provider: 'google' or 'facebook'
            user_type: 'individual' or 'organization'
            
        Returns:
            User data if successful
        """
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/auth/{provider}/callback",
                json={
                    'code': code,
                    'user_type': user_type,
                    'redirect_uri': f"{self.frontend_url}"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"OAuth exchange failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"OAuth code exchange error: {e}")
            return None
    
    def is_user_authenticated(self) -> bool:
        """
        Check if user is properly authenticated with database verification
        
        Returns:
            True if user is authenticated and exists in database
        """
        if not st.session_state.get('authenticated', False):
            return False
        
        user_data = st.session_state.get('user_data')
        user_type = st.session_state.get('user_type')
        
        if not user_data or not user_type:
            return False
        
        # Verify user still exists in database
        exists, _ = self.check_user_in_database(user_data['email'], user_type)
        
        if not exists:
            # User no longer exists in database, clear session
            self.logout()
            return False
        
        return True
    
    def get_user_data(self) -> Optional[Dict[str, Any]]:
        """Get current user data from session"""
        if self.is_user_authenticated():
            return st.session_state.get('user_data')
        return None
    
    def get_user_type(self) -> Optional[str]:
        """Get current user type from session"""
        if self.is_user_authenticated():
            return st.session_state.get('user_type')
        return None
    
    def logout(self):
        """Clear authentication session"""
        keys_to_clear = [
            'authenticated', 'user_data', 'user_type', 
            'current_page', 'selected_campaign'
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        logger.info("User logged out successfully")
    
    def require_authentication(self, redirect_to_login: bool = True) -> bool:
        """
        Decorator-like function to require authentication
        
        Args:
            redirect_to_login: Whether to redirect to login page if not authenticated
            
        Returns:
            True if authenticated, False otherwise
        """
        if not self.is_user_authenticated():
            if redirect_to_login:
                st.session_state.current_page = 'login'
                st.warning("🔒 Please log in to access this feature.")
            return False
        return True
    
    def require_role(self, required_role: str) -> bool:
        """
        Check if user has required role
        
        Args:
            required_role: 'individual' or 'organization'
            
        Returns:
            True if user has required role
        """
        if not self.is_user_authenticated():
            return False
        
        user_type = self.get_user_type()
        if user_type != required_role:
            st.error(f"❌ This feature requires {required_role} account.")
            return False
        
        return True

class TermSimplificationManager:
    """Manages term simplification features integration"""
    
    def __init__(self):
        self.backend_url = os.getenv('BACKEND_URL', 'https://haven-backend-9lw3.onrender.com')
        self.simplification_enabled = os.getenv('SIMPLIFICATION_ENABLED', 'true').lower() == 'true'
    
    def simplify_text(self, text: str, preserve_formatting: bool = True) -> Dict[str, Any]:
        """
        Simplify complex text using backend API
        
        Args:
            text: Text to simplify
            preserve_formatting: Whether to preserve original formatting
            
        Returns:
            Simplification result
        """
        if not self.simplification_enabled:
            return {'simplified_text': text, 'simplifications': []}
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/simplify/simplify",
                json={
                    'text': text,
                    'preserve_formatting': preserve_formatting,
                    'max_sentence_length': 20
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Simplification failed: {response.status_code}")
                return {'simplified_text': text, 'simplifications': []}
                
        except Exception as e:
            logger.error(f"Simplification error: {e}")
            return {'simplified_text': text, 'simplifications': []}
    
    def explain_term(self, term: str) -> Dict[str, Any]:
        """
        Get explanation for a specific term
        
        Args:
            term: Term to explain
            
        Returns:
            Term explanation
        """
        if not self.simplification_enabled:
            return {'explanation': None, 'found': False}
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/simplify/explain-term",
                json={'term': term},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Term explanation failed: {response.status_code}")
                return {'explanation': None, 'found': False}
                
        except Exception as e:
            logger.error(f"Term explanation error: {e}")
            return {'explanation': None, 'found': False}
    
    def render_text_with_simplification(self, text: str, show_simplified: bool = False) -> str:
        """
        Render text with simplification features
        
        Args:
            text: Original text
            show_simplified: Whether to show simplified version
            
        Returns:
            HTML with simplification features
        """
        if not self.simplification_enabled:
            return text
        
        if show_simplified:
            result = self.simplify_text(text)
            simplified_text = result.get('simplified_text', text)
            simplifications = result.get('simplifications', [])
            
            # Add 'i' icons for simplified terms
            html_text = simplified_text
            for simplification in simplifications:
                original = simplification.get('original', '')
                simplified = simplification.get('simplified', '')
                explanation = simplification.get('explanation', '')
                
                if original and simplified and explanation:
                    # Create hover tooltip with MaterializeCSS styling
                    tooltip_html = f"""
                    <span class="simplified-term" title="{explanation}">
                        {simplified}
                        <i class="material-icons tiny" style="color: #009688; cursor: help;">info</i>
                    </span>
                    """
                    html_text = html_text.replace(simplified, tooltip_html)
            
            return html_text
        
        return text
    
    def add_simplification_css(self):
        """Add CSS for simplification features"""
        st.markdown("""
        <style>
        .simplified-term {
            position: relative;
            display: inline-block;
        }
        
        .simplified-term i {
            margin-left: 2px;
            font-size: 12px !important;
        }
        
        .simplified-term:hover::after {
            content: attr(title);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #009688;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            white-space: nowrap;
            z-index: 1000;
            font-size: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        
        .simplification-toggle {
            margin: 10px 0;
            padding: 5px 10px;
            background: #e8f5e8;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }
        </style>
        """, unsafe_allow_html=True)

# Global instances
auth_manager = AuthenticationManager()
simplification_manager = TermSimplificationManager()

# Convenience functions for easy import
def check_authentication() -> bool:
    """Check if user is authenticated"""
    return auth_manager.is_user_authenticated()

def require_auth(redirect: bool = True) -> bool:
    """Require authentication"""
    return auth_manager.require_authentication(redirect)

def require_role(role: str) -> bool:
    """Require specific user role"""
    return auth_manager.require_role(role)

def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current user data"""
    return auth_manager.get_user_data()

def get_current_user_type() -> Optional[str]:
    """Get current user type"""
    return auth_manager.get_user_type()

def logout_user():
    """Logout current user"""
    auth_manager.logout()

def handle_oauth_callback() -> Optional[Dict[str, Any]]:
    """Handle OAuth callback"""
    return auth_manager.handle_oauth_callback()

def simplify_text(text: str) -> str:
    """Simplify text with 'i' icons"""
    return simplification_manager.render_text_with_simplification(text, show_simplified=True)

def add_simplification_styles():
    """Add simplification CSS styles"""
    simplification_manager.add_simplification_css()

def explain_term(term: str) -> Dict[str, Any]:
    """Get term explanation"""
    return simplification_manager.explain_term(term)

