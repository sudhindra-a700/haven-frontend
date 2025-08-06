"""
Configuration management for HAVEN Crowdfunding Platform
Matches the repository structure of sudhindra-a700/haven-frontend
"""

import os
import streamlit as st
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration management class"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables and Streamlit secrets"""
        config = {}
        
        try:
            # Backend configuration
            config['backend'] = {
                'url': self._get_env_var('BACKEND_URL', 'https://haven-fastapi-backend.onrender.com'),
                'timeout': int(self._get_env_var('BACKEND_TIMEOUT', '30')),
                'retry_attempts': int(self._get_env_var('BACKEND_RETRY_ATTEMPTS', '3'))
            }
            
            # OAuth configuration
            config['oauth'] = {
                'enabled': self._get_env_var('OAUTH_ENABLED', 'true').lower() == 'true',
                'google': {
                    'client_id': self._get_env_var('GOOGLE_CLIENT_ID', ''),
                    'client_secret': self._get_env_var('GOOGLE_CLIENT_SECRET', ''),
                    'redirect_uri': self._get_env_var('GOOGLE_REDIRECT_URI', '')
                },
                'facebook': {
                    'app_id': self._get_env_var('FACEBOOK_APP_ID', ''),
                    'app_secret': self._get_env_var('FACEBOOK_APP_SECRET', ''),
                    'redirect_uri': self._get_env_var('FACEBOOK_REDIRECT_URI', '')
                }
            }
            
            # Feature flags
            config['features'] = {
                'translation_enabled': self._get_env_var('TRANSLATION_ENABLED', 'true').lower() == 'true',
                'simplification_enabled': self._get_env_var('SIMPLIFICATION_ENABLED', 'true').lower() == 'true',
                'fraud_detection_enabled': self._get_env_var('FRAUD_DETECTION_ENABLED', 'true').lower() == 'true',
                'analytics_enabled': self._get_env_var('ANALYTICS_ENABLED', 'true').lower() == 'true',
                'notifications_enabled': self._get_env_var('NOTIFICATIONS_ENABLED', 'true').lower() == 'true'
            }
            
            # UI configuration
            config['ui'] = {
                'theme': self._get_env_var('UI_THEME', 'light_green'),
                'language_default': self._get_env_var('DEFAULT_LANGUAGE', 'English'),
                'currency_symbol': self._get_env_var('CURRENCY_SYMBOL', '₹'),
                'date_format': self._get_env_var('DATE_FORMAT', 'DD/MM/YYYY'),
                'items_per_page': int(self._get_env_var('ITEMS_PER_PAGE', '10'))
            }
            
            # Security configuration
            config['security'] = {
                'session_timeout': int(self._get_env_var('SESSION_TIMEOUT', '3600')),  # 1 hour
                'max_login_attempts': int(self._get_env_var('MAX_LOGIN_ATTEMPTS', '5')),
                'password_min_length': int(self._get_env_var('PASSWORD_MIN_LENGTH', '8')),
                'enable_2fa': self._get_env_var('ENABLE_2FA', 'false').lower() == 'true'
            }
            
            # API endpoints
            config['api'] = {
                'auth': '/api/auth',
                'campaigns': '/api/campaigns',
                'users': '/api/users',
                'fraud_detection': '/api/fraud-detection',
                'translation': '/api/translation',
                'simplification': '/api/simplification',
                'upload': '/api/upload'
            }
            
            # File upload configuration
            config['upload'] = {
                'max_file_size': int(self._get_env_var('MAX_FILE_SIZE', '10485760')),  # 10MB
                'allowed_extensions': self._get_env_var('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,pdf,doc,docx').split(','),
                'upload_path': self._get_env_var('UPLOAD_PATH', '/tmp/uploads')
            }
            
            # Logging configuration
            config['logging'] = {
                'level': self._get_env_var('LOG_LEVEL', 'INFO'),
                'format': self._get_env_var('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                'file_path': self._get_env_var('LOG_FILE_PATH', 'logs/haven_frontend.log')
            }
            
            # Development configuration
            config['development'] = {
                'debug': self._get_env_var('DEBUG', 'false').lower() == 'true',
                'mock_api': self._get_env_var('MOCK_API', 'false').lower() == 'true',
                'show_debug_info': self._get_env_var('SHOW_DEBUG_INFO', 'false').lower() == 'true'
            }
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Return minimal default configuration
            config = self._get_default_config()
        
        return config
    
    def _get_env_var(self, key: str, default: str = '') -> str:
        """Get environment variable with fallback to Streamlit secrets"""
        try:
            # First try environment variables
            value = os.getenv(key)
            if value is not None:
                return value
            
            # Then try Streamlit secrets
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
            
            # Return default
            return default
            
        except Exception as e:
            logger.warning(f"Error getting environment variable {key}: {e}")
            return default
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for fallback"""
        return {
            'backend': {
                'url': 'https://haven-fastapi-backend.onrender.com',
                'timeout': 30,
                'retry_attempts': 3
            },
            'oauth': {
                'enabled': False,
                'google': {'client_id': '', 'client_secret': '', 'redirect_uri': ''},
                'facebook': {'app_id': '', 'app_secret': '', 'redirect_uri': ''}
            },
            'features': {
                'translation_enabled': True,
                'simplification_enabled': True,
                'fraud_detection_enabled': True,
                'analytics_enabled': True,
                'notifications_enabled': True
            },
            'ui': {
                'theme': 'light_green',
                'language_default': 'English',
                'currency_symbol': '₹',
                'date_format': 'DD/MM/YYYY',
                'items_per_page': 10
            },
            'security': {
                'session_timeout': 3600,
                'max_login_attempts': 5,
                'password_min_length': 8,
                'enable_2fa': False
            },
            'api': {
                'auth': '/api/auth',
                'campaigns': '/api/campaigns',
                'users': '/api/users',
                'fraud_detection': '/api/fraud-detection',
                'translation': '/api/translation',
                'simplification': '/api/simplification',
                'upload': '/api/upload'
            },
            'upload': {
                'max_file_size': 10485760,
                'allowed_extensions': ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'],
                'upload_path': '/tmp/uploads'
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file_path': 'logs/haven_frontend.log'
            },
            'development': {
                'debug': False,
                'mock_api': False,
                'show_debug_info': False
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        try:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
            
        except Exception as e:
            logger.error(f"Error getting config key {key}: {e}")
            return default
    
    def get_backend_url(self) -> str:
        """Get backend URL"""
        return self.get('backend.url', 'https://haven-fastapi-backend.onrender.com')
    
    def get_api_endpoint(self, endpoint: str) -> str:
        """Get full API endpoint URL"""
        base_url = self.get_backend_url().rstrip('/')
        api_path = self.get(f'api.{endpoint}', f'/api/{endpoint}')
        return f"{base_url}{api_path}"
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        return self.get(f'features.{feature}_enabled', False)
    
    def is_oauth_enabled(self) -> bool:
        """Check if OAuth is enabled"""
        return self.get('oauth.enabled', False)
    
    def is_development_mode(self) -> bool:
        """Check if development mode is enabled"""
        return self.get('development.debug', False)
    
    def get_upload_config(self) -> Dict[str, Any]:
        """Get upload configuration"""
        return self.get('upload', {})
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration"""
        return self.get('security', {})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration"""
        return self.get('ui', {})
    
    def reload(self):
        """Reload configuration"""
        self.config = self._load_config()
        logger.info("Configuration reloaded")

# Global configuration instance
config = Config()

def get_config() -> Config:
    """Get global configuration instance"""
    return config

def get_backend_url() -> str:
    """Get backend URL"""
    return config.get_backend_url()

def get_api_endpoint(endpoint: str) -> str:
    """Get API endpoint URL"""
    return config.get_api_endpoint(endpoint)

def is_feature_enabled(feature: str) -> bool:
    """Check if feature is enabled"""
    return config.is_feature_enabled(feature)

def is_oauth_enabled() -> bool:
    """Check if OAuth is enabled"""
    return config.is_oauth_enabled()

def is_development_mode() -> bool:
    """Check if development mode is enabled"""
    return config.is_development_mode()

