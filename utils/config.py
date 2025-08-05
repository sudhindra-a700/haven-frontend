"""
Configuration Management for HAVEN Frontend
Handles environment variables and application settings
Updated to match existing environment configuration
"""

import os
import streamlit as st
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Configuration manager for the frontend application"""
    
    def __init__(self):
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables and Streamlit secrets"""
        config = {}
        
        # Try to get from environment variables first, then from Streamlit secrets
        def get_config_value(key: str, default: Any = None) -> Any:
            # First try environment variables
            env_value = os.getenv(key)
            if env_value is not None:
                return env_value
            
            # Then try Streamlit secrets
            try:
                return st.secrets.get(key, default)
            except:
                return default
        
        # Backend Configuration
        config['backend_url'] = get_config_value('BACKEND_URL', 'http://haven-fastapi-backend:10000')
        
        # OAuth Configuration - Google
        config['google_client_id'] = get_config_value('GOOGLE_CLIENT_ID', '')
        config['google_client_secret'] = get_config_value('GOOGLE_CLIENT_SECRET', '')
        
        # OAuth Configuration - Facebook
        config['facebook_app_id'] = get_config_value('FACEBOOK_APP_ID', '')
        config['facebook_app_secret'] = get_config_value('FACEBOOK_APP_SECRET', '')
        
        # Feature Flags
        config['features_oauth_enabled'] = self._parse_bool(get_config_value('FEATURES_OAUTH_ENABLED', 'true'))
        config['features_translation_enabled'] = self._parse_bool(get_config_value('FEATURES_TRANSLATION_ENABLED', 'true'))
        config['features_simplification_enabled'] = self._parse_bool(get_config_value('FEATURES_SIMPLIFICATION_ENABLED', 'true'))
        config['features_fraud_detection_enabled'] = self._parse_bool(get_config_value('FEATURES_FRAUD_DETECTION_ENABLED', 'true'))
        config['features_analytics_enabled'] = self._parse_bool(get_config_value('FEATURES_ANALYTICS_ENABLED', 'true'))
        config['features_file_upload_enabled'] = self._parse_bool(get_config_value('FEATURES_FILE_UPLOAD_ENABLED', 'true'))
        config['features_batch_operations_enabled'] = self._parse_bool(get_config_value('FEATURES_BATCH_OPERATIONS_ENABLED', 'true'))
        
        # Translation Configuration
        config['translation_enabled'] = self._parse_bool(get_config_value('TRANSLATION_ENABLED', 'true'))
        config['translation_default_language'] = get_config_value('TRANSLATION_DEFAULT_LANGUAGE', 'en')
        
        # Simplification Configuration
        config['simplification_enabled'] = self._parse_bool(get_config_value('SIMPLIFICATION_ENABLED', 'true'))
        config['simplification_default_level'] = get_config_value('SIMPLIFICATION_DEFAULT_LEVEL', 'simple')
        
        # Environment
        config['environment'] = get_config_value('ENVIRONMENT', 'development')
        
        return config
    
    def _parse_bool(self, value: str) -> bool:
        """Parse boolean value from string"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def get_backend_url(self) -> str:
        """Get backend URL"""
        backend_url = self.get('backend_url')
        
        # Handle different deployment scenarios
        if backend_url.startswith('http://haven-fastapi-backend:'):
            # Local development or Docker Compose
            return backend_url
        elif 'onrender.com' in backend_url:
            # Production deployment on Render
            return backend_url
        else:
            # Default fallback
            return 'http://localhost:8000'
    
    def get_oauth_config(self, provider: str) -> Dict[str, str]:
        """Get OAuth configuration for a provider"""
        if provider.lower() == 'google':
            return {
                'client_id': self.get('google_client_id', ''),
                'client_secret': self.get('google_client_secret', ''),
            }
        elif provider.lower() == 'facebook':
            return {
                'app_id': self.get('facebook_app_id', ''),
                'app_secret': self.get('facebook_app_secret', ''),
            }
        return {}
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        return self.get(f'features_{feature}_enabled', False)
    
    def is_oauth_enabled(self) -> bool:
        """Check if OAuth is enabled"""
        return self.is_feature_enabled('oauth')
    
    def is_translation_enabled(self) -> bool:
        """Check if translation is enabled"""
        return self.get('translation_enabled', False)
    
    def is_simplification_enabled(self) -> bool:
        """Check if simplification is enabled"""
        return self.get('simplification_enabled', False)
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.get('environment', 'development').lower() == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.get('environment', 'development').lower() == 'development'
    
    def get_translation_config(self) -> Dict[str, Any]:
        """Get translation configuration"""
        return {
            'enabled': self.is_translation_enabled(),
            'default_language': self.get('translation_default_language', 'en'),
        }
    
    def get_simplification_config(self) -> Dict[str, Any]:
        """Get simplification configuration"""
        return {
            'enabled': self.is_simplification_enabled(),
            'default_level': self.get('simplification_default_level', 'simple'),
        }
    
    def get_feature_flags(self) -> Dict[str, bool]:
        """Get all feature flags"""
        return {
            'oauth_enabled': self.is_feature_enabled('oauth'),
            'translation_enabled': self.is_feature_enabled('translation'),
            'simplification_enabled': self.is_feature_enabled('simplification'),
            'fraud_detection_enabled': self.is_feature_enabled('fraud_detection'),
            'analytics_enabled': self.is_feature_enabled('analytics'),
            'file_upload_enabled': self.is_feature_enabled('file_upload'),
            'batch_operations_enabled': self.is_feature_enabled('batch_operations'),
        }
    
    def validate_config(self) -> Dict[str, str]:
        """Validate configuration and return any issues"""
        issues = {}
        
        # Check backend URL
        backend_url = self.get_backend_url()
        if not backend_url or backend_url == 'http://localhost:8000':
            issues['backend_url'] = 'Backend URL not properly configured'
        
        # Check OAuth configuration if enabled
        if self.is_oauth_enabled():
            google_config = self.get_oauth_config('google')
            if not google_config.get('client_id'):
                issues['google_oauth'] = 'Google OAuth client ID not configured'
            
            facebook_config = self.get_oauth_config('facebook')
            if not facebook_config.get('app_id'):
                issues['facebook_oauth'] = 'Facebook OAuth app ID not configured'
        
        return issues
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get debug information about configuration"""
        return {
            'backend_url': self.get_backend_url(),
            'environment': self.get('environment'),
            'feature_flags': self.get_feature_flags(),
            'oauth_providers': {
                'google': bool(self.get_oauth_config('google').get('client_id')),
                'facebook': bool(self.get_oauth_config('facebook').get('app_id')),
            },
            'services': {
                'translation': self.is_translation_enabled(),
                'simplification': self.is_simplification_enabled(),
            }
        }

# Global configuration manager instance
config_manager = ConfigManager()

# Convenience functions for backward compatibility
def get_backend_url() -> str:
    """Get backend URL"""
    return config_manager.get_backend_url()

def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled"""
    return config_manager.is_feature_enabled(feature)

def get_oauth_config(provider: str) -> Dict[str, str]:
    """Get OAuth configuration for a provider"""
    return config_manager.get_oauth_config(provider)

def is_production() -> bool:
    """Check if running in production"""
    return config_manager.is_production()

def is_development() -> bool:
    """Check if running in development"""
    return config_manager.is_development()

