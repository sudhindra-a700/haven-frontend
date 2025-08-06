"""
Verification and Funding Workflow Pages for HAVEN
Implements: Admin Review → Verification → Browse → View → Fund → Payment → Success
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import logging
import time
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def render_admin_review_page(workflow_manager):
    """Render admin review page - shows campaign under review"""
    st.markdown("### 👨‍💼 Admin Review in Progress")
    
    campaign = st.session_state.current_campaign
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #f57c00;">⏳ Under Manual Review</h2>
        <p style="color: #ef6c00; font-size: 1.2rem;">
            Campaign "{campaign.get('basic_info', {}).get('title', 'your campaign')}" is being reviewed by our verification team
        </p>
        <p style="color: #ff9800;">
            <strong>Estimated Review Time:</strong> 24-48 hours
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Review status
    st.markdown("### 📋 Review Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: #4caf50;">✅ AI Analysis</h4>
            <p style="color: #666;">Completed</p>
            <p style="color: #4caf50;"><strong>Score:</strong> 95/100</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: #ff9800;">🔄 Document Review</h4>
            <p style="color: #666;">In Progress</p>
            <p style="color: #ff9800;"><strong>Status:</strong> Reviewing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: #9e9e9e;">⏳ Final Decision</h4>
            <p style="color: #666;">Pending</p>
            <p style="color: #9e9e9e;"><strong>Status:</strong> Waiting</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Campaign details being reviewed
    st.markdown("### 📄 Campaign Under Review")
    
    if campaign.get('basic_info'):
        basic_info = campaign['basic_info']
        details = campaign.get('details', {})
        funding = campaign.get('funding', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Campaign Title:** {basic_info.get('title', 'N/A')}  
            **Category:** {basic_info.get('category', 'N/A')}  
            **Location:** {basic_info.get('location', 'N/A')}  
            **Beneficiary:** {details.get('beneficiary_name', 'N/A')}  
            **Urgency:** {basic_info.get('urgency', 'N/A')}
            """)
        
        with col2:
            st.markdown(f"""
            **Target Amount:** ₹{funding.get('target_amount', 0):,}  
            **Minimum Amount:** ₹{funding.get('minimum_amount', 0):,}  
            **Duration:** {funding.get('campaign_duration', 0)} days  
            **Submitted:** {campaign.get('created_at', 'N/A')[:10]}  
            **Campaign ID:** {campaign.get('id', 'N/A')[:8]}...
            """)
    
    # Action buttons
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            workflow_manager.navigate_to('admin_review', 'back')
    
    with col2:
        if st.button("📧 Contact Support", use_container_width=True):
            st.info("Support contact: support@haven.com | +91-1234567890")
    
    with col3:
        # Simulate admin decision for demo
        if st.button("🎲 Simulate Review Result", use_container_width=True):
            # Random decision for demo (90% approval rate)
            decision = random.choice(['approved'] * 9 + ['rejected'])
            
            if decision == 'approved':
                st.session_state.current_campaign['status'] = 'approved'
                st.session_state.current_campaign['verification_status'] = 'verified'
                st.session_state.current_campaign['approved_at'] = datetime.now().isoformat()
                workflow_manager.navigate_to('admin_review', 'approved')
            else:
                st.session_state.current_campaign['status'] = 'rejected'
                st.session_state.current_campaign['rejection_reason'] = 'Insufficient documentation'
                workflow_manager.navigate_to('admin_review', 'rejected')

