"""
Translation Service for HAVEN Crowdfunding Platform
Moved to utils directory to match repository structure
"""

import streamlit as st
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    """Translation service for multi-language support"""
    
    def __init__(self):
        self.translations = self._load_translations()
        self.current_language = 'English'
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translation dictionaries for supported languages"""
        return {
            'English': {
                # Common terms
                'welcome': 'Welcome',
                'login': 'Login',
                'register': 'Register',
                'logout': 'Logout',
                'home': 'Home',
                'explore': 'Explore',
                'search': 'Search',
                'campaign': 'Campaign',
                'profile': 'Profile',
                'language': 'Language',
                'settings': 'Settings',
                'navigation': 'Navigation',
                
                # Authentication
                'sign_in': 'Sign In',
                'sign_up': 'Sign Up',
                'email': 'Email',
                'password': 'Password',
                'forgot_password': 'Forgot Password',
                'create_account': 'Create Account',
                'google_signin': 'Sign in with Google',
                'facebook_signin': 'Sign in with Facebook',
                'full_name': 'Full Name',
                'agree_terms': 'I agree to Terms of Service',
                
                # Campaign terms
                'create_campaign': 'Create Campaign',
                'browse_projects': 'Browse Projects',
                'support_causes': 'Support Causes',
                'donate': 'Donate',
                'funding_goal': 'Funding Goal',
                'raised': 'Raised',
                'supporters': 'Supporters',
                'days_left': 'Days Left',
                'campaigns': 'Campaigns',
                
                # Categories
                'medical': 'Medical',
                'education': 'Education',
                'disaster_relief': 'Disaster Relief',
                'animal_welfare': 'Animal Welfare',
                'environment': 'Environment',
                'community_development': 'Community Development',
                'technology': 'Technology',
                'social_causes': 'Social Causes',
                'arts_culture': 'Arts & Culture',
                'sports': 'Sports',
                
                # Messages
                'success_login': 'Login successful!',
                'success_register': 'Account created successfully!',
                'error_login': 'Login failed. Please try again.',
                'error_register': 'Registration failed. Please try again.',
                'loading': 'Loading...',
                'please_wait': 'Please wait...',
                'login_successful': 'Login successful!',
                'demo_login_successful': 'Demo login successful!',
                'account_created': 'Account created successfully!',
                'logged_out': 'Logged out successfully!',
                'valid_email_required': 'Please enter a valid email address',
                'fill_all_fields': 'Please fill all fields and accept terms',
                
                # Platform info
                'platform_tagline': 'Empowering Communities Through Crowdfunding',
                'trusted_platform': 'Your trusted crowdfunding platform',
                'make_difference': 'Make a difference today',
                'join_community': 'Join thousands of changemakers',
                'about_platform': 'About HAVEN Platform',
                'create_campaigns': 'Create Campaigns',
                'discover_causes': 'Discover Causes',
                'secure_trusted': 'Secure & Trusted',
                'total_raised': 'Total Raised',
                'active_campaigns': 'Active Campaigns',
                'community_members': 'Community Members',
                'success_rate': 'Success Rate',
                'quick_stats': 'Quick Stats',
                
                # Authentication pages
                'sign_in_to_haven': 'Sign In to HAVEN',
                'create_haven_account': 'Create HAVEN Account',
                'demo_login': 'Demo Login',
            },
            
            'Hindi': {
                # Common terms
                'welcome': 'स्वागत',
                'login': 'लॉगिन',
                'register': 'पंजीकरण',
                'logout': 'लॉगआउट',
                'home': 'होम',
                'explore': 'खोजें',
                'search': 'खोज',
                'campaign': 'अभियान',
                'profile': 'प्रोफाइल',
                'language': 'भाषा',
                'settings': 'सेटिंग्स',
                'navigation': 'नेवीगेशन',
                
                # Authentication
                'sign_in': 'साइन इन',
                'sign_up': 'साइन अप',
                'email': 'ईमेल',
                'password': 'पासवर्ड',
                'forgot_password': 'पासवर्ड भूल गए',
                'create_account': 'खाता बनाएं',
                'google_signin': 'Google से साइन इन करें',
                'facebook_signin': 'Facebook से साइन इन करें',
                'full_name': 'पूरा नाम',
                'agree_terms': 'मैं सेवा की शर्तों से सहमत हूं',
                
                # Campaign terms
                'create_campaign': 'अभियान बनाएं',
                'browse_projects': 'प्रोजेक्ट्स देखें',
                'support_causes': 'कारणों का समर्थन करें',
                'donate': 'दान करें',
                'funding_goal': 'फंडिंग लक्ष्य',
                'raised': 'जुटाया गया',
                'supporters': 'समर्थक',
                'days_left': 'दिन बचे',
                'campaigns': 'अभियान',
                
                # Categories
                'medical': 'चिकित्सा',
                'education': 'शिक्षा',
                'disaster_relief': 'आपदा राहत',
                'animal_welfare': 'पशु कल्याण',
                'environment': 'पर्यावरण',
                'community_development': 'सामुदायिक विकास',
                'technology': 'प्रौद्योगिकी',
                'social_causes': 'सामाजिक कारण',
                'arts_culture': 'कला और संस्कृति',
                'sports': 'खेल',
                
                # Messages
                'success_login': 'लॉगिन सफल!',
                'success_register': 'खाता सफलतापूर्वक बनाया गया!',
                'error_login': 'लॉगिन असफल। कृपया पुनः प्रयास करें।',
                'error_register': 'पंजीकरण असफल। कृपया पुनः प्रयास करें।',
                'loading': 'लोड हो रहा है...',
                'please_wait': 'कृपया प्रतीक्षा करें...',
                'login_successful': 'लॉगिन सफल!',
                'demo_login_successful': 'डेमो लॉगिन सफल!',
                'account_created': 'खाता सफलतापूर्वक बनाया गया!',
                'logged_out': 'सफलतापूर्वक लॉगआउट!',
                'valid_email_required': 'कृपया एक वैध ईमेल पता दर्ज करें',
                'fill_all_fields': 'कृपया सभी फ़ील्ड भरें और शर्तों को स्वीकार करें',
                
                # Platform info
                'platform_tagline': 'क्राउडफंडिंग के माध्यम से समुदायों को सशक्त बनाना',
                'trusted_platform': 'आपका विश्वसनीय क्राउडफंडिंग प्लेटफॉर्म',
                'make_difference': 'आज ही बदलाव लाएं',
                'join_community': 'हजारों परिवर्तनकर्ताओं से जुड़ें',
                'about_platform': 'HAVEN प्लेटफॉर्म के बारे में',
                'create_campaigns': 'अभियान बनाएं',
                'discover_causes': 'कारण खोजें',
                'secure_trusted': 'सुरक्षित और विश्वसनीय',
                'total_raised': 'कुल जुटाया गया',
                'active_campaigns': 'सक्रिय अभियान',
                'community_members': 'समुदाय के सदस्य',
                'success_rate': 'सफलता दर',
                'quick_stats': 'त्वरित आंकड़े',
                
                # Authentication pages
                'sign_in_to_haven': 'HAVEN में साइन इन करें',
                'create_haven_account': 'HAVEN खाता बनाएं',
                'demo_login': 'डेमो लॉगिन',
            },
            
            'Tamil': {
                # Common terms
                'welcome': 'வரவேற்கிறோம்',
                'login': 'உள்நுழைவு',
                'register': 'பதிவு',
                'logout': 'வெளியேறு',
                'home': 'முகப்பு',
                'explore': 'ஆராய்',
                'search': 'தேடல்',
                'campaign': 'பிரச்சாரம்',
                'profile': 'சுயவிவரம்',
                'language': 'மொழி',
                'settings': 'அமைப்புகள்',
                'navigation': 'வழிசெலுத்தல்',
                
                # Authentication
                'sign_in': 'உள்நுழைக',
                'sign_up': 'பதிவு செய்க',
                'email': 'மின்னஞ்சல்',
                'password': 'கடவுச்சொல்',
                'forgot_password': 'கடவுச்சொல் மறந்துவிட்டதா',
                'create_account': 'கணக்கு உருவாக்கு',
                'google_signin': 'Google மூலம் உள்நுழைக',
                'facebook_signin': 'Facebook மூலம் உள்நுழைக',
                'full_name': 'முழு பெயர்',
                'agree_terms': 'நான் சேவை விதிமுறைகளை ஏற்கிறேன்',
                
                # Campaign terms
                'create_campaign': 'பிரச்சாரம் உருவாக்கு',
                'browse_projects': 'திட்டங்களை உலாவு',
                'support_causes': 'காரணங்களை ஆதரி',
                'donate': 'நன்கொடை',
                'funding_goal': 'நிதி இலக்கு',
                'raised': 'திரட்டப்பட்டது',
                'supporters': 'ஆதரவாளர்கள்',
                'days_left': 'நாட்கள் மீதம்',
                'campaigns': 'பிரச்சாரங்கள்',
                
                # Categories
                'medical': 'மருத்துவம்',
                'education': 'கல்வி',
                'disaster_relief': 'பேரிடர் நிவாரணம்',
                'animal_welfare': 'விலங்கு நலன்',
                'environment': 'சுற்றுச்சூழல்',
                'community_development': 'சமூக வளர்ச்சி',
                'technology': 'தொழில்நுட்பம்',
                'social_causes': 'சமூக காரணங்கள்',
                'arts_culture': 'கலை மற்றும் கலாச்சாரம்',
                'sports': 'விளையாட்டு',
                
                # Messages
                'success_login': 'உள்நுழைவு வெற்றிகரமாக!',
                'success_register': 'கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது!',
                'error_login': 'உள்நுழைவு தோல்வி. மீண்டும் முயற்சிக்கவும்.',
                'error_register': 'பதிவு தோல்வி. மீண்டும் முயற்சிக்கவும்.',
                'loading': 'ஏற்றுகிறது...',
                'please_wait': 'தயவுசெய்து காத்திருக்கவும்...',
                'login_successful': 'உள்நுழைவு வெற்றிகரமாக!',
                'demo_login_successful': 'டெமோ உள்நுழைவு வெற்றிகரமாக!',
                'account_created': 'கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது!',
                'logged_out': 'வெற்றிகரமாக வெளியேறினீர்கள்!',
                'valid_email_required': 'தயவுசெய்து சரியான மின்னஞ்சல் முகவரியை உள்ளிடவும்',
                'fill_all_fields': 'தயவுசெய்து அனைத்து புலங்களையும் நிரப்பி விதிமுறைகளை ஏற்கவும்',
                
                # Platform info
                'platform_tagline': 'க்ராउட்ஃபண்டிங் மூலம் சமூகங்களை வலுப்படுத்துதல்',
                'trusted_platform': 'உங்கள் நம்பகமான க்ராउட்ஃபண்டிங் தளம்',
                'make_difference': 'இன்றே மாற்றத்தை ஏற்படுத்துங்கள்',
                'join_community': 'ஆயிரக்கணக்கான மாற்றத்தை ஏற்படுத்துபவர்களுடன் சேருங்கள்',
                'about_platform': 'HAVEN தளத்தைப் பற்றி',
                'create_campaigns': 'பிரச்சாரங்களை உருவாக்குங்கள்',
                'discover_causes': 'காரணங்களைக் கண்டறியுங்கள்',
                'secure_trusted': 'பாதுகாப்பான மற்றும் நம்பகமான',
                'total_raised': 'மொத்தம் திரட்டப்பட்டது',
                'active_campaigns': 'செயலில் உள்ள பிரச்சாரங்கள்',
                'community_members': 'சமூக உறுப்பினர்கள்',
                'success_rate': 'வெற்றி விகிதம்',
                'quick_stats': 'விரைவு புள்ளிவிவரங்கள்',
                
                # Authentication pages
                'sign_in_to_haven': 'HAVEN இல் உள்நுழைக',
                'create_haven_account': 'HAVEN கணக்கை உருவாக்கவும்',
                'demo_login': 'டெமோ உள்நுழைவு',
            },
            
            'Telugu': {
                # Common terms
                'welcome': 'స్వాగతం',
                'login': 'లాగిన్',
                'register': 'నమోదు',
                'logout': 'లాగ్అవుట్',
                'home': 'హోమ్',
                'explore': 'అన్వేషించు',
                'search': 'వెతుకు',
                'campaign': 'ప్రచారం',
                'profile': 'ప్రొఫైల్',
                'language': 'భాష',
                'settings': 'సెట్టింగ్స్',
                'navigation': 'నావిగేషన్',
                
                # Authentication
                'sign_in': 'సైన్ ఇన్',
                'sign_up': 'సైన్ అప్',
                'email': 'ఇమెయిల్',
                'password': 'పాస్‌వర్డ్',
                'forgot_password': 'పాస్‌వర్డ్ మర్చిపోయారా',
                'create_account': 'ఖాతా సృష్టించు',
                'google_signin': 'Google తో సైన్ ఇన్ చేయండి',
                'facebook_signin': 'Facebook తో సైన్ ఇన్ చేయండి',
                'full_name': 'పూర్తి పేరు',
                'agree_terms': 'నేను సేవా నిబంధనలను అంగీకరిస్తున్నాను',
                
                # Campaign terms
                'create_campaign': 'ప్రచారం సృష్టించు',
                'browse_projects': 'ప్రాజెక్ట్‌లను బ్రౌజ్ చేయండి',
                'support_causes': 'కారణాలకు మద్దతు ఇవ్వండి',
                'donate': 'దానం చేయండి',
                'funding_goal': 'ఫండింగ్ లక్ష్యం',
                'raised': 'సేకరించబడింది',
                'supporters': 'మద్దతుదారులు',
                'days_left': 'రోజులు మిగిలాయి',
                'campaigns': 'ప్రచారాలు',
                
                # Categories
                'medical': 'వైద్యం',
                'education': 'విద్య',
                'disaster_relief': 'విపత్తు ఉపశమనం',
                'animal_welfare': 'జంతు సంక్షేమం',
                'environment': 'పర్యావరణం',
                'community_development': 'సమాజ అభివృద్ధి',
                'technology': 'సాంకేతికత',
                'social_causes': 'సామాజిక కారణాలు',
                'arts_culture': 'కళలు మరియు సంస్కృతి',
                'sports': 'క్రీడలు',
                
                # Messages
                'success_login': 'లాగిన్ విజయవంతం!',
                'success_register': 'ఖాతా విజయవంతంగా సృష్టించబడింది!',
                'error_login': 'లాగిన్ విఫలమైంది. దయచేసి మళ్లీ ప్రయత్నించండి.',
                'error_register': 'నమోదు విఫలమైంది. దయచేసి మళ్లీ ప్రయత్నించండి.',
                'loading': 'లోడ్ అవుతోంది...',
                'please_wait': 'దయచేసి వేచి ఉండండి...',
                'login_successful': 'లాగిన్ విజయవంతం!',
                'demo_login_successful': 'డెమో లాగిన్ విజయవంతం!',
                'account_created': 'ఖాతా విజయవంతంగా సృష్టించబడింది!',
                'logged_out': 'విజయవంతంగా లాగ్అవుట్ అయ్యారు!',
                'valid_email_required': 'దయచేసి చెల్లుబాటు అయ్యే ఇమెయిల్ చిరునామాను నమోదు చేయండి',
                'fill_all_fields': 'దయచేసి అన్ని ఫీల్డ్‌లను పూరించి నిబంధనలను అంగీకరించండి',
                
                # Platform info
                'platform_tagline': 'క్రౌడ్‌ఫండింగ్ ద్వారా కమ్యూనిటీలను శక్తివంతం చేయడం',
                'trusted_platform': 'మీ విశ్వసనీయ క్రౌడ్‌ఫండింగ్ ప్లాట్‌ఫారమ్',
                'make_difference': 'ఈ రోజే మార్పు తీసుకురండి',
                'join_community': 'వేలాది మార్పు తీసుకువచ్చేవారితో చేరండి',
                'about_platform': 'HAVEN ప్లాట్‌ఫారమ్ గురించి',
                'create_campaigns': 'ప్రచారాలను సృష్టించండి',
                'discover_causes': 'కారణాలను కనుగొనండి',
                'secure_trusted': 'సురక్షితమైన మరియు విశ్వసనీయమైన',
                'total_raised': 'మొత్తం సేకరించబడింది',
                'active_campaigns': 'క్రియాశీల ప్రచారాలు',
                'community_members': 'కమ్యూనిటీ సభ్యులు',
                'success_rate': 'విజయ రేటు',
                'quick_stats': 'త్వరిత గణాంకాలు',
                
                # Authentication pages
                'sign_in_to_haven': 'HAVEN లో సైన్ ఇన్ చేయండి',
                'create_haven_account': 'HAVEN ఖాతాను సృష్టించండి',
                'demo_login': 'డెమో లాగిన్',
            }
        }
    
    def set_language(self, language: str):
        """Set the current language"""
        if language in self.translations:
            self.current_language = language
            if 'language' in st.session_state:
                st.session_state.language = language
    
    def get_text(self, key: str, default: Optional[str] = None) -> str:
        """Get translated text for a key"""
        try:
            current_lang = st.session_state.get('language', self.current_language)
            
            if current_lang in self.translations:
                return self.translations[current_lang].get(key, default or key)
            else:
                # Fallback to English
                return self.translations['English'].get(key, default or key)
                
        except Exception as e:
            logger.error(f"Translation error for key '{key}': {e}")
            return default or key
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages with their native names"""
        return {
            'English': '🇺🇸 English',
            'Hindi': '🇮🇳 हिंदी',
            'Tamil': '🇮🇳 தமிழ்',
            'Telugu': '🇮🇳 తెలుగు'
        }
    
    def translate_campaign_data(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Translate campaign data based on current language"""
        try:
            translated_data = campaign_data.copy()
            
            # Translate category if it exists
            if 'category' in translated_data:
                category_key = translated_data['category'].lower().replace(' ', '_')
                translated_data['category_translated'] = self.get_text(category_key, translated_data['category'])
            
            # Add translated status messages
            if 'status' in translated_data:
                status_key = translated_data['status'].lower().replace(' ', '_')
                translated_data['status_translated'] = self.get_text(status_key, translated_data['status'])
            
            return translated_data
            
        except Exception as e:
            logger.error(f"Campaign data translation error: {e}")
            return campaign_data
    
    def get_language_specific_formatting(self) -> Dict[str, Any]:
        """Get language-specific formatting preferences"""
        current_lang = st.session_state.get('language', self.current_language)
        
        formatting = {
            'English': {
                'currency_symbol': '₹',
                'currency_position': 'before',
                'date_format': 'DD/MM/YYYY',
                'number_separator': ',',
                'text_direction': 'ltr'
            },
            'Hindi': {
                'currency_symbol': '₹',
                'currency_position': 'before',
                'date_format': 'DD/MM/YYYY',
                'number_separator': ',',
                'text_direction': 'ltr'
            },
            'Tamil': {
                'currency_symbol': '₹',
                'currency_position': 'before',
                'date_format': 'DD/MM/YYYY',
                'number_separator': ',',
                'text_direction': 'ltr'
            },
            'Telugu': {
                'currency_symbol': '₹',
                'currency_position': 'before',
                'date_format': 'DD/MM/YYYY',
                'number_separator': ',',
                'text_direction': 'ltr'
            }
        }
        
        return formatting.get(current_lang, formatting['English'])
    
    def format_currency(self, amount: float) -> str:
        """Format currency based on current language"""
        try:
            formatting = self.get_language_specific_formatting()
            
            # Format number with separators
            formatted_amount = f"{amount:,.0f}"
            
            # Add currency symbol
            if formatting['currency_position'] == 'before':
                return f"{formatting['currency_symbol']}{formatted_amount}"
            else:
                return f"{formatted_amount} {formatting['currency_symbol']}"
                
        except Exception as e:
            logger.error(f"Currency formatting error: {e}")
            return f"₹{amount:,.0f}"

# Global translation service instance
translation_service = TranslationService()

def t(key: str, default: Optional[str] = None) -> str:
    """Shorthand function for getting translated text"""
    return translation_service.get_text(key, default)

def set_language(language: str):
    """Shorthand function for setting language"""
    translation_service.set_language(language)

def get_supported_languages() -> Dict[str, str]:
    """Shorthand function for getting supported languages"""
    return translation_service.get_supported_languages()

def format_currency(amount: float) -> str:
    """Shorthand function for formatting currency"""
    return translation_service.format_currency(amount)

