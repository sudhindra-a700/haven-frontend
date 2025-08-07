"""
COMPATIBILITY UPDATED Workflow Campaign Pages for HAVEN Platform
Ensures compatibility with the fully integrated Streamlit app

This module provides campaign management functionality that works seamlessly with:
1. fully_integrated_app.py
2. corrected_authentication_flow.py
3. Streamlit compatibility fixes
4. Term simplification features
"""

import streamlit as st
import logging
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import uuid

logger = logging.getLogger(__name__)

# Backend configuration
BACKEND_URL = st.secrets.get('BACKEND_URL', 'https://haven-backend-9lw3.onrender.com')

def safe_rerun():
    """Safe rerun function that works with both old and new Streamlit versions"""
    try:
        if hasattr(st, 'rerun'):
            st.rerun()
        elif hasattr(st, 'experimental_rerun'):
            st.experimental_rerun()
        else:
            st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in safe_rerun: {e}")

def apply_term_simplification(text: str) -> str:
    """Apply term simplification with 'i' icons if enabled"""
    
    if not st.session_state.get('simplification_active', False):
        return text
    
    # Campaign-specific simplifications
    simplifications = {
        'campaign': {
            'simplified': 'fundraising project',
            'explanation': 'A specific project or cause that is asking for money donations'
        },
        'fundraising': {
            'simplified': 'collecting money',
            'explanation': 'The process of collecting money from people to support a cause or project'
        },
        'donation': {
            'simplified': 'money gift',
            'explanation': 'Money given freely to support a cause without expecting anything back'
        },
        'goal': {
            'simplified': 'target amount',
            'explanation': 'The total amount of money the campaign hopes to raise'
        },
        'milestone': {
            'simplified': 'progress point',
            'explanation': 'Important points reached during the fundraising process'
        }
    }
    
    result_text = text
    for original, data in simplifications.items():
        if original.lower() in text.lower():
            simplified = data['simplified']
            explanation = data['explanation']
            
            # Create HTML with 'i' icon and hover explanation
            replacement = f"""
            <span class="simplified-term">
                {simplified}
                <i class="material-icons info-icon">info</i>
                <div class="term-explanation">{explanation}</div>
            </span>
            """
            
            result_text = result_text.replace(original, replacement)
    
    return result_text

