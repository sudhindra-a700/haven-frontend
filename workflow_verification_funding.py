"""
UPDATED Verification and Funding Workflow Pages for HAVEN
Integrates with fixed OAuth authentication system
Implements: Admin Review → Verification → Browse → View → Fund → Payment → Success
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import logging
import time
import random
from datetime import datetime, timedelta

# Import updated authentication utilities
from workflow_auth_utils import (
    get_auth_manager, 
    require_authentication, 
    require_role, 
    get_user_role,
    check_user_authentication
)

logger = logging.getLogger(__name__)

def render_admin_review_page(workflow_manager):
    """UPDATED: Render admin review page - shows campaign under review with authentication"""
    
    # Require authentication
    if not require_authentication():
        return
    
    # Get current campaign from session state
    campaign = st.session_state.get('current_campaign')
    
    if not campaign:
        st.error("❌ No campaign selected for review")
        return
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;'>
        <h2 style='color: #f57c00; margin: 0;'>🔍 Admin Review in Progress</h2>
        <p style='color: #ef6c00; margin: 0;'>Campaign "{campaign.get('basic_info', {}).get('title', 'your campaign')}" is being reviewed by our team</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Review status
    st.markdown("### 📊 Review Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📝 Review Stage", "Manual Review")
    
    with col2:
        st.metric("⏰ Estimated Review Time", "24-48 hours")
    
    with col3:
        auth_time = datetime.fromtimestamp(campaign.get('created_at', time.time()))
        st.metric("📅 Submitted", auth_time.strftime("%Y-%m-%d %H:%M"))
    
    # Review progress
    st.markdown("### 🔄 Review Progress")
    
    progress_steps = [
        ("📥 Received", True, "Campaign received and queued for review"),
        ("🤖 AI Check", True, "Automated compliance and completeness check"),
        ("👥 Manual Review", True, "Human review of campaign details and documents"),
        ("✅ Decision", False, "Final approval or feedback"),
        ("🚀 Launch", False, "Campaign goes live on platform")
    ]
    
    for step_name, completed, description in progress_steps:
        if completed:
            st.success(f"✅ **{step_name}**: {description}")
        else:
            st.info(f"⏳ **{step_name}**: {description}")
    
    # Campaign summary
    st.markdown("### 📋 Campaign Summary")
    
    with st.expander("View Campaign Details", expanded=False):
        basic_info = campaign.get('basic_info', {})
        details = campaign.get('details', {})
        funding = campaign.get('funding', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Basic Information:**")
            st.write(f"• **Title:** {basic_info.get('title', 'N/A')}")
            st.write(f"• **Category:** {basic_info.get('category', 'N/A')}")
            st.write(f"• **Location:** {basic_info.get('location', 'N/A')}")
            st.write(f"• **Urgency:** {basic_info.get('urgency_level', 'N/A')}")
        
        with col2:
            st.markdown("**Funding Information:**")
            st.write(f"• **Target:** ${funding.get('funding_target', 0):,}")
            st.write(f"• **Minimum:** ${funding.get('minimum_funding', 0):,}")
            st.write(f"• **Currency:** {funding.get('currency', 'USD')}")
            st.write(f"• **Type:** {funding.get('funding_type', 'N/A')}")
    
    # What happens next
    st.markdown("### 🔮 What Happens Next?")
    
    st.info("""
    **Review Process:**
    
    1. **Document Verification**: Our team verifies all uploaded documents and organization credentials
    2. **Content Review**: Campaign content is reviewed for compliance with our guidelines
    3. **Risk Assessment**: We assess the campaign for potential risks and authenticity
    4. **Final Decision**: Campaign is either approved, requires modifications, or is declined
    
    **You will be notified via email once the review is complete.**
    """)
    
    # Contact support
    st.markdown("### 📞 Need Help?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📧 Contact Support", use_container_width=True):
            st.info("📧 Please email support@haven-platform.org for assistance")
    
    with col2:
        if st.button("📚 Review Guidelines", use_container_width=True):
            st.info("📚 Review our campaign guidelines for more information")
    
    # Refresh status
    if st.button("🔄 Refresh Status", use_container_width=True, type="primary"):
        st.experimental_rerun()

def render_campaign_browse_page(workflow_manager):
    """UPDATED: Render campaign browsing page with authentication"""
    
    # Require authentication for browsing
    if not require_authentication():
        return
    
    st.markdown("### 🔍 Browse Campaigns")
    st.markdown("Discover and support amazing causes in your community and beyond")
    
    # Search and filter section
    st.markdown("#### 🔎 Search & Filter")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input(
            "Search campaigns",
            placeholder="Enter keywords...",
            key="campaign_search"
        )
    
    with col2:
        category_filter = st.selectbox(
            "Category",
            options=["All Categories", "Medical", "Education", "Disaster Relief", 
                    "Community Development", "Environment", "Animal Welfare"],
            key="category_filter"
        )
    
    with col3:
        location_filter = st.text_input(
            "Location",
            placeholder="City, State, Country",
            key="location_filter"
        )
    
    # Additional filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        urgency_filter = st.selectbox(
            "Urgency Level",
            options=["All Levels", "Critical", "High", "Medium", "Low"],
            key="urgency_filter"
        )
    
    with col2:
        funding_range = st.selectbox(
            "Funding Range",
            options=["All Amounts", "Under $1K", "$1K-$5K", "$5K-$25K", "$25K-$100K", "Over $100K"],
            key="funding_filter"
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            options=["Most Recent", "Ending Soon", "Most Funded", "Least Funded", "Alphabetical"],
            key="sort_filter"
        )
    
    # Mock campaign data (in real implementation, this would come from backend)
    campaigns = get_mock_campaigns()
    
    # Apply filters (simplified for demo)
    filtered_campaigns = campaigns
    
    if search_query:
        filtered_campaigns = [c for c in filtered_campaigns 
                            if search_query.lower() in c['title'].lower() 
                            or search_query.lower() in c['description'].lower()]
    
    if category_filter != "All Categories":
        filtered_campaigns = [c for c in filtered_campaigns if c['category'] == category_filter]
    
    # Display campaigns
    st.markdown(f"#### 📊 Found {len(filtered_campaigns)} campaigns")
    
    if not filtered_campaigns:
        st.info("🔍 No campaigns found matching your criteria. Try adjusting your filters.")
        return
    
    # Campaign cards
    for i in range(0, len(filtered_campaigns), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(filtered_campaigns):
                render_campaign_card(filtered_campaigns[i])
        
        with col2:
            if i + 1 < len(filtered_campaigns):
                render_campaign_card(filtered_campaigns[i + 1])

def render_campaign_card(campaign):
    """UPDATED: Render individual campaign card with authentication"""
    
    with st.container():
        st.markdown(f"""
        <div style='border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin: 1rem 0; background: white;'>
            <h4 style='color: #4CAF50; margin-top: 0;'>{campaign['title']}</h4>
            <p style='color: #666; margin: 0.5rem 0;'><strong>Category:</strong> {campaign['category']}</p>
            <p style='color: #666; margin: 0.5rem 0;'><strong>Location:</strong> {campaign['location']}</p>
            <p style='margin: 1rem 0;'>{campaign['description'][:150]}...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        progress = campaign['raised'] / campaign['target']
        st.progress(progress)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Raised", f"${campaign['raised']:,}")
        
        with col2:
            st.metric("🎯 Target", f"${campaign['target']:,}")
        
        with col3:
            days_left = (campaign['end_date'] - datetime.now()).days
            st.metric("📅 Days Left", f"{max(0, days_left)}")
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"👁️ View Details", key=f"view_{campaign['id']}", use_container_width=True):
                st.session_state.selected_campaign = campaign
                st.session_state.page = "campaign_details"
                st.experimental_rerun()
        
        with col2:
            if st.button(f"💝 Donate Now", key=f"donate_{campaign['id']}", use_container_width=True, type="primary"):
                st.session_state.selected_campaign = campaign
                st.session_state.page = "donation"
                st.experimental_rerun()