def render_funding_display_page(workflow_manager):
    """Render approved campaign now live for funding"""
    st.markdown("### 🎉 Campaign Approved & Live!")
    
    campaign = st.session_state.current_campaign
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #2e7d32;">✅ Campaign is Now Live!</h2>
        <p style="color: #388e3c; font-size: 1.2rem;">
            "{campaign.get('basic_info', {}).get('title', 'Your campaign')}" is now accepting donations
        </p>
        <p style="color: #4caf50;">
            <strong>Campaign URL:</strong> haven.com/campaign/{campaign.get('id', 'N/A')[:8]}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Campaign stats
    st.markdown("### 📊 Campaign Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Target Amount", f"₹{campaign.get('funding', {}).get('target_amount', 0):,}")
    
    with col2:
        st.metric("Raised So Far", "₹0", "₹0")
    
    with col3:
        st.metric("Donors", "0", "0")
    
    with col4:
        days_left = campaign.get('funding', {}).get('campaign_duration', 60)
        st.metric("Days Left", str(days_left), "0")
    
    # Share campaign
    st.markdown("### 📢 Share Your Campaign")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 Share on WhatsApp", use_container_width=True):
            st.success("WhatsApp share link copied!")
    
    with col2:
        if st.button("📘 Share on Facebook", use_container_width=True):
            st.success("Facebook share link copied!")
    
    with col3:
        if st.button("📧 Share via Email", use_container_width=True):
            st.success("Email template copied!")
    
    # Action buttons
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            workflow_manager.navigate_to('funding_display', 'back')
    
    with col2:
        if st.button("👀 View as Donor", use_container_width=True):
            st.session_state.selected_campaign = campaign
            workflow_manager.navigate_to('funding_display', 'view')
    
    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.info("Analytics dashboard coming soon!")

def render_discard_project_page(workflow_manager):
    """Render page for rejected campaigns"""
    st.markdown("### ❌ Campaign Not Approved")
    
    campaign = st.session_state.current_campaign
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); 
                padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #d32f2f;">❌ Campaign Rejected</h2>
        <p style="color: #c62828; font-size: 1.2rem;">
            Unfortunately, "{campaign.get('basic_info', {}).get('title', 'your campaign')}" could not be approved
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rejection reason
    st.markdown("### 📋 Reason for Rejection")
    
    rejection_reason = campaign.get('rejection_reason', 'Insufficient documentation provided')
    
    st.error(f"**Reason:** {rejection_reason}")
    
    # What you can do
    st.markdown("### 🔧 What You Can Do")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h4 style="color: #2e7d32;">📝 Resubmit Campaign</h4>
            <p style="color: #666;">Address the issues mentioned and resubmit your campaign with additional documentation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h4 style="color: #2e7d32;">📞 Contact Support</h4>
            <p style="color: #666;">Get in touch with our support team for guidance on improving your campaign.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            workflow_manager.navigate_to('discard_project', 'back')
    
    with col2:
        if st.button("📝 Create New Campaign", use_container_width=True):
            # Clear current campaign and start fresh
            st.session_state.current_campaign = {}
            workflow_manager.navigate_to('authenticated', 'create')
    
    with col3:
        if st.button("📞 Contact Support", use_container_width=True):
            st.info("Support: support@haven.com | +91-1234567890")

