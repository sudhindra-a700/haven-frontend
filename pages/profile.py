"""

# Import utilities with error handling
try:
    from utils.translation_service import t, format_currency
    from utils.auth_utils import get_current_user
    from utils.api_client import *
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

Profile Page for HAVEN Crowdfunding Platform
User account management and settings
"""

import streamlit as st
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def show():
    """
    Render the user profile page
    """
    try:
        # Page header
        user = st.session_state.get('user', {})
        user_name = user.get('name', 'User')
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: #2e7d32; font-size: 2.5rem; margin-bottom: 1rem;">
                👤 {user_name}'s Profile
            </h1>
            <p style="color: #388e3c; font-size: 1.2rem;">
                Manage your account, campaigns, and preferences
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tab navigation
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "👤 Personal Info", 
            "🎯 My Campaigns", 
            "💝 My Donations", 
            "⚙️ Settings", 
            "📊 Activity"
        ])
        
        with tab1:
            show_personal_info()
        
        with tab2:
            show_user_campaigns()
        
        with tab3:
            show_user_donations()
        
        with tab4:
            show_user_settings()
        
        with tab5:
            show_user_activity()
        
    except Exception as e:
        logger.error(f"Error rendering profile page: {e}")
        st.error("Sorry, there was an error loading the profile page. Please try refreshing.")
        st.exception(e)