def render_campaign_details_page(workflow_manager):
    """UPDATED: Render detailed campaign view with authentication"""
    
    # Require authentication
    if not require_authentication():
        return
    
    campaign = st.session_state.get('selected_campaign')
    
    if not campaign:
        st.error("❌ No campaign selected")
        return
    
    # Campaign header
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: #2e7d32; margin: 0;'>{campaign['title']}</h1>
        <p style='color: #388e3c; margin: 0.5rem 0;'>{campaign['category']} • {campaign['location']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Campaign stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Raised", f"${campaign['raised']:,}")
    
    with col2:
        st.metric("🎯 Target", f"${campaign['target']:,}")
    
    with col3:
        progress = (campaign['raised'] / campaign['target']) * 100
        st.metric("📊 Progress", f"{progress:.1f}%")
    
    with col4:
        days_left = (campaign['end_date'] - datetime.now()).days
        st.metric("📅 Days Left", f"{max(0, days_left)}")
    
    # Progress bar
    st.progress(campaign['raised'] / campaign['target'])
    
    # Campaign content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Description
        st.markdown("### 📖 Campaign Story")
        st.markdown(campaign['description'])
        
        # Updates (mock)
        st.markdown("### 📢 Campaign Updates")
        
        updates = [
            {"date": "2025-08-06", "title": "Thank you for your support!", "content": "We've reached 75% of our goal..."},
            {"date": "2025-08-04", "title": "Campaign milestone reached", "content": "Thanks to your generous donations..."},
            {"date": "2025-08-01", "title": "Campaign launched", "content": "We're excited to launch this campaign..."}
        ]
        
        for update in updates:
            with st.expander(f"{update['date']} - {update['title']}"):
                st.markdown(update['content'])
    
    with col2:
        # Donation section
        st.markdown("### 💝 Support This Campaign")
        
        # Quick donation amounts
        st.markdown("**Quick Donate:**")
        
        amounts = [25, 50, 100, 250, 500]
        
        for amount in amounts:
            if st.button(f"${amount}", key=f"quick_donate_{amount}", use_container_width=True):
                st.session_state.donation_amount = amount
                st.session_state.page = "donation"
                st.experimental_rerun()
        
        # Custom amount
        custom_amount = st.number_input(
            "Custom Amount ($)",
            min_value=1,
            max_value=10000,
            value=50,
            step=5
        )
        
        if st.button("💝 Donate Custom Amount", use_container_width=True, type="primary"):
            st.session_state.donation_amount = custom_amount
            st.session_state.selected_campaign = campaign
            st.session_state.page = "donation"
            st.experimental_rerun()
        
        # Share campaign
        st.markdown("### 📤 Share Campaign")
        
        if st.button("📱 Share on Social Media", use_container_width=True):
            st.info("📱 Share functionality would be implemented here")
        
        if st.button("📧 Share via Email", use_container_width=True):
            st.info("📧 Email sharing functionality would be implemented here")
        
        # Campaign organizer
        st.markdown("### 👥 Campaign Organizer")
        
        st.markdown(f"""
        **Organization:** {campaign.get('organizer', 'Haven Organization')}
        
        **Verified:** ✅ Verified Organization
        
        **Contact:** Available after donation
        """)
    
    # Back button
    if st.button("⬅️ Back to Browse", use_container_width=True):
        st.session_state.page = "browse"
        st.experimental_rerun()

def render_donation_page(workflow_manager):
    """UPDATED: Render donation page with authentication"""
    
    # Require authentication
    if not require_authentication():
        return
    
    campaign = st.session_state.get('selected_campaign')
    donation_amount = st.session_state.get('donation_amount', 50)
    
    if not campaign:
        st.error("❌ No campaign selected for donation")
        return
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h2 style='color: #1976d2; margin: 0;'>💝 Make a Donation</h2>
        <p style='color: #1565c0; margin: 0;'>Supporting: {campaign['title']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Donation form
    with st.form("donation_form"):
        # Donation amount
        st.markdown("### 💰 Donation Amount")
        
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input(
                "Donation Amount ($)",
                min_value=1,
                max_value=10000,
                value=donation_amount,
                step=5
            )
        
        with col2:
            currency = st.selectbox(
                "Currency",
                options=["USD", "EUR", "GBP", "CAD"],
                index=0
            )
        
        # Donation frequency
        frequency = st.radio(
            "Donation Frequency",
            options=["One-time", "Monthly", "Quarterly"],
            index=0,
            horizontal=True
        )
        
        # Personal information
        st.markdown("### 👤 Donor Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            donor_name = st.text_input(
                "Full Name *",
                placeholder="Enter your full name"
            )
            
            donor_email = st.text_input(
                "Email Address *",
                placeholder="your.email@example.com"
            )
        
        with col2:
            donor_phone = st.text_input(
                "Phone Number",
                placeholder="+1234567890"
            )
            
            anonymous = st.checkbox(
                "Make this donation anonymous",
                value=False
            )
        
        # Payment information
        st.markdown("### 💳 Payment Information")
        
        payment_method = st.selectbox(
            "Payment Method",
            options=["Credit Card", "Debit Card", "PayPal", "Bank Transfer"],
            index=0
        )
        
        if payment_method in ["Credit Card", "Debit Card"]:
            col1, col2 = st.columns(2)
            
            with col1:
                card_number = st.text_input(
                    "Card Number *",
                    placeholder="1234 5678 9012 3456",
                    type="password"
                )
                
                cardholder_name = st.text_input(
                    "Cardholder Name *",
                    placeholder="Name on card"
                )
            
            with col2:
                col2_1, col2_2 = st.columns(2)
                
                with col2_1:
                    expiry_date = st.text_input(
                        "Expiry Date *",
                        placeholder="MM/YY"
                    )
                
                with col2_2:
                    cvv = st.text_input(
                        "CVV *",
                        placeholder="123",
                        type="password"
                    )
        
        # Billing address
        st.markdown("### 🏠 Billing Address")
        
        col1, col2 = st.columns(2)
        
        with col1:
            billing_address = st.text_input(
                "Address *",
                placeholder="Street address"
            )
            
            billing_city = st.text_input(
                "City *",
                placeholder="City"
            )
        
        with col2:
            billing_state = st.text_input(
                "State/Province *",
                placeholder="State or province"
            )
            
            billing_zip = st.text_input(
                "ZIP/Postal Code *",
                placeholder="ZIP code"
            )
        
        # Additional options
        st.markdown("### ⚙️ Additional Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cover_fees = st.checkbox(
                "Cover processing fees (3.5%)",
                value=False,
                help="Help the campaign receive the full donation amount"
            )
            
            newsletter = st.checkbox(
                "Subscribe to campaign updates",
                value=True
            )
        
        with col2:
            tax_receipt = st.checkbox(
                "Email me a tax receipt",
                value=True
            )
            
            share_info = st.checkbox(
                "Share my contact info with organizer",
                value=False
            )
        
        # Donation summary
        st.markdown("### 📊 Donation Summary")
        
        processing_fee = amount * 0.035 if cover_fees else 0
        total_amount = amount + processing_fee
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💝 Donation", f"${amount:.2f}")
        
        with col2:
            st.metric("💳 Processing Fee", f"${processing_fee:.2f}")
        
        with col3:
            st.metric("💰 Total", f"${total_amount:.2f}")
        
        # Terms and submit
        terms_accepted = st.checkbox(
            "I agree to the Terms of Service and Privacy Policy *",
            value=False
        )
        
        # Submit button
        submitted = st.form_submit_button(
            f"💝 Donate ${total_amount:.2f}",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Validation
            errors = []
            
            if not donor_name.strip():
                errors.append("Full name is required")
            if not donor_email.strip():
                errors.append("Email address is required")
            if payment_method in ["Credit Card", "Debit Card"]:
                if not card_number.strip():
                    errors.append("Card number is required")
                if not cardholder_name.strip():
                    errors.append("Cardholder name is required")
                if not expiry_date.strip():
                    errors.append("Expiry date is required")
                if not cvv.strip():
                    errors.append("CVV is required")
            if not billing_address.strip():
                errors.append("Billing address is required")
            if not billing_city.strip():
                errors.append("Billing city is required")
            if not billing_state.strip():
                errors.append("Billing state is required")
            if not billing_zip.strip():
                errors.append("Billing ZIP code is required")
            if not terms_accepted:
                errors.append("You must accept the terms and conditions")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Process donation (mock)
                process_donation(campaign, amount, donor_name, donor_email, anonymous)

def process_donation(campaign, amount, donor_name, donor_email, anonymous):
    """UPDATED: Process donation with authentication"""
    
    try:
        # Simulate payment processing
        with st.spinner("Processing your donation..."):
            time.sleep(2)  # Simulate processing time
        
        # Mock successful payment
        donation_id = f"DON-{int(time.time())}"
        
        st.success("🎉 **Donation Successful!**")
        
        st.markdown(f"""
        **Donation Details:**
        - **Donation ID:** {donation_id}
        - **Amount:** ${amount:.2f}
        - **Campaign:** {campaign['title']}
        - **Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        **What happens next:**
        - You'll receive an email confirmation shortly
        - Tax receipt will be sent within 24 hours
        - Campaign organizer will be notified of your support
        """)
        
        # Clear donation state
        if "donation_amount" in st.session_state:
            del st.session_state.donation_amount
        if "selected_campaign" in st.session_state:
            del st.session_state.selected_campaign
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 Return to Browse", use_container_width=True):
                st.session_state.page = "browse"
                st.experimental_rerun()
        
        with col2:
            if st.button("📧 Share Your Support", use_container_width=True, type="primary"):
                st.info("📧 Sharing functionality would be implemented here")
        
    except Exception as e:
        logger.error(f"Donation processing error: {e}")
        st.error(f"❌ Donation failed: {str(e)}")

def get_mock_campaigns():
    """Generate mock campaign data for demonstration"""
    
    campaigns = [
        {
            'id': 'camp_001',
            'title': 'Emergency Medical Fund for Children',
            'category': 'Medical',
            'location': 'New York, NY',
            'description': 'Help provide emergency medical care for children in need. Our hospital serves over 1000 children annually and needs support for critical equipment and treatments.',
            'target': 50000,
            'raised': 37500,
            'end_date': datetime.now() + timedelta(days=15),
            'organizer': 'Children\'s Medical Center'
        },
        {
            'id': 'camp_002',
            'title': 'School Supplies for Rural Education',
            'category': 'Education',
            'location': 'Rural Texas',
            'description': 'Providing essential school supplies and learning materials to underserved rural schools. Help us bridge the education gap and give every child a chance to succeed.',
            'target': 25000,
            'raised': 18750,
            'end_date': datetime.now() + timedelta(days=22),
            'organizer': 'Rural Education Foundation'
        },
        {
            'id': 'camp_003',
            'title': 'Clean Water Initiative',
            'category': 'Environment',
            'location': 'Kenya, Africa',
            'description': 'Building clean water wells in remote villages to provide safe drinking water. Each well serves approximately 500 people and dramatically improves health outcomes.',
            'target': 75000,
            'raised': 45000,
            'end_date': datetime.now() + timedelta(days=30),
            'organizer': 'Global Water Project'
        },
        {
            'id': 'camp_004',
            'title': 'Animal Shelter Renovation',
            'category': 'Animal Welfare',
            'location': 'Los Angeles, CA',
            'description': 'Renovating our animal shelter to provide better care for rescued animals. The new facility will house 200+ animals and include modern medical facilities.',
            'target': 100000,
            'raised': 65000,
            'end_date': datetime.now() + timedelta(days=45),
            'organizer': 'City Animal Rescue'
        }
    ]
    
    return campaigns

# Utility functions for workflow management
def get_campaign_by_id(campaign_id: str) -> Optional[Dict[str, Any]]:
    """UPDATED: Get campaign by ID with authentication"""
    
    if not check_user_authentication():
        return None
    
    # In real implementation, this would fetch from backend
    campaigns = get_mock_campaigns()
    return next((c for c in campaigns if c['id'] == campaign_id), None)

def get_user_donations(user_id: str) -> List[Dict[str, Any]]:
    """UPDATED: Get user's donation history with authentication"""
    
    if not check_user_authentication():
        return []
    
    # In real implementation, this would fetch from backend
    return []

def get_donation_receipt(donation_id: str) -> Optional[Dict[str, Any]]:
    """UPDATED: Get donation receipt with authentication"""
    
    if not check_user_authentication():
        return None
    
    # In real implementation, this would fetch from backend
    return None
