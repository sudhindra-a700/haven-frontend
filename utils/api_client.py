"""
API Client for HAVEN Crowdfunding Platform
Matches the repository structure of sudhindra-a700/haven-frontend
"""

import requests
import streamlit as st
from typing import Dict, Any, Optional, List, Tuple
import logging
import time
from .config import get_config, get_api_endpoint

logger = logging.getLogger(__name__)

class APIClient:
    """API client for communicating with HAVEN backend"""
    
    def __init__(self):
        self.config = get_config()
        self.base_url = self.config.get_backend_url()
        self.timeout = self.config.get('backend.timeout', 30)
        self.retry_attempts = self.config.get('backend.retry_attempts', 3)
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'HAVEN-Frontend/1.0'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None, files: Optional[Dict] = None) -> Tuple[bool, Any]:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url.rstrip('/')}{endpoint}"
        
        for attempt in range(self.retry_attempts):
            try:
                # Add authentication token if available
                headers = {}
                user = st.session_state.get('user', {})
                if user.get('token'):
                    headers['Authorization'] = f"Bearer {user['token']}"
                
                # Make request
                if method.upper() == 'GET':
                    response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
                elif method.upper() == 'POST':
                    if files:
                        response = self.session.post(url, data=data, files=files, headers=headers, timeout=self.timeout)
                    else:
                        response = self.session.post(url, json=data, headers=headers, timeout=self.timeout)
                elif method.upper() == 'PUT':
                    response = self.session.put(url, json=data, headers=headers, timeout=self.timeout)
                elif method.upper() == 'DELETE':
                    response = self.session.delete(url, headers=headers, timeout=self.timeout)
                else:
                    return False, f"Unsupported HTTP method: {method}"
                
                # Handle response
                if response.status_code < 400:
                    try:
                        return True, response.json()
                    except ValueError:
                        return True, response.text
                else:
                    error_msg = self._extract_error_message(response)
                    logger.warning(f"API request failed: {response.status_code} - {error_msg}")
                    return False, error_msg
                    
            except requests.RequestException as e:
                logger.warning(f"API request attempt {attempt + 1} failed: {e}")
                if attempt == self.retry_attempts - 1:
                    return False, f"API request failed after {self.retry_attempts} attempts: {str(e)}"
                time.sleep(1)  # Wait before retry
        
        return False, "API request failed"
    
    def _extract_error_message(self, response: requests.Response) -> str:
        """Extract error message from response"""
        try:
            error_data = response.json()
            return error_data.get('detail', error_data.get('message', f"HTTP {response.status_code}"))
        except ValueError:
            return f"HTTP {response.status_code}: {response.text[:100]}"
    
    # Authentication endpoints
    def login(self, email: str, password: str) -> Tuple[bool, Any]:
        """Login user"""
        data = {'email': email, 'password': password}
        return self._make_request('POST', '/api/auth/login', data)
    
    def register(self, user_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Register new user"""
        return self._make_request('POST', '/api/auth/register', user_data)
    
    def oauth_login(self, provider: str, oauth_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """OAuth login"""
        data = {'provider': provider, **oauth_data}
        return self._make_request('POST', '/api/auth/oauth/login', data)
    
    def logout(self) -> Tuple[bool, Any]:
        """Logout user"""
        return self._make_request('POST', '/api/auth/logout')
    
    def refresh_token(self) -> Tuple[bool, Any]:
        """Refresh authentication token"""
        return self._make_request('POST', '/api/auth/refresh')
    
    # Campaign endpoints
    def get_campaigns(self, params: Optional[Dict] = None) -> Tuple[bool, Any]:
        """Get campaigns list"""
        return self._make_request('GET', '/api/campaigns', params=params)
    
    def get_campaign(self, campaign_id: str) -> Tuple[bool, Any]:
        """Get specific campaign"""
        return self._make_request('GET', f'/api/campaigns/{campaign_id}')
    
    def create_campaign(self, campaign_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Create new campaign"""
        return self._make_request('POST', '/api/campaigns', campaign_data)
    
    def update_campaign(self, campaign_id: str, campaign_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Update campaign"""
        return self._make_request('PUT', f'/api/campaigns/{campaign_id}', campaign_data)
    
    def delete_campaign(self, campaign_id: str) -> Tuple[bool, Any]:
        """Delete campaign"""
        return self._make_request('DELETE', f'/api/campaigns/{campaign_id}')
    
    def search_campaigns(self, query: str, filters: Optional[Dict] = None) -> Tuple[bool, Any]:
        """Search campaigns"""
        params = {'q': query}
        if filters:
            params.update(filters)
        return self._make_request('GET', '/api/campaigns/search', params=params)
    
    def get_campaign_categories(self) -> Tuple[bool, Any]:
        """Get campaign categories"""
        return self._make_request('GET', '/api/campaigns/categories')
    
    # User endpoints
    def get_user_profile(self, user_id: Optional[str] = None) -> Tuple[bool, Any]:
        """Get user profile"""
        endpoint = f'/api/users/{user_id}' if user_id else '/api/users/me'
        return self._make_request('GET', endpoint)
    
    def update_user_profile(self, user_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Update user profile"""
        return self._make_request('PUT', '/api/users/me', user_data)
    
    def get_user_campaigns(self, user_id: Optional[str] = None) -> Tuple[bool, Any]:
        """Get user's campaigns"""
        endpoint = f'/api/users/{user_id}/campaigns' if user_id else '/api/users/me/campaigns'
        return self._make_request('GET', endpoint)
    
    def get_user_donations(self, user_id: Optional[str] = None) -> Tuple[bool, Any]:
        """Get user's donations"""
        endpoint = f'/api/users/{user_id}/donations' if user_id else '/api/users/me/donations'
        return self._make_request('GET', endpoint)
    
    # Fraud detection endpoints
    def check_fraud(self, entity_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Check entity for fraud"""
        return self._make_request('POST', '/api/fraud-detection/check', entity_data)
    
    def get_fraud_score(self, entity_id: str) -> Tuple[bool, Any]:
        """Get fraud score for entity"""
        return self._make_request('GET', f'/api/fraud-detection/score/{entity_id}')
    
    def report_fraud(self, report_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Report fraudulent activity"""
        return self._make_request('POST', '/api/fraud-detection/report', report_data)
    
    # Translation endpoints
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> Tuple[bool, Any]:
        """Translate text"""
        data = {
            'text': text,
            'target_language': target_language,
            'source_language': source_language
        }
        return self._make_request('POST', '/api/translation/translate', data)
    
    def get_supported_languages(self) -> Tuple[bool, Any]:
        """Get supported languages for translation"""
        return self._make_request('GET', '/api/translation/languages')
    
    # Simplification endpoints
    def simplify_text(self, text: str, complexity_level: str = 'simple') -> Tuple[bool, Any]:
        """Simplify complex text"""
        data = {
            'text': text,
            'complexity_level': complexity_level
        }
        return self._make_request('POST', '/api/simplification/simplify', data)
    
    def get_term_explanation(self, term: str) -> Tuple[bool, Any]:
        """Get explanation for a term"""
        params = {'term': term}
        return self._make_request('GET', '/api/simplification/explain', params=params)
    
    # File upload endpoints
    def upload_file(self, file_data: bytes, filename: str, file_type: str) -> Tuple[bool, Any]:
        """Upload file"""
        files = {'file': (filename, file_data, file_type)}
        return self._make_request('POST', '/api/upload', files=files)
    
    def upload_campaign_image(self, campaign_id: str, image_data: bytes, filename: str) -> Tuple[bool, Any]:
        """Upload campaign image"""
        files = {'image': (filename, image_data, 'image/jpeg')}
        return self._make_request('POST', f'/api/campaigns/{campaign_id}/upload-image', files=files)
    
    # Analytics endpoints
    def get_platform_stats(self) -> Tuple[bool, Any]:
        """Get platform statistics"""
        return self._make_request('GET', '/api/analytics/stats')
    
    def get_campaign_analytics(self, campaign_id: str) -> Tuple[bool, Any]:
        """Get campaign analytics"""
        return self._make_request('GET', f'/api/analytics/campaigns/{campaign_id}')
    
    def get_user_analytics(self, user_id: Optional[str] = None) -> Tuple[bool, Any]:
        """Get user analytics"""
        endpoint = f'/api/analytics/users/{user_id}' if user_id else '/api/analytics/users/me'
        return self._make_request('GET', endpoint)
    
    # Donation endpoints
    def create_donation(self, donation_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Create donation"""
        return self._make_request('POST', '/api/donations', donation_data)
    
    def get_donation(self, donation_id: str) -> Tuple[bool, Any]:
        """Get donation details"""
        return self._make_request('GET', f'/api/donations/{donation_id}')
    
    def process_payment(self, payment_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """Process payment"""
        return self._make_request('POST', '/api/payments/process', payment_data)
    
    # Notification endpoints
    def get_notifications(self) -> Tuple[bool, Any]:
        """Get user notifications"""
        return self._make_request('GET', '/api/notifications')
    
    def mark_notification_read(self, notification_id: str) -> Tuple[bool, Any]:
        """Mark notification as read"""
        return self._make_request('PUT', f'/api/notifications/{notification_id}/read')
    
    def get_notification_settings(self) -> Tuple[bool, Any]:
        """Get notification settings"""
        return self._make_request('GET', '/api/notifications/settings')
    
    def update_notification_settings(self, settings: Dict[str, Any]) -> Tuple[bool, Any]:
        """Update notification settings"""
        return self._make_request('PUT', '/api/notifications/settings', settings)
    
    # Health check
    def health_check(self) -> Tuple[bool, Any]:
        """Check API health"""
        return self._make_request('GET', '/api/health')

# Global API client instance
api_client = APIClient()

# Convenience functions
def get_campaigns(params: Optional[Dict] = None) -> Tuple[bool, Any]:
    """Get campaigns"""
    return api_client.get_campaigns(params)

def get_campaign(campaign_id: str) -> Tuple[bool, Any]:
    """Get campaign"""
    return api_client.get_campaign(campaign_id)

def create_campaign(campaign_data: Dict[str, Any]) -> Tuple[bool, Any]:
    """Create campaign"""
    return api_client.create_campaign(campaign_data)

def search_campaigns(query: str, filters: Optional[Dict] = None) -> Tuple[bool, Any]:
    """Search campaigns"""
    return api_client.search_campaigns(query, filters)

def check_fraud(entity_data: Dict[str, Any]) -> Tuple[bool, Any]:
    """Check fraud"""
    return api_client.check_fraud(entity_data)

def translate_text(text: str, target_language: str) -> Tuple[bool, Any]:
    """Translate text"""
    return api_client.translate_text(text, target_language)

def simplify_text(text: str) -> Tuple[bool, Any]:
    """Simplify text"""
    return api_client.simplify_text(text)

def get_platform_stats() -> Tuple[bool, Any]:
    """Get platform statistics"""
    return api_client.get_platform_stats()

