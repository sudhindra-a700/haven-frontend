"""
API Client for HAVEN Crowdfunding Platform Frontend
Handles all backend API communication with proper error handling
"""

import requests
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import streamlit as st

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom API error exception"""
    def __init__(self, message: str, status_code: int = None, response_data: Dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)

class APIClient:
    """
    API Client for backend communication
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'HAVEN-Frontend/1.0'
        })
        
        # Set timeout
        self.timeout = 30
    
    def _get_auth_headers(self, token: str = None) -> Dict[str, str]:
        """Get authentication headers"""
        headers = {}
        
        # Use provided token or get from session state
        auth_token = token or st.session_state.get('access_token')
        
        if auth_token:
            headers['Authorization'] = f'Bearer {auth_token}'
        
        return headers
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Dict = None,
        params: Dict = None,
        token: str = None,
        files: Dict = None
    ) -> Dict[str, Any]:
        """Make HTTP request to backend API"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            # Prepare headers
            headers = self._get_auth_headers(token)
            
            # Prepare request arguments
            request_kwargs = {
                'timeout': self.timeout,
                'params': params,
                'headers': headers
            }
            
            # Handle different content types
            if files:
                # For file uploads, don't set Content-Type (let requests handle it)
                if 'Content-Type' in headers:
                    del headers['Content-Type']
                request_kwargs['files'] = files
                if data:
                    request_kwargs['data'] = data
            else:
                # For JSON data
                if data:
                    request_kwargs['json'] = data
            
            # Make request
            response = self.session.request(method, url, **request_kwargs)
            
            # Handle response
            if response.status_code == 204:
                return {}
            
            try:
                response_data = response.json()
            except ValueError:
                response_data = {'message': response.text}
            
            if response.status_code >= 400:
                error_message = response_data.get('detail', f'API Error: {response.status_code}')
                raise APIError(error_message, response.status_code, response_data)
            
            return response_data
            
        except requests.exceptions.Timeout:
            raise APIError("Request timeout. Please try again.")
        
        except requests.exceptions.ConnectionError:
            raise APIError("Unable to connect to server. Please check your internet connection.")
        
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")
        
        except APIError:
            raise
        
        except Exception as e:
            logger.error(f"Unexpected API error: {e}")
            raise APIError(f"Unexpected error: {str(e)}")
    
    # Authentication endpoints
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login with email and password"""
        data = {
            'email': email,
            'password': password
        }
        return self._make_request('POST', '/auth/login', data=data)
    
    def register(self, email: str, password: str, full_name: str, phone_number: str = None) -> Dict[str, Any]:
        """Register new user"""
        data = {
            'email': email,
            'password': password,
            'full_name': full_name,
            'phone_number': phone_number
        }
        return self._make_request('POST', '/auth/register', data=data)
    
    def logout(self, token: str = None) -> Dict[str, Any]:
        """Logout user"""
        return self._make_request('POST', '/auth/logout', token=token)
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        data = {'refresh_token': refresh_token}
        return self._make_request('POST', '/auth/refresh', data=data)
    
    def get_current_user(self, token: str = None) -> Dict[str, Any]:
        """Get current user information"""
        return self._make_request('GET', '/auth/me', token=token)
    
    def get_google_auth_url(self, redirect_url: str = None) -> str:
        """Get Google OAuth authorization URL"""
        params = {}
        if redirect_url:
            params['redirect_url'] = redirect_url
        
        response = self._make_request('GET', '/auth/google', params=params)
        return response.get('auth_url')
    
    def get_facebook_auth_url(self, redirect_url: str = None) -> str:
        """Get Facebook OAuth authorization URL"""
        params = {}
        if redirect_url:
            params['redirect_url'] = redirect_url
        
        response = self._make_request('GET', '/auth/facebook', params=params)
        return response.get('auth_url')
    
    # User endpoints
    def get_user_profile(self, user_id: int = None, token: str = None) -> Dict[str, Any]:
        """Get user profile"""
        if user_id:
            endpoint = f'/users/{user_id}'
        else:
            endpoint = '/users/me'
        
        return self._make_request('GET', endpoint, token=token)
    
    def update_user_profile(self, profile_data: Dict[str, Any], token: str = None) -> Dict[str, Any]:
        """Update user profile"""
        return self._make_request('PUT', '/users/me', data=profile_data, token=token)
    
    def change_password(self, current_password: str, new_password: str, token: str = None) -> Dict[str, Any]:
        """Change user password"""
        data = {
            'current_password': current_password,
            'new_password': new_password
        }
        return self._make_request('POST', '/users/me/change-password', data=data, token=token)
    
    def get_user_stats(self, token: str = None) -> Dict[str, Any]:
        """Get user statistics"""
        return self._make_request('GET', '/users/me/stats', token=token)
    
    def get_user_campaigns(self, skip: int = 0, limit: int = 20, token: str = None) -> List[Dict[str, Any]]:
        """Get user's campaigns"""
        params = {'skip': skip, 'limit': limit}
        return self._make_request('GET', '/users/me/campaigns', params=params, token=token)
    
    def get_user_donations(self, skip: int = 0, limit: int = 20, token: str = None) -> List[Dict[str, Any]]:
        """Get user's donations"""
        params = {'skip': skip, 'limit': limit}
        return self._make_request('GET', '/users/me/donations', params=params, token=token)
    
    # Campaign endpoints
    def get_campaigns(
        self,
        skip: int = 0,
        limit: int = 20,
        category: str = None,
        status: str = None,
        search: str = None,
        sort_by: str = 'created_at',
        sort_order: str = 'desc'
    ) -> List[Dict[str, Any]]:
        """Get campaigns with filtering"""
        params = {
            'skip': skip,
            'limit': limit,
            'sort_by': sort_by,
            'sort_order': sort_order
        }
        
        if category:
            params['category'] = category
        if status:
            params['status'] = status
        if search:
            params['search'] = search
        
        return self._make_request('GET', '/campaigns/', params=params)
    
    def get_campaign(self, campaign_id: int) -> Dict[str, Any]:
        """Get campaign by ID"""
        return self._make_request('GET', f'/campaigns/{campaign_id}')
    
    def create_campaign(self, campaign_data: Dict[str, Any], token: str = None) -> Dict[str, Any]:
        """Create new campaign"""
        return self._make_request('POST', '/campaigns/', data=campaign_data, token=token)
    
    def update_campaign(self, campaign_id: int, campaign_data: Dict[str, Any], token: str = None) -> Dict[str, Any]:
        """Update campaign"""
        return self._make_request('PUT', f'/campaigns/{campaign_id}', data=campaign_data, token=token)
    
    def delete_campaign(self, campaign_id: int, token: str = None) -> Dict[str, Any]:
        """Delete campaign"""
        return self._make_request('DELETE', f'/campaigns/{campaign_id}', token=token)
    
    def submit_campaign(self, campaign_id: int, token: str = None) -> Dict[str, Any]:
        """Submit campaign for review"""
        return self._make_request('POST', f'/campaigns/{campaign_id}/submit', token=token)
    
    def donate_to_campaign(self, campaign_id: int, donation_data: Dict[str, Any], token: str = None) -> Dict[str, Any]:
        """Make donation to campaign"""
        return self._make_request('POST', f'/campaigns/{campaign_id}/donate', data=donation_data, token=token)
    
    def create_campaign_update(self, campaign_id: int, update_data: Dict[str, Any], token: str = None) -> Dict[str, Any]:
        """Create campaign update"""
        return self._make_request('POST', f'/campaigns/{campaign_id}/updates', data=update_data, token=token)
    
    def create_campaign_comment(self, campaign_id: int, comment_data: Dict[str, Any], token: str = None) -> Dict[str, Any]:
        """Create campaign comment"""
        return self._make_request('POST', f'/campaigns/{campaign_id}/comments', data=comment_data, token=token)
    
    # Translation endpoints
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto', token: str = None) -> Dict[str, Any]:
        """Translate text"""
        data = {
            'text': text,
            'target_language': target_language,
            'source_language': source_language
        }
        return self._make_request('POST', '/translate/translate', data=data, token=token)
    
    def detect_language(self, text: str, token: str = None) -> Dict[str, Any]:
        """Detect language of text"""
        data = {'text': text}
        return self._make_request('POST', '/translate/detect-language', data=data, token=token)
    
    def get_supported_languages(self) -> Dict[str, Any]:
        """Get supported languages"""
        return self._make_request('GET', '/translate/languages')
    
    # Fraud detection endpoints
    def analyze_campaign_fraud(self, campaign_data: Dict[str, Any], token: str = None) -> Dict[str, Any]:
        """Analyze campaign for fraud"""
        data = {'campaign_data': campaign_data}
        return self._make_request('POST', '/fraud/analyze', data=data, token=token)
    
    def analyze_existing_campaign_fraud(self, campaign_id: int, token: str = None) -> Dict[str, Any]:
        """Analyze existing campaign for fraud"""
        return self._make_request('POST', f'/fraud/analyze/campaign/{campaign_id}', token=token)
    
    def report_fraud(self, campaign_id: int, reason: str, evidence: str = None, token: str = None) -> Dict[str, Any]:
        """Report campaign as fraudulent"""
        data = {
            'campaign_id': campaign_id,
            'reason': reason,
            'evidence': evidence
        }
        return self._make_request('POST', '/fraud/report', data=data, token=token)
    
    # Health and status endpoints
    def get_health_status(self) -> Dict[str, Any]:
        """Get API health status"""
        return self._make_request('GET', '/health')
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get platform statistics"""
        try:
            # This endpoint might not exist, so we'll simulate it
            campaigns = self.get_campaigns(limit=1000)  # Get all campaigns for stats
            
            total_campaigns = len(campaigns)
            total_raised = sum(float(c.get('current_amount', 0)) for c in campaigns)
            active_campaigns = len([c for c in campaigns if c.get('status') == 'active'])
            
            return {
                'total_campaigns': total_campaigns,
                'total_raised': total_raised,
                'active_campaigns': active_campaigns,
                'active_users': 100  # Placeholder
            }
        except:
            return {
                'total_campaigns': 0,
                'total_raised': 0,
                'active_campaigns': 0,
                'active_users': 0
            }
    
    # File upload endpoints
    def upload_file(self, file_data, file_type: str = 'image', token: str = None) -> Dict[str, Any]:
        """Upload file to server"""
        files = {'file': file_data}
        data = {'file_type': file_type}
        
        return self._make_request('POST', '/upload', data=data, files=files, token=token)
    
    # Utility methods
    def test_connection(self) -> bool:
        """Test connection to backend API"""
        try:
            self.get_health_status()
            return True
        except:
            return False
    
    def get_api_info(self) -> Dict[str, Any]:
        """Get API information"""
        try:
            return self._make_request('GET', '/')
        except:
            return {'message': 'API information unavailable'}