def render_create_campaign_page(session_state):
    """Render the create campaign page with multi-step form"""
    
    # Check authentication and role
    if not session_state.get('authenticated', False):
        st.error("❌ Authentication required")
        return
    
    if session_state.get('user_type') != 'organization':
        st.error("❌ Organization role required to create campaigns")
        return
    
    # Page header with term simplification
    title = "🚀 Create New Campaign"
    subtitle = "Launch your fundraising campaign and make a difference"
    
    if session_state.get('simplification_active', False):
        title = apply_term_simplification(title)
        subtitle = apply_term_simplification(subtitle)
    
    st.markdown(f"""
    <div class='main-header'>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize campaign creation state
    if 'campaign_creation_step' not in session_state:
        session_state.campaign_creation_step = 1
    
    if 'campaign_draft' not in session_state:
        session_state.campaign_draft = {}
    
    # Progress indicator
    show_campaign_progress(session_state.campaign_creation_step)
    
    # Show appropriate step
    if session_state.campaign_creation_step == 1:
        show_campaign_basic_info(session_state)
    elif session_state.campaign_creation_step == 2:
        show_campaign_details(session_state)
    elif session_state.campaign_creation_step == 3:
        show_campaign_media(session_state)
    elif session_state.campaign_creation_step == 4:
        show_campaign_funding(session_state)
    elif session_state.campaign_creation_step == 5:
        show_campaign_review(session_state)

def show_campaign_progress(current_step: int):
    """Show campaign creation progress"""
    
    steps = [
        "📝 Basic Info",
        "📄 Details", 
        "🖼️ Media",
        "💰 Funding",
        "✅ Review"
    ]
    
    # Progress bar
    progress = (current_step - 1) / (len(steps) - 1)
    st.progress(progress)
    
    # Step indicators
    cols = st.columns(len(steps))
    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            if i + 1 == current_step:
                st.markdown(f"**{step}** ✨")
            elif i + 1 < current_step:
                st.markdown(f"{step} ✅")
            else:
                st.markdown(f"{step}")

def show_campaign_basic_info(session_state):
    """Show basic campaign information form"""
    
    st.markdown("### 📝 Basic Campaign Information")
    
    with st.form("campaign_basic_info"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input(
                "Campaign Title *",
                value=session_state.campaign_draft.get('title', ''),
                placeholder="Enter a compelling campaign title",
                help="Choose a clear, engaging title that describes your cause"
            )
            
            category = st.selectbox(
                "Campaign Category *",
                ["Medical", "Education", "Environment", "Community", "Emergency", "Arts", "Sports", "Technology", "Other"],
                index=0 if not session_state.campaign_draft.get('category') else 
                      ["Medical", "Education", "Environment", "Community", "Emergency", "Arts", "Sports", "Technology", "Other"].index(session_state.campaign_draft.get('category', 'Medical'))
            )
            
            location = st.text_input(
                "Campaign Location *",
                value=session_state.campaign_draft.get('location', ''),
                placeholder="City, Country",
                help="Where is this campaign taking place?"
            )
        
        with col2:
            short_description = st.text_area(
                "Short Description *",
                value=session_state.campaign_draft.get('short_description', ''),
                placeholder="Brief summary of your campaign (max 200 characters)",
                max_chars=200,
                help="This will appear in campaign previews"
            )
            
            tags = st.text_input(
                "Tags",
                value=session_state.campaign_draft.get('tags', ''),
                placeholder="health, children, emergency (comma-separated)",
                help="Add relevant tags to help people find your campaign"
            )
        
        # Form submission
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            submitted = st.form_submit_button("Next: Campaign Details →", use_container_width=True, type="primary")
        
        with col3:
            if st.form_submit_button("Save Draft", use_container_width=True):
                save_campaign_draft(session_state, {
                    'title': title,
                    'category': category,
                    'location': location,
                    'short_description': short_description,
                    'tags': tags
                })
                st.success("✅ Draft saved!")
        
        if submitted:
            # Validate required fields
            if not all([title, category, location, short_description]):
                st.error("❌ Please fill in all required fields")
                return
            
            # Save to draft and proceed
            session_state.campaign_draft.update({
                'title': title,
                'category': category,
                'location': location,
                'short_description': short_description,
                'tags': tags
            })
            
            session_state.campaign_creation_step = 2
            safe_rerun()

def show_campaign_details(session_state):
    """Show detailed campaign information form"""
    
    st.markdown("### 📄 Campaign Details")
    
    with st.form("campaign_details"):
        # Full description
        full_description = st.text_area(
            "Full Campaign Description *",
            value=session_state.campaign_draft.get('full_description', ''),
            placeholder="Provide a detailed description of your campaign, including the problem you're solving, your solution, and how donations will be used.",
            height=200,
            help="Be specific about your goals and how funds will be used"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Problem statement
            problem_statement = st.text_area(
                "Problem Statement *",
                value=session_state.campaign_draft.get('problem_statement', ''),
                placeholder="What problem are you trying to solve?",
                height=100
            )
            
            # Target beneficiaries
            target_beneficiaries = st.text_input(
                "Target Beneficiaries *",
                value=session_state.campaign_draft.get('target_beneficiaries', ''),
                placeholder="Who will benefit from this campaign?",
                help="e.g., 100 children, local community, patients"
            )
        
        with col2:
            # Solution approach
            solution_approach = st.text_area(
                "Solution Approach *",
                value=session_state.campaign_draft.get('solution_approach', ''),
                placeholder="How will you solve this problem?",
                height=100
            )
            
            # Expected impact
            expected_impact = st.text_area(
                "Expected Impact",
                value=session_state.campaign_draft.get('expected_impact', ''),
                placeholder="What impact do you expect to achieve?",
                height=100
            )
        
        # Navigation buttons
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            if st.form_submit_button("← Previous", use_container_width=True):
                session_state.campaign_creation_step = 1
                safe_rerun()
        
        with col2:
            if st.form_submit_button("Save Draft", use_container_width=True):
                save_campaign_draft(session_state, {
                    'full_description': full_description,
                    'problem_statement': problem_statement,
                    'solution_approach': solution_approach,
                    'target_beneficiaries': target_beneficiaries,
                    'expected_impact': expected_impact
                })
                st.success("✅ Draft saved!")
        
        with col3:
            submitted = st.form_submit_button("Next: Media →", use_container_width=True, type="primary")
        
        if submitted:
            # Validate required fields
            if not all([full_description, problem_statement, solution_approach, target_beneficiaries]):
                st.error("❌ Please fill in all required fields")
                return
            
            # Save to draft and proceed
            session_state.campaign_draft.update({
                'full_description': full_description,
                'problem_statement': problem_statement,
                'solution_approach': solution_approach,
                'target_beneficiaries': target_beneficiaries,
                'expected_impact': expected_impact
            })
            
            session_state.campaign_creation_step = 3
            safe_rerun()

def show_campaign_media(session_state):
    """Show campaign media upload form"""
    
    st.markdown("### 🖼️ Campaign Media")
    
    st.markdown("""
    <div class='info-message'>
        <h4>📸 Media Guidelines</h4>
        <p>High-quality images and videos help tell your story and build trust with donors.</p>
        <ul>
            <li>Use clear, high-resolution images</li>
            <li>Show the people or cause you're helping</li>
            <li>Include progress photos if applicable</li>
            <li>Videos should be under 5 minutes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("campaign_media"):
        # Main campaign image
        st.markdown("#### 🖼️ Main Campaign Image *")
        main_image = st.file_uploader(
            "Upload main campaign image",
            type=['jpg', 'jpeg', 'png'],
            help="This will be the primary image for your campaign"
        )
        
        # Additional images
        st.markdown("#### 📸 Additional Images")
        additional_images = st.file_uploader(
            "Upload additional images",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            help="Upload up to 5 additional images"
        )
        
        # Campaign video
        st.markdown("#### 🎥 Campaign Video (Optional)")
        video_url = st.text_input(
            "Video URL",
            value=session_state.campaign_draft.get('video_url', ''),
            placeholder="https://youtube.com/watch?v=...",
            help="YouTube, Vimeo, or other video platform URL"
        )
        
        # Documents
        st.markdown("#### 📄 Supporting Documents (Optional)")
        documents = st.file_uploader(
            "Upload supporting documents",
            type=['pdf', 'doc', 'docx'],
            accept_multiple_files=True,
            help="Medical reports, certificates, project plans, etc."
        )
        
        # Navigation buttons
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            if st.form_submit_button("← Previous", use_container_width=True):
                session_state.campaign_creation_step = 2
                safe_rerun()
        
        with col2:
            if st.form_submit_button("Save Draft", use_container_width=True):
                save_campaign_draft(session_state, {
                    'video_url': video_url,
                    'main_image_uploaded': main_image is not None,
                    'additional_images_count': len(additional_images) if additional_images else 0,
                    'documents_count': len(documents) if documents else 0
                })
                st.success("✅ Draft saved!")
        
        with col3:
            submitted = st.form_submit_button("Next: Funding →", use_container_width=True, type="primary")
        
        if submitted:
            # Validate required fields
            if not main_image:
                st.error("❌ Please upload a main campaign image")
                return
            
            # Save media information to draft
            session_state.campaign_draft.update({
                'video_url': video_url,
                'main_image': main_image,
                'additional_images': additional_images,
                'documents': documents
            })
            
            session_state.campaign_creation_step = 4
            safe_rerun()

def show_campaign_funding(session_state):
    """Show campaign funding configuration form"""
    
    st.markdown("### 💰 Funding Configuration")
    
    with st.form("campaign_funding"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Funding goal
            funding_goal = st.number_input(
                "Funding Goal (USD) *",
                min_value=100,
                max_value=1000000,
                value=session_state.campaign_draft.get('funding_goal', 5000),
                step=100,
                help="How much money do you need to raise?"
            )
            
            # Campaign duration
            duration_days = st.number_input(
                "Campaign Duration (Days) *",
                min_value=7,
                max_value=365,
                value=session_state.campaign_draft.get('duration_days', 30),
                step=1,
                help="How long will your campaign run?"
            )
            
            # Minimum donation
            min_donation = st.number_input(
                "Minimum Donation (USD)",
                min_value=1,
                max_value=1000,
                value=session_state.campaign_draft.get('min_donation', 10),
                step=1,
                help="Minimum amount donors can contribute"
            )
        
        with col2:
            # Funding type
            funding_type = st.selectbox(
                "Funding Type *",
                ["All or Nothing", "Keep What You Raise"],
                index=0 if session_state.campaign_draft.get('funding_type') == "All or Nothing" else 1,
                help="All or Nothing: Only receive funds if goal is met. Keep What You Raise: Keep all donations regardless of goal."
            )
            
            # End date calculation
            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration_days)
            
            st.markdown(f"""
            **Campaign Timeline:**
            - **Start Date:** {start_date.strftime('%B %d, %Y')}
            - **End Date:** {end_date.strftime('%B %d, %Y')}
            - **Duration:** {duration_days} days
            """)
        
        # Milestones
        st.markdown("#### 🎯 Funding Milestones (Optional)")
        
        milestones = []
        for i in range(3):
            col1, col2 = st.columns(2)
            with col1:
                milestone_amount = st.number_input(
                    f"Milestone {i+1} Amount",
                    min_value=0,
                    max_value=funding_goal,
                    value=0,
                    key=f"milestone_amount_{i}"
                )
            with col2:
                milestone_description = st.text_input(
                    f"Milestone {i+1} Description",
                    placeholder="What will be achieved at this milestone?",
                    key=f"milestone_desc_{i}"
                )
            
            if milestone_amount > 0 and milestone_description:
                milestones.append({
                    'amount': milestone_amount,
                    'description': milestone_description
                })
        
        # Navigation buttons
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            if st.form_submit_button("← Previous", use_container_width=True):
                session_state.campaign_creation_step = 3
                safe_rerun()
        
        with col2:
            if st.form_submit_button("Save Draft", use_container_width=True):
                save_campaign_draft(session_state, {
                    'funding_goal': funding_goal,
                    'duration_days': duration_days,
                    'min_donation': min_donation,
                    'funding_type': funding_type,
                    'milestones': milestones
                })
                st.success("✅ Draft saved!")
        
        with col3:
            submitted = st.form_submit_button("Next: Review →", use_container_width=True, type="primary")
        
        if submitted:
            # Validate required fields
            if funding_goal < 100:
                st.error("❌ Funding goal must be at least $100")
                return
            
            # Save to draft and proceed
            session_state.campaign_draft.update({
                'funding_goal': funding_goal,
                'duration_days': duration_days,
                'min_donation': min_donation,
                'funding_type': funding_type,
                'milestones': milestones,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            })
            
            session_state.campaign_creation_step = 5
            safe_rerun()

def show_campaign_review(session_state):
    """Show campaign review and submission"""
    
    st.markdown("### ✅ Review Your Campaign")
    
    draft = session_state.campaign_draft
    
    # Campaign preview
    st.markdown("#### 📋 Campaign Summary")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        **Title:** {draft.get('title', 'N/A')}
        
        **Category:** {draft.get('category', 'N/A')}
        
        **Location:** {draft.get('location', 'N/A')}
        
        **Short Description:** {draft.get('short_description', 'N/A')}
        
        **Funding Goal:** ${draft.get('funding_goal', 0):,}
        
        **Duration:** {draft.get('duration_days', 0)} days
        
        **Funding Type:** {draft.get('funding_type', 'N/A')}
        """)
    
    with col2:
        st.markdown("**Media Uploaded:**")
        st.write(f"✅ Main Image: {'Yes' if draft.get('main_image') else 'No'}")
        st.write(f"📸 Additional Images: {len(draft.get('additional_images', []))}")
        st.write(f"🎥 Video: {'Yes' if draft.get('video_url') else 'No'}")
        st.write(f"📄 Documents: {len(draft.get('documents', []))}")
    
    # Terms and conditions
    st.markdown("#### 📜 Terms and Conditions")
    
    terms_accepted = st.checkbox(
        "I agree to the Terms of Service and Campaign Guidelines",
        help="You must agree to the terms to submit your campaign"
    )
    
    verification_consent = st.checkbox(
        "I consent to campaign verification process",
        help="Your campaign will be reviewed before going live"
    )
    
    # Submission buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("← Previous", use_container_width=True):
            session_state.campaign_creation_step = 4
            safe_rerun()
    
    with col2:
        if st.button("Save Draft", use_container_width=True):
            save_campaign_draft(session_state, draft)
            st.success("✅ Draft saved!")
    
    with col3:
        if st.button("Preview Campaign", use_container_width=True):
            show_campaign_preview(draft)
    
    with col4:
        if st.button("🚀 Submit Campaign", use_container_width=True, type="primary"):
            if not terms_accepted or not verification_consent:
                st.error("❌ Please accept the terms and consent to verification")
                return
            
            if handle_campaign_submission(session_state, draft):
                st.success("🎉 Campaign submitted successfully!")
                st.balloons()
                
                # Reset campaign creation state
                session_state.campaign_creation_step = 1
                session_state.campaign_draft = {}
                
                # Redirect to my campaigns
                session_state.current_page = 'my_campaigns'
                safe_rerun()

def save_campaign_draft(session_state, data: Dict[str, Any]):
    """Save campaign draft to session state"""
    session_state.campaign_draft.update(data)
    session_state.campaign_draft['last_saved'] = datetime.now().isoformat()

def show_campaign_preview(draft: Dict[str, Any]):
    """Show campaign preview"""
    
    with st.expander("📋 Campaign Preview", expanded=True):
        st.markdown(f"# {draft.get('title', 'Campaign Title')}")
        st.markdown(f"**Category:** {draft.get('category')} | **Location:** {draft.get('location')}")
        
        # Progress bar (mock)
        st.progress(0.0)
        st.markdown(f"**Goal:** ${draft.get('funding_goal', 0):,} | **Raised:** $0 | **Days Left:** {draft.get('duration_days', 0)}")
        
        st.markdown("### About This Campaign")
        st.write(draft.get('full_description', 'No description provided'))
        
        if draft.get('milestones'):
            st.markdown("### Milestones")
            for i, milestone in enumerate(draft.get('milestones', [])):
                st.write(f"🎯 ${milestone['amount']:,}: {milestone['description']}")

def handle_campaign_submission(session_state, draft: Dict[str, Any]) -> bool:
    """Handle campaign submission to backend"""
    
    try:
        user_data = session_state.get('user_data')
        if not user_data:
            st.error("❌ User data not found")
            return False
        
        # Prepare campaign data for submission
        campaign_data = {
            'title': draft.get('title'),
            'category': draft.get('category'),
            'location': draft.get('location'),
            'short_description': draft.get('short_description'),
            'full_description': draft.get('full_description'),
            'problem_statement': draft.get('problem_statement'),
            'solution_approach': draft.get('solution_approach'),
            'target_beneficiaries': draft.get('target_beneficiaries'),
            'expected_impact': draft.get('expected_impact'),
            'funding_goal': draft.get('funding_goal'),
            'duration_days': draft.get('duration_days'),
            'min_donation': draft.get('min_donation'),
            'funding_type': draft.get('funding_type'),
            'video_url': draft.get('video_url'),
            'tags': draft.get('tags'),
            'milestones': draft.get('milestones', []),
            'start_date': draft.get('start_date'),
            'end_date': draft.get('end_date'),
            'organization_id': user_data.get('id'),
            'organization_email': user_data.get('email'),
            'status': 'pending_review',
            'created_at': datetime.now().isoformat()
        }
        
        # Submit to backend
        response = requests.post(
            f"{BACKEND_URL}/api/v1/campaigns/create",
            json=campaign_data,
            timeout=15
        )
        
        if response.status_code == 201:
            logger.info(f"Campaign '{draft.get('title')}' submitted successfully")
            return True
        else:
            logger.error(f"Campaign submission failed: {response.status_code}")
            st.error(f"❌ Submission failed: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Exception during campaign submission: {e}")
        st.error(f"❌ Submission error: {str(e)}")
        return False

def render_campaign_management_page(session_state):
    """Render campaign management page for organizations"""
    
    st.markdown("### 📊 My Campaigns")
    
    # Check authentication and role
    if not session_state.get('authenticated', False):
        st.error("❌ Authentication required")
        return
    
    if session_state.get('user_type') != 'organization':
        st.error("❌ Organization role required")
        return
    
    # Show campaigns list
    show_my_campaigns_list(session_state)

def show_my_campaigns_list(session_state):
    """Show list of organization's campaigns"""
    
    # Mock campaign data (in real app, fetch from backend)
    campaigns = [
        {
            'id': '1',
            'title': 'Emergency Medical Fund',
            'status': 'active',
            'goal': 50000,
            'raised': 37500,
            'donors': 89,
            'days_left': 15,
            'created_at': '2024-01-15'
        },
        {
            'id': '2', 
            'title': 'School Renovation Project',
            'status': 'pending_review',
            'goal': 25000,
            'raised': 0,
            'donors': 0,
            'days_left': 30,
            'created_at': '2024-02-01'
        }
    ]
    
    # Campaign stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Campaigns", len(campaigns))
    
    with col2:
        active_campaigns = len([c for c in campaigns if c['status'] == 'active'])
        st.metric("Active Campaigns", active_campaigns)
    
    with col3:
        total_raised = sum(c['raised'] for c in campaigns)
        st.metric("Total Raised", f"${total_raised:,}")
    
    with col4:
        total_donors = sum(c['donors'] for c in campaigns)
        st.metric("Total Donors", total_donors)
    
    # Campaigns list
    st.markdown("#### 📋 Your Campaigns")
    
    for campaign in campaigns:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{campaign['title']}**")
                
                # Progress bar
                progress = campaign['raised'] / campaign['goal'] if campaign['goal'] > 0 else 0
                st.progress(progress)
                
                st.markdown(f"${campaign['raised']:,} raised of ${campaign['goal']:,} goal")
                st.markdown(f"👥 {campaign['donors']} donors • ⏰ {campaign['days_left']} days left")
            
            with col2:
                # Status badge
                status_color = {
                    'active': '🟢',
                    'pending_review': '🟡',
                    'completed': '✅',
                    'cancelled': '🔴'
                }
                st.markdown(f"{status_color.get(campaign['status'], '⚪')} {campaign['status'].replace('_', ' ').title()}")
            
            with col3:
                if st.button("View Details", key=f"view_{campaign['id']}", use_container_width=True):
                    session_state.selected_campaign = campaign['id']
                    session_state.current_page = 'campaign_details'
                    safe_rerun()
                
                if st.button("Edit", key=f"edit_{campaign['id']}", use_container_width=True):
                    st.info("🔧 Campaign editing coming soon!")
            
            st.markdown("---")

def handle_campaign_update(session_state, campaign_id: str, updates: Dict[str, Any]) -> bool:
    """Handle campaign update"""
    
    try:
        response = requests.put(
            f"{BACKEND_URL}/api/v1/campaigns/{campaign_id}",
            json=updates,
            timeout=15
        )
        
        if response.status_code == 200:
            logger.info(f"Campaign {campaign_id} updated successfully")
            return True
        else:
            logger.error(f"Campaign update failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Exception during campaign update: {e}")
        return False

# Export functions for main app integration
__all__ = [
    'render_create_campaign_page',
    'show_campaign_creation_form',
    'handle_campaign_submission',
    'show_campaign_progress',
    'render_campaign_management_page',
    'show_my_campaigns_list',
    'handle_campaign_update'
]