def show_personal_info():
    """Show and edit personal information"""
    st.markdown("### 👤 Personal Information")
    
    user = st.session_state.get('user', {})
    
    with st.form("personal_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Profile picture
            st.markdown("#### 📸 Profile Picture")
            current_avatar = user.get('avatar', '👤')
            st.markdown(f"<div style='font-size: 4rem; text-align: center;'>{current_avatar}</div>", 
                       unsafe_allow_html=True)
            
            profile_picture = st.file_uploader(
                "Upload new profile picture",
                type=['jpg', 'jpeg', 'png'],
                help="Upload a clear photo of yourself"
            )
            
            # Basic information
            first_name = st.text_input(
                "👤 First Name",
                value=user.get('name', '').split(' ')[0] if user.get('name') else '',
                placeholder="Enter your first name"
            )
            
            last_name = st.text_input(
                "👤 Last Name", 
                value=' '.join(user.get('name', '').split(' ')[1:]) if user.get('name') and len(user.get('name', '').split(' ')) > 1 else '',
                placeholder="Enter your last name"
            )
            
            email = st.text_input(
                "📧 Email Address",
                value=user.get('email', ''),
                placeholder="your.email@example.com",
                disabled=True,
                help="Email cannot be changed. Contact support if needed."
            )
        
        with col2:
            # Contact information
            phone = st.text_input(
                "📱 Phone Number",
                value=user.get('phone', ''),
                placeholder="+91 XXXXX XXXXX"
            )
            
            date_of_birth = st.date_input(
                "🎂 Date of Birth",
                help="This helps us provide age-appropriate content"
            )
            
            gender = st.selectbox(
                "⚧ Gender",
                ["Prefer not to say", "Male", "Female", "Non-binary", "Other"]
            )
            
            # Address information
            st.markdown("#### 🏠 Address")
            
            address_line1 = st.text_input(
                "Address Line 1",
                placeholder="Street address, apartment, suite, etc."
            )
            
            col_city, col_state = st.columns(2)
            with col_city:
                city = st.text_input("City", placeholder="Your city")
            with col_state:
                state = st.text_input("State", placeholder="Your state")
            
            col_pincode, col_country = st.columns(2)
            with col_pincode:
                pincode = st.text_input("PIN Code", placeholder="123456")
            with col_country:
                country = st.selectbox("Country", ["India", "Other"])
        
        # Bio section
        st.markdown("#### 📝 About Me")
        bio = st.text_area(
            "Tell others about yourself",
            placeholder="Share a bit about yourself, your interests, and what causes you care about...",
            height=100,
            help="This will be visible on your public profile"
        )
        
        # Social media links
        st.markdown("#### 🌐 Social Media")
        col1, col2 = st.columns(2)
        
        with col1:
            facebook_url = st.text_input(
                "📘 Facebook",
                placeholder="https://facebook.com/yourprofile"
            )
            
            linkedin_url = st.text_input(
                "💼 LinkedIn",
                placeholder="https://linkedin.com/in/yourprofile"
            )
        
        with col2:
            twitter_url = st.text_input(
                "🐦 Twitter",
                placeholder="https://twitter.com/yourhandle"
            )
            
            instagram_url = st.text_input(
                "📷 Instagram",
                placeholder="https://instagram.com/yourhandle"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            update_profile = st.form_submit_button(
                "💾 Update Profile",
                use_container_width=True,
                type="primary"
            )
    
    if update_profile:
        handle_profile_update(first_name, last_name, phone, bio)

def show_user_campaigns():
    """Show user's campaigns"""
    st.markdown("### 🎯 My Campaigns")
    
    # Campaign statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Campaigns", "3", "+1 this month")
    
    with col2:
        st.metric("💰 Total Raised", "₹2,45,000", "+₹15,000 this week")
    
    with col3:
        st.metric("👥 Total Supporters", "156", "+12 this week")
    
    with col4:
        st.metric("🏆 Success Rate", "67%", "+10% improvement")
    
    # Quick actions
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Create New Campaign", use_container_width=True):
            st.session_state.current_page = 'campaign'
            st.rerun()
    
    with col2:
        if st.button("📊 View All Analytics", use_container_width=True):
            st.info("📈 Opening comprehensive analytics dashboard...")
    
    # Recent campaigns
    st.markdown("---")
    st.markdown("#### 📋 Recent Campaigns")
    
    campaigns = get_user_campaigns_summary()
    
    for campaign in campaigns:
        with st.expander(f"{campaign['status_icon']} {campaign['title']} - {campaign['status']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Goal:** ₹{campaign['goal']:,}")
                st.markdown(f"**Raised:** ₹{campaign['raised']:,} ({campaign['percentage']:.1f}%)")
                st.markdown(f"**Supporters:** {campaign['supporters']}")
                st.markdown(f"**Created:** {campaign['created_date']}")
                
                # Progress bar
                progress = campaign['percentage'] / 100
                st.progress(progress)
            
            with col2:
                if st.button(f"📊 Analytics", key=f"prof_analytics_{campaign['id']}"):
                    st.info(f"Loading analytics for {campaign['title']}...")
                
                if st.button(f"✏️ Edit", key=f"prof_edit_{campaign['id']}"):
                    st.info(f"Opening editor for {campaign['title']}...")

def show_user_donations():
    """Show user's donation history"""
    st.markdown("### 💝 My Donations")
    
    # Donation statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Donated", "₹45,600", "+₹2,500 this month")
    
    with col2:
        st.metric("🎯 Campaigns Supported", "23", "+3 this month")
    
    with col3:
        st.metric("🏆 Impact Score", "8.7/10", "+0.3 this month")
    
    with col4:
        st.metric("📅 Member Since", "Jan 2024", "8 months")
    
    # Donation filters
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_filter = st.selectbox(
            "📅 Time Period",
            ["All Time", "This Year", "Last 6 Months", "Last 3 Months", "This Month"]
        )
    
    with col2:
        category_filter = st.selectbox(
            "📂 Category",
            ["All Categories", "Medical", "Education", "Disaster Relief", "Animal Welfare"]
        )
    
    with col3:
        amount_filter = st.selectbox(
            "💰 Amount Range",
            ["All Amounts", "₹1-500", "₹501-2000", "₹2001-5000", "₹5000+"]
        )
    
    # Donation history
    st.markdown("---")
    st.markdown("#### 📋 Donation History")
    
    donations = get_user_donations()
    
    for donation in donations:
        with st.expander(f"💝 ₹{donation['amount']:,} to {donation['campaign_title']} - {donation['date']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Campaign:** {donation['campaign_title']}")
                st.markdown(f"**Organizer:** {donation['organizer']}")
                st.markdown(f"**Category:** {donation['category']}")
                st.markdown(f"**Amount:** ₹{donation['amount']:,}")
                st.markdown(f"**Date:** {donation['date']}")
                st.markdown(f"**Status:** {donation['status']}")
                
                if donation.get('message'):
                    st.markdown(f"**Your Message:** {donation['message']}")
            
            with col2:
                if st.button(f"📄 Receipt", key=f"receipt_{donation['id']}"):
                    download_receipt(donation['id'])
                
                if st.button(f"📊 Impact", key=f"impact_{donation['id']}"):
                    view_donation_impact(donation['id'])
                
                if donation['status'] == 'Completed':
                    st.success("✅ Completed")
                elif donation['status'] == 'Processing':
                    st.warning("⏳ Processing")

def show_user_settings():
    """Show user settings and preferences"""
    st.markdown("### ⚙️ Settings & Preferences")
    
    # Notification settings
    st.markdown("#### 🔔 Notification Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        email_notifications = st.checkbox(
            "📧 Email Notifications",
            value=True,
            help="Receive updates about your campaigns and donations"
        )
        
        campaign_updates = st.checkbox(
            "📢 Campaign Updates",
            value=True,
            help="Get notified when campaigns you support post updates"
        )
        
        donation_receipts = st.checkbox(
            "🧾 Donation Receipts",
            value=True,
            help="Automatically receive donation receipts via email"
        )
    
    with col2:
        sms_notifications = st.checkbox(
            "📱 SMS Notifications",
            value=False,
            help="Receive important updates via SMS"
        )
        
        marketing_emails = st.checkbox(
            "📬 Marketing Emails",
            value=False,
            help="Receive newsletters and promotional content"
        )
        
        push_notifications = st.checkbox(
            "🔔 Push Notifications",
            value=True,
            help="Browser push notifications for urgent updates"
        )
    
    # Privacy settings
    st.markdown("---")
    st.markdown("#### 🔒 Privacy Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        public_profile = st.checkbox(
            "👁️ Public Profile",
            value=True,
            help="Make your profile visible to other users"
        )
        
        show_donations = st.checkbox(
            "💝 Show Donation History",
            value=False,
            help="Display your donations on your public profile"
        )
    
    with col2:
        show_campaigns = st.checkbox(
            "🎯 Show My Campaigns",
            value=True,
            help="Display campaigns you've created on your profile"
        )
        
        allow_messages = st.checkbox(
            "💬 Allow Messages",
            value=True,
            help="Let other users send you messages"
        )
    
    # Language and region
    st.markdown("---")
    st.markdown("#### 🌍 Language & Region")
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox(
            "🗣️ Language",
            ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi"],
            help="Choose your preferred language"
        )
        
        currency = st.selectbox(
            "💱 Currency",
            ["INR (₹)", "USD ($)", "EUR (€)"],
            help="Display currency preference"
        )
    
    with col2:
        timezone = st.selectbox(
            "🕐 Timezone",
            ["Asia/Kolkata", "Asia/Mumbai", "Asia/Delhi"],
            help="Your local timezone"
        )
        
        date_format = st.selectbox(
            "📅 Date Format",
            ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"],
            help="Preferred date display format"
        )
    
    # Account security
    st.markdown("---")
    st.markdown("#### 🔐 Account Security")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔑 Change Password", use_container_width=True):
            show_change_password_form()
        
        if st.button("📱 Two-Factor Authentication", use_container_width=True):
            setup_2fa()
    
    with col2:
        if st.button("🔗 Connected Accounts", use_container_width=True):
            show_connected_accounts()
        
        if st.button("📋 Download My Data", use_container_width=True):
            download_user_data()
    
    # Save settings
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Save Settings", use_container_width=True, type="primary"):
            save_user_settings()

def show_user_activity():
    """Show user activity and statistics"""
    st.markdown("### 📊 Activity & Statistics")
    
    # Activity overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🎯 Campaign Activity
        - **Created:** 3 campaigns
        - **Active:** 1 campaign
        - **Completed:** 2 campaigns
        - **Total Raised:** ₹2,45,000
        """)
    
    with col2:
        st.markdown("""
        #### 💝 Donation Activity
        - **Total Donated:** ₹45,600
        - **Campaigns Supported:** 23
        - **Average Donation:** ₹1,983
        - **Last Donation:** 3 days ago
        """)
    
    with col3:
        st.markdown("""
        #### 🏆 Achievements
        - **Verified Donor** ✅
        - **Campaign Creator** 🎯
        - **Community Helper** 🤝
        - **Regular Supporter** 💝
        """)
    
    # Recent activity
    st.markdown("---")
    st.markdown("#### 📋 Recent Activity")
    
    activities = get_user_activities()
    
    for activity in activities:
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; 
                    margin-bottom: 0.5rem; border-left: 4px solid #4caf50;">
            <strong>{activity['icon']} {activity['action']}</strong><br>
            <small style="color: #666;">{activity['description']} • {activity['time']}</small>
        </div>
        """, unsafe_allow_html=True)

def get_user_campaigns_summary() -> List[Dict[str, Any]]:
    """Get summary of user's campaigns"""
    return [
        {
            'id': 'camp_001',
            'title': 'Emergency Medical Support',
            'goal': 500000,
            'raised': 325000,
            'percentage': 65.0,
            'supporters': 89,
            'status': 'Active',
            'status_icon': '🟢',
            'created_date': '2024-07-15'
        },
        {
            'id': 'camp_002',
            'title': 'School Infrastructure Project',
            'goal': 200000,
            'raised': 200000,
            'percentage': 100.0,
            'supporters': 67,
            'status': 'Completed',
            'status_icon': '✅',
            'created_date': '2024-06-01'
        }
    ]

def get_user_donations() -> List[Dict[str, Any]]:
    """Get user's donation history"""
    return [
        {
            'id': 'don_001',
            'campaign_title': 'Child Heart Surgery',
            'organizer': 'Medical Foundation',
            'category': 'Medical',
            'amount': 5000,
            'date': '2024-08-01',
            'status': 'Completed',
            'message': 'Wishing the child a speedy recovery!'
        },
        {
            'id': 'don_002',
            'campaign_title': 'Flood Relief Kerala',
            'organizer': 'Disaster Response Team',
            'category': 'Disaster Relief',
            'amount': 2500,
            'date': '2024-07-28',
            'status': 'Completed',
            'message': 'Hope this helps the affected families.'
        },
        {
            'id': 'don_003',
            'campaign_title': 'Animal Shelter Support',
            'organizer': 'Paws & Hearts',
            'category': 'Animal Welfare',
            'amount': 1000,
            'date': '2024-07-25',
            'status': 'Processing',
            'message': ''
        }
    ]

def get_user_activities() -> List[Dict[str, Any]]:
    """Get user's recent activities"""
    return [
        {
            'icon': '💝',
            'action': 'Made a donation',
            'description': 'Donated ₹5,000 to Child Heart Surgery campaign',
            'time': '2 hours ago'
        },
        {
            'icon': '📢',
            'action': 'Campaign update',
            'description': 'Posted an update to Emergency Medical Support campaign',
            'time': '1 day ago'
        },
        {
            'icon': '🎯',
            'action': 'Campaign milestone',
            'description': 'Emergency Medical Support reached 60% funding goal',
            'time': '3 days ago'
        },
        {
            'icon': '👥',
            'action': 'New supporter',
            'description': 'Your campaign received a new supporter',
            'time': '5 days ago'
        },
        {
            'icon': '✅',
            'action': 'Profile verified',
            'description': 'Your profile verification was completed',
            'time': '1 week ago'
        }
    ]

def handle_profile_update(first_name, last_name, phone, bio):
    """Handle profile update"""
    try:
        with st.spinner("Updating your profile..."):
            import time
            time.sleep(2)
            
            # Update session state
            if 'user' not in st.session_state:
                st.session_state.user = {}
            
            st.session_state.user['name'] = f"{first_name} {last_name}"
            st.session_state.user['phone'] = phone
            st.session_state.user['bio'] = bio
            
            st.success("✅ Profile updated successfully!")
            
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        st.error("❌ Failed to update profile. Please try again.")

def show_change_password_form():
    """Show change password form"""
    st.info("🔑 Password change form would be displayed here.")

def setup_2fa():
    """Setup two-factor authentication"""
    st.info("📱 Two-factor authentication setup would be displayed here.")

def show_connected_accounts():
    """Show connected social accounts"""
    st.info("🔗 Connected accounts management would be displayed here.")

def download_user_data():
    """Download user data"""
    st.success("📋 Your data export has been initiated. You'll receive an email when ready.")

def save_user_settings():
    """Save user settings"""
    st.success("💾 Settings saved successfully!")

def download_receipt(donation_id: str):
    """Download donation receipt"""
    st.success(f"📄 Receipt for donation {donation_id} downloaded!")

def view_donation_impact(donation_id: str):
    """View donation impact"""
    st.info(f"📊 Loading impact report for donation {donation_id}...")

# Legacy function support
def render_profile_page(api_client=None):
    """Legacy function name support - redirects to show()"""
    show()

