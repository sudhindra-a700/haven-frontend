"""

# Import utilities with error handling
try:
    from utils.translation_service import t, format_currency
    from utils.auth_utils import get_current_user
    from utils.api_client import *
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

Campaign Management Page for HAVEN Crowdfunding Platform
Create and manage crowdfunding campaigns
"""

import streamlit as st
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def show():
    """
    Render the campaign management page
    """
    try:
        # Page header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: #2e7d32; font-size: 2.5rem; margin-bottom: 1rem;">
                🎯 Campaign Management
            </h1>
            <p style="color: #388e3c; font-size: 1.2rem;">
                Create, manage, and track your crowdfunding campaigns
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tab navigation
        tab1, tab2, tab3 = st.tabs(["🚀 Create Campaign", "📊 My Campaigns", "📈 Analytics"])
        
        with tab1:
            show_create_campaign()
        
        with tab2:
            show_my_campaigns()
        
        with tab3:
            show_campaign_analytics()
        
    except Exception as e:
        logger.error(f"Error rendering campaign page: {e}")
        st.error("Sorry, there was an error loading the campaign page. Please try refreshing.")
        st.exception(e)

def show_create_campaign():
    """Show campaign creation form"""
    st.markdown("### 🚀 Create New Campaign")
    
    with st.form("create_campaign_form"):
        # Basic Information
        st.markdown("#### 📝 Basic Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_title = st.text_input(
                "🎯 Campaign Title *",
                placeholder="Enter a compelling campaign title...",
                help="Make it clear and engaging (max 100 characters)"
            )
            
            category = st.selectbox(
                "📂 Category *",
                ["Medical", "Education", "Disaster Relief", "Animal Welfare", 
                 "Environment", "Community Development", "Technology", 
                 "Social Causes", "Arts & Culture", "Sports"],
                help="Choose the category that best fits your campaign"
            )
            
            funding_goal = st.number_input(
                "💰 Funding Goal (₹) *",
                min_value=1000,
                max_value=50000000,
                value=100000,
                step=1000,
                help="Set a realistic funding target"
            )
        
        with col2:
            campaign_duration = st.number_input(
                "📅 Campaign Duration (days) *",
                min_value=1,
                max_value=365,
                value=30,
                help="How long should your campaign run?"
            )
            
            location = st.text_input(
                "📍 Location *",
                placeholder="City, State",
                help="Where is your campaign based?"
            )
            
            beneficiary_type = st.selectbox(
                "👥 Beneficiary Type *",
                ["Individual", "Family", "Community", "Organization", "Animals", "Environment"],
                help="Who will benefit from this campaign?"
            )
        
        # Campaign Description
        st.markdown("#### 📖 Campaign Description")
        
        campaign_description = st.text_area(
            "📝 Tell Your Story *",
            placeholder="Describe your campaign in detail. Explain why it's important, how the funds will be used, and the impact it will make...",
            height=200,
            help="A compelling story increases donations. Be honest and detailed."
        )
        
        # Media Upload
        st.markdown("#### 📸 Media & Documents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_image = st.file_uploader(
                "🖼️ Campaign Image *",
                type=['jpg', 'jpeg', 'png'],
                help="Upload a high-quality image that represents your campaign"
            )
            
            additional_images = st.file_uploader(
                "📷 Additional Images",
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True,
                help="Upload up to 5 additional images"
            )
        
        with col2:
            campaign_video = st.file_uploader(
                "🎥 Campaign Video",
                type=['mp4', 'avi', 'mov'],
                help="A video can significantly increase engagement"
            )
            
            supporting_documents = st.file_uploader(
                "📄 Supporting Documents",
                type=['pdf', 'doc', 'docx'],
                accept_multiple_files=True,
                help="Medical reports, certificates, etc."
            )
        
        # Fund Usage Plan
        st.markdown("#### 💰 Fund Usage Plan")
        
        fund_breakdown = st.text_area(
            "📊 How will you use the funds? *",
            placeholder="Provide a detailed breakdown of how the funds will be used:\n- Medical expenses: ₹50,000\n- Hospital charges: ₹30,000\n- Medicines: ₹20,000",
            height=150,
            help="Transparency builds trust with donors"
        )
        
        # Contact Information
        st.markdown("#### 📞 Contact Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            contact_name = st.text_input(
                "👤 Contact Person *",
                placeholder="Full name of contact person",
                help="Person responsible for the campaign"
            )
            
            contact_phone = st.text_input(
                "📱 Phone Number *",
                placeholder="+91 XXXXX XXXXX",
                help="Primary contact number"
            )
        
        with col2:
            contact_email = st.text_input(
                "📧 Email Address *",
                placeholder="contact@example.com",
                help="Email for campaign communications"
            )
            
            organization_name = st.text_input(
                "🏢 Organization Name",
                placeholder="If applicable",
                help="Name of organization running the campaign"
            )
        
        # Verification Documents
        st.markdown("#### ✅ Verification & Legal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            identity_proof = st.file_uploader(
                "🆔 Identity Proof *",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                help="Aadhaar, PAN, or other government ID"
            )
            
            address_proof = st.file_uploader(
                "🏠 Address Proof *",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                help="Utility bill, bank statement, etc."
            )
        
        with col2:
            medical_documents = st.file_uploader(
                "🏥 Medical Documents",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                accept_multiple_files=True,
                help="For medical campaigns only"
            )
            
            ngo_certificate = st.file_uploader(
                "📜 NGO Certificate",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                help="For NGO campaigns only"
            )
        
        # Terms and Conditions
        st.markdown("#### 📋 Terms & Conditions")
        
        terms_accepted = st.checkbox(
            "I agree to the Terms of Service and Campaign Guidelines *",
            help="Required to create a campaign"
        )
        
        fraud_declaration = st.checkbox(
            "I declare that all information provided is true and accurate *",
            help="False information may result in campaign suspension"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            submit_campaign = st.form_submit_button(
                "🚀 Create Campaign",
                use_container_width=True,
                type="primary"
            )
    
    # Handle form submission
    if submit_campaign:
        handle_campaign_creation(
            campaign_title, category, funding_goal, campaign_duration,
            location, beneficiary_type, campaign_description, fund_breakdown,
            contact_name, contact_phone, contact_email, organization_name,
            terms_accepted, fraud_declaration
        )

def show_my_campaigns():
    """Show user's existing campaigns"""
    st.markdown("### 📊 My Campaigns")
    
    # Campaign statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Total Campaigns", "3", "+1 this month")
    
    with col2:
        st.metric("💰 Total Raised", "₹2,45,000", "+₹15,000 this week")
    
    with col3:
        st.metric("👥 Total Supporters", "156", "+12 this week")
    
    with col4:
        st.metric("📈 Success Rate", "67%", "+10% improvement")
    
    # Campaign list
    st.markdown("---")
    campaigns = get_user_campaigns()
    
    for campaign in campaigns:
        with st.expander(f"{campaign['status_icon']} {campaign['title']} - {campaign['status']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Category:** {campaign['category']}")
                st.markdown(f"**Goal:** ₹{campaign['goal']:,}")
                st.markdown(f"**Raised:** ₹{campaign['raised']:,} ({campaign['percentage']:.1f}%)")
                st.markdown(f"**Supporters:** {campaign['supporters']}")
                st.markdown(f"**Days Left:** {campaign['days_left']}")
                st.markdown(f"**Created:** {campaign['created_date']}")
                
                # Progress bar
                progress = campaign['percentage'] / 100
                st.progress(progress)
            
            with col2:
                # Action buttons
                if st.button(f"📊 View Analytics", key=f"analytics_{campaign['id']}"):
                    view_campaign_analytics(campaign['id'])
                
                if st.button(f"✏️ Edit Campaign", key=f"edit_{campaign['id']}"):
                    edit_campaign(campaign['id'])
                
                if st.button(f"📤 Share Campaign", key=f"share_{campaign['id']}"):
                    share_campaign(campaign['id'])
                
                if campaign['status'] == 'Active':
                    if st.button(f"⏸️ Pause", key=f"pause_{campaign['id']}"):
                        pause_campaign(campaign['id'])
                
                if st.button(f"💬 Messages", key=f"messages_{campaign['id']}"):
                    view_campaign_messages(campaign['id'])

def show_campaign_analytics():
    """Show campaign analytics and insights"""
    st.markdown("### 📈 Campaign Analytics")
    
    # Select campaign for analytics
    campaigns = get_user_campaigns()
    campaign_options = {f"{c['title']} ({c['status']})": c['id'] for c in campaigns}
    
    selected_campaign = st.selectbox(
        "📊 Select Campaign",
        options=list(campaign_options.keys()),
        help="Choose a campaign to view detailed analytics"
    )
    
    if selected_campaign:
        campaign_id = campaign_options[selected_campaign]
        campaign = next(c for c in campaigns if c['id'] == campaign_id)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Total Raised", f"₹{campaign['raised']:,}", "+₹5,000 this week")
        
        with col2:
            st.metric("👥 Supporters", campaign['supporters'], "+8 this week")
        
        with col3:
            st.metric("👀 Page Views", "2,456", "+234 this week")
        
        with col4:
            st.metric("📤 Shares", "89", "+12 this week")
        
        # Charts and graphs would go here
        st.markdown("---")
        st.markdown("#### 📊 Funding Progress Over Time")
        st.info("📈 Interactive charts showing donation trends, supporter growth, and engagement metrics would be displayed here.")
        
        st.markdown("#### 🌍 Supporter Demographics")
        st.info("🗺️ Geographic distribution and demographic breakdown of supporters would be shown here.")
        
        st.markdown("#### 💡 Insights & Recommendations")
        st.success("✅ Your campaign is performing well! Consider adding more updates to maintain engagement.")
        st.info("💡 Tip: Campaigns with regular updates receive 40% more donations on average.")

def get_user_campaigns() -> List[Dict[str, Any]]:
    """Get user's campaigns data"""
    return [
        {
            'id': 'camp_001',
            'title': 'Emergency Medical Support',
            'category': 'Medical',
            'goal': 500000,
            'raised': 325000,
            'percentage': 65.0,
            'supporters': 89,
            'days_left': 12,
            'status': 'Active',
            'status_icon': '🟢',
            'created_date': '2024-07-15'
        },
        {
            'id': 'camp_002',
            'title': 'School Infrastructure Project',
            'category': 'Education',
            'goal': 200000,
            'raised': 200000,
            'percentage': 100.0,
            'supporters': 67,
            'days_left': 0,
            'status': 'Completed',
            'status_icon': '✅',
            'created_date': '2024-06-01'
        },
        {
            'id': 'camp_003',
            'title': 'Animal Shelter Renovation',
            'category': 'Animal Welfare',
            'goal': 150000,
            'raised': 45000,
            'percentage': 30.0,
            'supporters': 23,
            'days_left': 25,
            'status': 'Under Review',
            'status_icon': '🟡',
            'created_date': '2024-07-28'
        }
    ]

def handle_campaign_creation(campaign_title, category, funding_goal, campaign_duration,
                           location, beneficiary_type, campaign_description, fund_breakdown,
                           contact_name, contact_phone, contact_email, organization_name,
                           terms_accepted, fraud_declaration):
    """Handle campaign creation form submission"""
    try:
        # Validation
        errors = []
        
        if not campaign_title or len(campaign_title) < 10:
            errors.append("Campaign title must be at least 10 characters long")
        
        if not campaign_description or len(campaign_description) < 100:
            errors.append("Campaign description must be at least 100 characters long")
        
        if not fund_breakdown:
            errors.append("Fund usage plan is required")
        
        if not contact_name or not contact_phone or not contact_email:
            errors.append("All contact information fields are required")
        
        if not terms_accepted or not fraud_declaration:
            errors.append("You must accept the terms and conditions")
        
        # Display errors
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
            return
        
        # Process campaign creation
        with st.spinner("Creating your campaign..."):
            import time
            time.sleep(3)
            
            st.success("🎉 Campaign created successfully!")
            st.balloons()
            
            st.info("""
            ### 🎊 What's Next?
            
            Your campaign has been submitted for review. Here's what happens next:
            
            1. **📋 Review Process** (1-2 business days)
               - Our team will verify your documents
               - We'll check for completeness and authenticity
            
            2. **✅ Approval & Launch**
               - Once approved, your campaign will go live
               - You'll receive an email confirmation
            
            3. **📢 Promotion Tips**
               - Share with friends and family first
               - Use social media to spread awareness
               - Provide regular updates to maintain engagement
            
            **📞 Need Help?** Contact our support team if you have any questions.
            """)
            
    except Exception as e:
        logger.error(f"Campaign creation error: {e}")
        st.error("❌ Campaign creation failed. Please try again.")

def view_campaign_analytics(campaign_id: str):
    """View detailed analytics for a specific campaign"""
    st.info(f"📊 Loading detailed analytics for campaign {campaign_id}...")

def edit_campaign(campaign_id: str):
    """Edit an existing campaign"""
    st.info(f"✏️ Opening campaign editor for {campaign_id}...")

def share_campaign(campaign_id: str):
    """Share campaign on social media"""
    st.success(f"📤 Campaign {campaign_id} sharing options opened!")

def pause_campaign(campaign_id: str):
    """Pause an active campaign"""
    st.warning(f"⏸️ Campaign {campaign_id} has been paused.")

def view_campaign_messages(campaign_id: str):
    """View messages and comments for a campaign"""
    st.info(f"💬 Loading messages for campaign {campaign_id}...")

# Legacy function support
def render_campaign_page(api_client=None):
    """Legacy function name support - redirects to show()"""
    show()