def render_browse_campaigns_page(workflow_manager):
    """Render campaign browsing page"""
    st.markdown("### 🔍 Browse Campaigns")
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search campaigns", placeholder="Search by title, category, or location")
    
    with col2:
        category_filter = st.selectbox(
            "Category",
            options=["All", "Medical", "Education", "Disaster Relief", "Community Development", 
                    "Environment", "Animal Welfare", "Technology", "Social Causes", "Arts & Culture", "Sports"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            options=["Recent", "Most Funded", "Ending Soon", "Target Amount"]
        )
    
    # Sample campaigns (in real app, would fetch from backend)
    sample_campaigns = [
        {
            'id': 'camp_001',
            'title': 'Help Ravi Fight Cancer',
            'category': 'Medical',
            'location': 'Mumbai, Maharashtra',
            'target_amount': 500000,
            'raised_amount': 125000,
            'donors': 45,
            'days_left': 25,
            'verification_status': 'verified',
            'urgency': 'High',
            'image': '🏥'
        },
        {
            'id': 'camp_002',
            'title': 'Education for Underprivileged Children',
            'category': 'Education',
            'location': 'Delhi, India',
            'target_amount': 200000,
            'raised_amount': 180000,
            'donors': 120,
            'days_left': 5,
            'verification_status': 'verified',
            'urgency': 'Medium',
            'image': '📚'
        },
        {
            'id': 'camp_003',
            'title': 'Flood Relief for Kerala Families',
            'category': 'Disaster Relief',
            'location': 'Kerala, India',
            'target_amount': 1000000,
            'raised_amount': 750000,
            'donors': 300,
            'days_left': 15,
            'verification_status': 'verified',
            'urgency': 'Critical',
            'image': '🌊'
        },
        {
            'id': 'camp_004',
            'title': 'Save Street Dogs Shelter',
            'category': 'Animal Welfare',
            'location': 'Bangalore, Karnataka',
            'target_amount': 150000,
            'raised_amount': 45000,
            'donors': 25,
            'days_left': 40,
            'verification_status': 'under_review',
            'urgency': 'Medium',
            'image': '🐕'
        }
    ]
    
    # Filter campaigns based on search and category
    filtered_campaigns = sample_campaigns
    if category_filter != "All":
        filtered_campaigns = [c for c in filtered_campaigns if c['category'] == category_filter]
    if search_query:
        filtered_campaigns = [c for c in filtered_campaigns if search_query.lower() in c['title'].lower()]
    
    # Display campaigns
    st.markdown(f"### 📋 Found {len(filtered_campaigns)} campaigns")
    
    for campaign in filtered_campaigns:
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
            
            with col1:
                st.markdown(f"<div style='font-size: 4rem; text-align: center;'>{campaign['image']}</div>", 
                           unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{campaign['title']}**")
                st.markdown(f"📍 {campaign['location']} | 📂 {campaign['category']}")
                
                # Verification status
                if campaign['verification_status'] == 'verified':
                    st.markdown("✅ **Verified Campaign**")
                else:
                    st.markdown("⏳ **Under Review**")
                
                # Urgency
                urgency_colors = {'Low': '🟢', 'Medium': '🟡', 'High': '🟠', 'Critical': '🔴'}
                st.markdown(f"{urgency_colors.get(campaign['urgency'], '⚪')} {campaign['urgency']} Priority")
            
            with col3:
                # Progress bar
                progress = campaign['raised_amount'] / campaign['target_amount']
                st.progress(progress)
                
                st.markdown(f"**₹{campaign['raised_amount']:,}** raised of ₹{campaign['target_amount']:,}")
                st.markdown(f"👥 {campaign['donors']} donors | ⏰ {campaign['days_left']} days left")
            
            with col4:
                if st.button(f"👀 View", key=f"view_{campaign['id']}", use_container_width=True):
                    st.session_state.selected_campaign = campaign
                    workflow_manager.navigate_to('browse_campaigns', 'view')
        
        st.markdown("---")
    
    # Back button
    if st.button("⬅️ Back to Dashboard", use_container_width=True):
        workflow_manager.navigate_to('browse_campaigns', 'back')

def render_view_campaign_page(workflow_manager):
    """Render individual campaign view page"""
    campaign = st.session_state.selected_campaign
    
    st.markdown(f"### {campaign['image']} {campaign['title']}")
    
    # Campaign header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: #2e7d32;">{campaign['title']}</h3>
            <p><strong>📍 Location:</strong> {campaign['location']}</p>
            <p><strong>📂 Category:</strong> {campaign['category']}</p>
            <p><strong>⚡ Urgency:</strong> {campaign['urgency']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Funding progress
        progress = campaign['raised_amount'] / campaign['target_amount']
        st.progress(progress)
        
        st.metric("Raised", f"₹{campaign['raised_amount']:,}", f"₹{campaign['raised_amount']:,}")
        st.metric("Target", f"₹{campaign['target_amount']:,}")
        st.metric("Donors", campaign['donors'])
        st.metric("Days Left", campaign['days_left'])
    
    # Campaign description
    st.markdown("### 📖 Campaign Description")
    st.markdown("""
    This is a detailed description of the campaign. In a real application, this would contain 
    the full story, background information, current situation, and how the funds will be used.
    
    The campaign organizer has provided comprehensive details about the cause, including 
    medical reports (if applicable), verification documents, and a clear breakdown of fund usage.
    """)
    
    # Verification status
    st.markdown("### ✅ Verification Status")
    
    if campaign['verification_status'] == 'verified':
        st.success("✅ This campaign has been verified by our team")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("✅ **Documents Verified**")
        with col2:
            st.markdown("✅ **Identity Confirmed**")
        with col3:
            st.markdown("✅ **Contact Verified**")
        
        # Funding decision
        st.markdown("### 💝 Support This Campaign")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center;">
                <h4 style="color: #2e7d32;">💝 Want to help this cause?</h4>
                <p style="color: #388e3c;">Your contribution can make a real difference!</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("💝 Donate Now", key="donate_btn", use_container_width=True):
                st.session_state.funding_intent = True
                workflow_manager.navigate_to('view_campaign', 'fund_yes')
    
    else:
        st.warning("⏳ This campaign is currently under review")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center;">
            <h4 style="color: #f57c00;">⚠️ Project Under Review</h4>
            <p style="color: #ef6c00;">This campaign is being verified by our team. Donations will be enabled once verification is complete.</p>
        </div>
        """, unsafe_allow_html=True)
        
        workflow_manager.navigate_to('view_campaign', 'fund_no')
    
    # Action buttons
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Browse", use_container_width=True):
            workflow_manager.navigate_to('view_campaign', 'back')
    
    with col2:
        if st.button("📢 Share Campaign", use_container_width=True):
            st.success("Share link copied to clipboard!")
    
    with col3:
        if st.button("🚨 Report Issue", use_container_width=True):
            st.info("Report submitted. Thank you for helping keep our platform safe.")

def render_verification_check_page(workflow_manager):
    """Render verification check page before allowing donation"""
    campaign = st.session_state.selected_campaign
    
    st.markdown("### 🔍 Verification Check")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #1976d2;">🔍 Checking Campaign Status</h2>
        <p style="color: #1565c0; font-size: 1.2rem;">
            Verifying "{campaign['title']}" before proceeding with donation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verification checks
    st.markdown("### ✅ Verification Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: #4caf50;">✅ Campaign Active</h4>
            <p style="color: #666;">Campaign is currently active and accepting donations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: #4caf50;">✅ Verified Status</h4>
            <p style="color: #666;">All documents and details have been verified</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: #4caf50;">✅ Secure Payment</h4>
            <p style="color: #666;">Payment processing is secure and encrypted</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Proceed to donation
    st.markdown("---")
    
    if campaign['verification_status'] == 'verified':
        st.success("✅ All checks passed! You can safely proceed with your donation.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("⬅️ Back to Campaign", use_container_width=True):
                workflow_manager.navigate_to('verification_check', 'back')
        
        with col2:
            if st.button("💝 Proceed to Donate", use_container_width=True):
                workflow_manager.navigate_to('verification_check', 'verified')
    
    else:
        st.warning("⚠️ Campaign verification is still in progress")
        workflow_manager.navigate_to('verification_check', 'not_verified')

def render_show_warning_page(workflow_manager):
    """Render warning page for unverified campaigns"""
    campaign = st.session_state.selected_campaign
    
    st.markdown("### ⚠️ Campaign Under Review")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #f57c00;">⚠️ Project Under Review</h2>
        <p style="color: #ef6c00; font-size: 1.2rem;">
            "{campaign['title']}" is currently being verified by our team
        </p>
        <p style="color: #ff9800;">
            Donations will be enabled once verification is complete
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # What this means
    st.markdown("### 📋 What This Means")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h4 style="color: #2e7d32;">🔍 Under Verification</h4>
            <p style="color: #666;">Our team is currently reviewing the campaign documents and verifying the authenticity of the cause.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h4 style="color: #2e7d32;">⏰ Estimated Time</h4>
            <p style="color: #666;">Verification typically takes 24-48 hours. You'll be notified once the campaign is approved.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Browse", use_container_width=True):
            workflow_manager.navigate_to('show_warning', 'back')
    
    with col2:
        if st.button("🔔 Notify When Ready", use_container_width=True):
            st.success("You'll be notified when this campaign is verified!")
    
    with col3:
        if st.button("🔍 Browse Other Campaigns", use_container_width=True):
            workflow_manager.navigate_to('browse_campaigns', 'browse')

def render_make_contribution_page(workflow_manager):
    """Render donation/contribution page"""
    campaign = st.session_state.selected_campaign
    
    st.markdown(f"### 💝 Support: {campaign['title']}")
    
    # Campaign summary
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h4 style="color: #2e7d32;">{campaign['title']}</h4>
            <p><strong>📍</strong> {campaign['location']}</p>
            <p><strong>📂</strong> {campaign['category']}</p>
            <p><strong>🎯</strong> ₹{campaign['raised_amount']:,} raised of ₹{campaign['target_amount']:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        progress = campaign['raised_amount'] / campaign['target_amount']
        st.progress(progress)
        st.markdown(f"**{progress*100:.1f}%** funded")
    
    # Donation form
    st.markdown("### 💰 Choose Your Contribution")
    
    with st.form("donation_form"):
        # Quick amount buttons
        st.markdown("#### 🎯 Quick Amounts")
        
        col1, col2, col3, col4 = st.columns(4)
        
        quick_amounts = [500, 1000, 2500, 5000]
        selected_quick = None
        
        for i, amount in enumerate(quick_amounts):
            with [col1, col2, col3, col4][i]:
                if st.form_submit_button(f"₹{amount}", use_container_width=True):
                    selected_quick = amount
        
        # Custom amount
        st.markdown("#### 💵 Custom Amount")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            custom_amount = st.number_input(
                "Enter amount (₹)",
                min_value=100,
                max_value=100000,
                value=selected_quick if selected_quick else 1000,
                step=100
            )
        
        with col2:
            currency = st.selectbox("Currency", ["INR (₹)", "USD ($)"], index=0)
        
        # Donor information
        st.markdown("#### 👤 Donor Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            donor_name = st.text_input("Full Name *", placeholder="Your full name")
            donor_email = st.text_input("Email *", placeholder="your.email@example.com")
        
        with col2:
            donor_phone = st.text_input("Phone Number", placeholder="+91 9876543210")
            anonymous = st.checkbox("Donate anonymously")
        
        # Message to beneficiary
        message = st.text_area(
            "Message to Beneficiary (Optional)",
            placeholder="Write a message of support...",
            max_chars=200
        )
        
        # Terms and conditions
        terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
        
        # Submit donation
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.form_submit_button("⬅️ Back to Campaign", use_container_width=True):
                workflow_manager.navigate_to('make_contribution', 'back')
        
        with col3:
            if st.form_submit_button("💳 Proceed to Payment", use_container_width=True):
                if not all([donor_name, donor_email, custom_amount > 0, terms_accepted]):
                    st.error("Please fill in all required fields and accept terms")
                else:
                    # Store donation data
                    st.session_state.payment_data = {
                        'campaign_id': campaign['id'],
                        'amount': custom_amount,
                        'currency': currency,
                        'donor_name': donor_name,
                        'donor_email': donor_email,
                        'donor_phone': donor_phone,
                        'anonymous': anonymous,
                        'message': message
                    }
                    workflow_manager.navigate_to('make_contribution', 'proceed')

def render_payment_page(workflow_manager):
    """Render payment processing page"""
    payment_data = st.session_state.payment_data
    campaign = st.session_state.selected_campaign
    
    st.markdown("### 💳 Secure Payment")
    
    # Payment summary
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h3 style="color: #2e7d32;">💝 Donation Summary</h3>
        <p style="color: #388e3c;"><strong>Campaign:</strong> {campaign['title']}</p>
        <p style="color: #388e3c;"><strong>Amount:</strong> ₹{payment_data['amount']:,}</p>
        <p style="color: #388e3c;"><strong>Donor:</strong> {payment_data['donor_name']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Payment methods
    st.markdown("### 💳 Choose Payment Method")
    
    payment_method = st.radio(
        "Select payment method:",
        ["Credit/Debit Card", "UPI", "Net Banking", "Digital Wallet"],
        horizontal=True
    )
    
    # Payment form based on method
    if payment_method == "Credit/Debit Card":
        col1, col2 = st.columns(2)
        
        with col1:
            card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            cardholder_name = st.text_input("Cardholder Name", placeholder="Name on card")
        
        with col2:
            expiry = st.text_input("Expiry Date", placeholder="MM/YY")
            cvv = st.text_input("CVV", placeholder="123", type="password")
    
    elif payment_method == "UPI":
        upi_id = st.text_input("UPI ID", placeholder="yourname@upi")
        st.info("You will be redirected to your UPI app to complete the payment")
    
    elif payment_method == "Net Banking":
        bank = st.selectbox("Select Bank", [
            "State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", 
            "Punjab National Bank", "Bank of Baroda", "Other"
        ])
        st.info("You will be redirected to your bank's website")
    
    else:  # Digital Wallet
        wallet = st.selectbox("Select Wallet", [
            "Paytm", "PhonePe", "Google Pay", "Amazon Pay", "Mobikwik"
        ])
        st.info("You will be redirected to your wallet app")
    
    # Security notice
    st.markdown("### 🔒 Security Notice")
    st.info("🔒 Your payment is secured with 256-bit SSL encryption. We never store your payment details.")
    
    # Process payment
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Donation", use_container_width=True):
            workflow_manager.navigate_to('payment', 'back')
    
    with col3:
        if st.button("💳 Complete Payment", use_container_width=True):
            # Simulate payment processing
            with st.spinner("Processing payment..."):
                time.sleep(2)  # Simulate processing time
            
            # Simulate success (90% success rate)
            success = random.choice([True] * 9 + [False])
            
            if success:
                st.session_state.payment_data['transaction_id'] = f"TXN{int(time.time())}"
                st.session_state.payment_data['status'] = 'success'
                workflow_manager.navigate_to('payment', 'success')
            else:
                st.error("Payment failed. Please try again.")
                workflow_manager.navigate_to('payment', 'failed')

def render_success_page(workflow_manager):
    """Render payment success page"""
    payment_data = st.session_state.payment_data
    campaign = st.session_state.selected_campaign
    
    st.markdown("### 🎉 Donation Successful!")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                padding: 3rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #2e7d32;">🎉 Thank You!</h1>
        <h2 style="color: #388e3c;">Your donation was successful</h2>
        <p style="color: #4caf50; font-size: 1.3rem;">
            You've contributed <strong>₹{payment_data['amount']:,}</strong> to "{campaign['title']}"
        </p>
        <p style="color: #4caf50;">
            <strong>Transaction ID:</strong> {payment_data.get('transaction_id', 'N/A')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Impact message
    st.markdown("### 💝 Your Impact")
    
    st.success(f"""
    🌟 **Amazing!** Your contribution of ₹{payment_data['amount']:,} brings this campaign closer to its goal.
    
    📧 **Receipt:** A donation receipt has been sent to {payment_data['donor_email']}
    
    📱 **Updates:** You'll receive updates about how your donation is making a difference.
    """)
    
    # Next steps
    st.markdown("### 📋 What Happens Next?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: #2e7d32;">📧 Receipt</h4>
            <p style="color: #666;">Tax-deductible receipt sent to your email</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: #2e7d32;">📱 Updates</h4>
            <p style="color: #666;">Regular updates on campaign progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: #2e7d32;">🤝 Community</h4>
            <p style="color: #666;">Join our community of changemakers</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            workflow_manager.navigate_to('success', 'continue')
    
    with col2:
        if st.button("📢 Share Your Good Deed", use_container_width=True):
            st.success("Share link copied! Inspire others to donate too.")
    
    with col3:
        if st.button("🔍 Browse More Campaigns", use_container_width=True):
            workflow_manager.navigate_to('browse_campaigns', 'browse')

