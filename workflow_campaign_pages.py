"""
UPDATED Campaign Creation and Submission Workflow Pages for HAVEN
Integrates with fixed OAuth authentication system
Implements the exact workflow: Create → Submit → AI Processing → Admin Review
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import logging
import time
import uuid
from datetime import datetime, timedelta

# Import updated authentication utilities
from workflow_auth_utils import (
    get_auth_manager, 
    require_auth, 
    require_role, 
    get_current_user_role,
    is_authenticated
)

logger = logging.getLogger(__name__)

def render_create_campaign_page(workflow_manager):
    """UPDATED: Render campaign creation page - multi-step form with authentication"""
    
    # Require authentication and organization role
    if not require_auth():
        return
    
    if not require_role(['organization']):
        return
    
    st.markdown("### 🚀 Create Your Campaign")
    
    # Initialize campaign data if not exists
    if 'campaign_draft' not in st.session_state:
        st.session_state.campaign_draft = {
            'step': 1,
            'basic_info': {},
            'details': {},
            'media': {},
            'verification': {},
            'funding': {}
        }
    
    current_step = st.session_state.campaign_draft['step']
    
    # Progress indicator
    progress_steps = ["Basic Info", "Campaign Details", "Media & Documents", "Verification", "Funding Goals"]
    
    st.markdown("#### 📊 Campaign Creation Progress")
    progress_cols = st.columns(len(progress_steps))
    
    for i, step_name in enumerate(progress_steps, 1):
        with progress_cols[i-1]:
            if i < current_step:
                st.markdown(f"✅ **{step_name}**")
            elif i == current_step:
                st.markdown(f"🔄 **{step_name}**")
            else:
                st.markdown(f"⏳ {step_name}")
    
    st.markdown("---")
    
    # Render current step
    if current_step == 1:
        render_basic_info_step(workflow_manager)
    elif current_step == 2:
        render_campaign_details_step(workflow_manager)
    elif current_step == 3:
        render_media_documents_step(workflow_manager)
    elif current_step == 4:
        render_verification_step(workflow_manager)
    elif current_step == 5:
        render_funding_goals_step(workflow_manager)

def render_basic_info_step(workflow_manager):
    """UPDATED: Step 1: Basic campaign information with authentication checks"""
    
    st.markdown("#### 📝 Step 1: Basic Information")
    
    with st.form("basic_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input(
                "Campaign Title *",
                value=st.session_state.campaign_draft['basic_info'].get('title', ''),
                placeholder="Enter a compelling campaign title",
                help="Choose a clear, descriptive title that explains your cause"
            )
            
            category = st.selectbox(
                "Campaign Category *",
                options=[
                    "", "Medical", "Education", "Disaster Relief", "Community Development",
                    "Environment", "Animal Welfare", "Sports", "Arts & Culture", "Technology"
                ],
                index=0 if not st.session_state.campaign_draft['basic_info'].get('category') else 
                      ["", "Medical", "Education", "Disaster Relief", "Community Development",
                       "Environment", "Animal Welfare", "Sports", "Arts & Culture", "Technology"].index(
                          st.session_state.campaign_draft['basic_info'].get('category', '')
                      )
            )
            
            location = st.text_input(
                "Location *",
                value=st.session_state.campaign_draft['basic_info'].get('location', ''),
                placeholder="City, State, Country"
            )
        
        with col2:
            short_description = st.text_area(
                "Short Description *",
                value=st.session_state.campaign_draft['basic_info'].get('short_description', ''),
                placeholder="Brief summary of your campaign (max 200 characters)",
                max_chars=200,
                height=100
            )
            
            beneficiary_type = st.selectbox(
                "Beneficiary Type *",
                options=["", "Individual", "Community", "Organization", "Environment", "Animals"],
                index=0 if not st.session_state.campaign_draft['basic_info'].get('beneficiary_type') else
                      ["", "Individual", "Community", "Organization", "Environment", "Animals"].index(
                          st.session_state.campaign_draft['basic_info'].get('beneficiary_type', '')
                      )
            )
            
            urgency_level = st.selectbox(
                "Urgency Level *",
                options=["", "Low", "Medium", "High", "Critical"],
                index=0 if not st.session_state.campaign_draft['basic_info'].get('urgency_level') else
                      ["", "Low", "Medium", "High", "Critical"].index(
                          st.session_state.campaign_draft['basic_info'].get('urgency_level', '')
                      )
            )
        
        # Form submission
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            submitted = st.form_submit_button("Continue to Details →", use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            errors = []
            if not title.strip():
                errors.append("Campaign title is required")
            if not category:
                errors.append("Campaign category is required")
            if not location.strip():
                errors.append("Location is required")
            if not short_description.strip():
                errors.append("Short description is required")
            if not beneficiary_type:
                errors.append("Beneficiary type is required")
            if not urgency_level:
                errors.append("Urgency level is required")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Save data and proceed
                st.session_state.campaign_draft['basic_info'] = {
                    'title': title.strip(),
                    'category': category,
                    'location': location.strip(),
                    'short_description': short_description.strip(),
                    'beneficiary_type': beneficiary_type,
                    'urgency_level': urgency_level
                }
                st.session_state.campaign_draft['step'] = 2
                st.experimental_rerun()

def render_campaign_details_step(workflow_manager):
    """UPDATED: Step 2: Detailed campaign information with authentication checks"""
    
    st.markdown("#### 📖 Step 2: Campaign Details")
    
    with st.form("campaign_details_form"):
        # Full description
        full_description = st.text_area(
            "Full Campaign Description *",
            value=st.session_state.campaign_draft['details'].get('full_description', ''),
            placeholder="Provide a detailed description of your campaign, including background, goals, and impact...",
            height=200,
            help="Explain your cause in detail. Include background information, specific goals, and expected impact."
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Problem statement
            problem_statement = st.text_area(
                "Problem Statement *",
                value=st.session_state.campaign_draft['details'].get('problem_statement', ''),
                placeholder="Clearly describe the problem you're addressing...",
                height=120
            )
            
            # Target beneficiaries
            target_beneficiaries = st.text_input(
                "Target Beneficiaries *",
                value=st.session_state.campaign_draft['details'].get('target_beneficiaries', ''),
                placeholder="Who will benefit from this campaign?"
            )
        
        with col2:
            # Solution approach
            solution_approach = st.text_area(
                "Solution Approach *",
                value=st.session_state.campaign_draft['details'].get('solution_approach', ''),
                placeholder="How will you solve the problem?",
                height=120
            )
            
            # Expected impact
            expected_impact = st.text_input(
                "Expected Impact *",
                value=st.session_state.campaign_draft['details'].get('expected_impact', ''),
                placeholder="What impact do you expect to achieve?"
            )
        
        # Timeline
        st.markdown("**Campaign Timeline**")
        timeline_col1, timeline_col2 = st.columns(2)
        
        with timeline_col1:
            start_date = st.date_input(
                "Campaign Start Date *",
                value=st.session_state.campaign_draft['details'].get('start_date', datetime.now().date()),
                min_value=datetime.now().date()
            )
        
        with timeline_col2:
            end_date = st.date_input(
                "Campaign End Date *",
                value=st.session_state.campaign_draft['details'].get('end_date', 
                    (datetime.now() + timedelta(days=30)).date()),
                min_value=datetime.now().date()
            )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            back_clicked = st.form_submit_button("← Back to Basic Info", use_container_width=True)
        
        with col3:
            next_clicked = st.form_submit_button("Continue to Media →", use_container_width=True, type="primary")
        
        if back_clicked:
            st.session_state.campaign_draft['step'] = 1
            st.experimental_rerun()
        
        if next_clicked:
            # Validation
            errors = []
            if not full_description.strip():
                errors.append("Full description is required")
            if not problem_statement.strip():
                errors.append("Problem statement is required")
            if not solution_approach.strip():
                errors.append("Solution approach is required")
            if not target_beneficiaries.strip():
                errors.append("Target beneficiaries is required")
            if not expected_impact.strip():
                errors.append("Expected impact is required")
            if end_date <= start_date:
                errors.append("End date must be after start date")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Save data and proceed
                st.session_state.campaign_draft['details'] = {
                    'full_description': full_description.strip(),
                    'problem_statement': problem_statement.strip(),
                    'solution_approach': solution_approach.strip(),
                    'target_beneficiaries': target_beneficiaries.strip(),
                    'expected_impact': expected_impact.strip(),
                    'start_date': start_date,
                    'end_date': end_date
                }
                st.session_state.campaign_draft['step'] = 3
                st.experimental_rerun()

def render_media_documents_step(workflow_manager):
    """UPDATED: Step 3: Media and documents with authentication checks"""
    
    st.markdown("#### 📸 Step 3: Media & Documents")
    
    with st.form("media_documents_form"):
        st.info("📝 **Note**: Upload compelling images and documents that support your campaign story.")
        
        # Campaign image
        st.markdown("**Campaign Cover Image**")
        campaign_image = st.file_uploader(
            "Upload Campaign Cover Image *",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a high-quality image that represents your campaign (max 5MB)"
        )
        
        # Additional images
        st.markdown("**Additional Images**")
        additional_images = st.file_uploader(
            "Upload Additional Images (Optional)",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            help="Upload up to 5 additional images to support your campaign"
        )
        
        # Supporting documents
        st.markdown("**Supporting Documents**")
        supporting_docs = st.file_uploader(
            "Upload Supporting Documents (Optional)",
            type=['pdf', 'doc', 'docx'],
            accept_multiple_files=True,
            help="Upload relevant documents like medical reports, certificates, etc."
        )
        
        # Video link
        video_link = st.text_input(
            "Video Link (Optional)",
            value=st.session_state.campaign_draft['media'].get('video_link', ''),
            placeholder="YouTube, Vimeo, or other video platform link",
            help="Add a video to make your campaign more compelling"
        )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            back_clicked = st.form_submit_button("← Back to Details", use_container_width=True)
        
        with col3:
            next_clicked = st.form_submit_button("Continue to Verification →", use_container_width=True, type="primary")
        
        if back_clicked:
            st.session_state.campaign_draft['step'] = 2
            st.experimental_rerun()
        
        if next_clicked:
            # Validation
            errors = []
            if not campaign_image:
                errors.append("Campaign cover image is required")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Save data and proceed
                st.session_state.campaign_draft['media'] = {
                    'campaign_image': campaign_image,
                    'additional_images': additional_images,
                    'supporting_docs': supporting_docs,
                    'video_link': video_link.strip() if video_link else None
                }
                st.session_state.campaign_draft['step'] = 4
                st.experimental_rerun()

def render_verification_step(workflow_manager):
    """UPDATED: Step 4: Verification with authentication checks"""
    
    st.markdown("#### ✅ Step 4: Verification")
    
    with st.form("verification_form"):
        st.info("🔍 **Identity Verification**: Please provide information to verify your identity and campaign authenticity.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Organization details
            org_name = st.text_input(
                "Organization Name *",
                value=st.session_state.campaign_draft['verification'].get('org_name', ''),
                placeholder="Official organization name"
            )
            
            org_registration = st.text_input(
                "Registration Number *",
                value=st.session_state.campaign_draft['verification'].get('org_registration', ''),
                placeholder="Official registration/license number"
            )
            
            contact_person = st.text_input(
                "Contact Person *",
                value=st.session_state.campaign_draft['verification'].get('contact_person', ''),
                placeholder="Primary contact person name"
            )
        
        with col2:
            contact_phone = st.text_input(
                "Contact Phone *",
                value=st.session_state.campaign_draft['verification'].get('contact_phone', ''),
                placeholder="+1234567890"
            )
            
            contact_email = st.text_input(
                "Contact Email *",
                value=st.session_state.campaign_draft['verification'].get('contact_email', ''),
                placeholder="contact@organization.org"
            )
            
            website = st.text_input(
                "Website (Optional)",
                value=st.session_state.campaign_draft['verification'].get('website', ''),
                placeholder="https://www.organization.org"
            )
        
        # Verification documents
        st.markdown("**Verification Documents**")
        verification_docs = st.file_uploader(
            "Upload Verification Documents *",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            help="Upload organization registration, tax exemption, or other official documents"
        )
        
        # Terms and conditions
        terms_accepted = st.checkbox(
            "I agree to the Terms of Service and Privacy Policy *",
            value=st.session_state.campaign_draft['verification'].get('terms_accepted', False)
        )
        
        authenticity_confirmed = st.checkbox(
            "I confirm that all information provided is accurate and authentic *",
            value=st.session_state.campaign_draft['verification'].get('authenticity_confirmed', False)
        )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            back_clicked = st.form_submit_button("← Back to Media", use_container_width=True)
        
        with col3:
            next_clicked = st.form_submit_button("Continue to Funding →", use_container_width=True, type="primary")
        
        if back_clicked:
            st.session_state.campaign_draft['step'] = 3
            st.experimental_rerun()
        
        if next_clicked:
            # Validation
            errors = []
            if not org_name.strip():
                errors.append("Organization name is required")
            if not org_registration.strip():
                errors.append("Registration number is required")
            if not contact_person.strip():
                errors.append("Contact person is required")
            if not contact_phone.strip():
                errors.append("Contact phone is required")
            if not contact_email.strip():
                errors.append("Contact email is required")
            if not verification_docs:
                errors.append("Verification documents are required")
            if not terms_accepted:
                errors.append("You must accept the terms and conditions")
            if not authenticity_confirmed:
                errors.append("You must confirm the authenticity of information")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Save data and proceed
                st.session_state.campaign_draft['verification'] = {
                    'org_name': org_name.strip(),
                    'org_registration': org_registration.strip(),
                    'contact_person': contact_person.strip(),
                    'contact_phone': contact_phone.strip(),
                    'contact_email': contact_email.strip(),
                    'website': website.strip() if website else None,
                    'verification_docs': verification_docs,
                    'terms_accepted': terms_accepted,
                    'authenticity_confirmed': authenticity_confirmed
                }
                st.session_state.campaign_draft['step'] = 5
                st.experimental_rerun()

def render_funding_goals_step(workflow_manager):
    """UPDATED: Step 5: Funding goals with authentication checks"""
    
    st.markdown("#### 💰 Step 5: Funding Goals")
    
    with st.form("funding_goals_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Funding target
            funding_target = st.number_input(
                "Funding Target (USD) *",
                min_value=100,
                max_value=1000000,
                value=st.session_state.campaign_draft['funding'].get('funding_target', 1000),
                step=100,
                help="Set a realistic funding goal for your campaign"
            )
            
            # Minimum funding
            minimum_funding = st.number_input(
                "Minimum Funding Required (USD) *",
                min_value=50,
                max_value=funding_target,
                value=st.session_state.campaign_draft['funding'].get('minimum_funding', 
                    min(500, funding_target // 2)),
                step=50,
                help="Minimum amount needed to proceed with the campaign"
            )
        
        with col2:
            # Currency
            currency = st.selectbox(
                "Currency *",
                options=["USD", "EUR", "GBP", "INR", "CAD", "AUD"],
                index=0 if not st.session_state.campaign_draft['funding'].get('currency') else
                      ["USD", "EUR", "GBP", "INR", "CAD", "AUD"].index(
                          st.session_state.campaign_draft['funding'].get('currency', 'USD')
                      )
            )
            
            # Funding type
            funding_type = st.selectbox(
                "Funding Type *",
                options=["All or Nothing", "Keep What You Raise"],
                index=0 if not st.session_state.campaign_draft['funding'].get('funding_type') else
                      ["All or Nothing", "Keep What You Raise"].index(
                          st.session_state.campaign_draft['funding'].get('funding_type', 'All or Nothing')
                      ),
                help="All or Nothing: Get funds only if target is reached. Keep What You Raise: Keep all funds raised."
            )
        
        # Budget breakdown
        st.markdown("**Budget Breakdown**")
        budget_breakdown = st.text_area(
            "Detailed Budget Breakdown *",
            value=st.session_state.campaign_draft['funding'].get('budget_breakdown', ''),
            placeholder="Provide a detailed breakdown of how the funds will be used...",
            height=150,
            help="Explain how each dollar will be spent. Be transparent and specific."
        )
        
        # Use of funds
        use_of_funds = st.text_area(
            "Use of Funds *",
            value=st.session_state.campaign_draft['funding'].get('use_of_funds', ''),
            placeholder="Describe how the funds will be used to achieve your campaign goals...",
            height=100
        )
        
        # Navigation and submission buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            back_clicked = st.form_submit_button("← Back to Verification", use_container_width=True)
        
        with col3:
            submit_clicked = st.form_submit_button("🚀 Submit Campaign", use_container_width=True, type="primary")
        
        if back_clicked:
            st.session_state.campaign_draft['step'] = 4
            st.experimental_rerun()
        
        if submit_clicked:
            # Validation
            errors = []
            if funding_target < 100:
                errors.append("Funding target must be at least $100")
            if minimum_funding >= funding_target:
                errors.append("Minimum funding must be less than funding target")
            if not budget_breakdown.strip():
                errors.append("Budget breakdown is required")
            if not use_of_funds.strip():
                errors.append("Use of funds description is required")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Save data and submit campaign
                st.session_state.campaign_draft['funding'] = {
                    'funding_target': funding_target,
                    'minimum_funding': minimum_funding,
                    'currency': currency,
                    'funding_type': funding_type,
                    'budget_breakdown': budget_breakdown.strip(),
                    'use_of_funds': use_of_funds.strip()
                }
                
                # Submit campaign
                submit_campaign(workflow_manager)

def submit_campaign(workflow_manager):
    """UPDATED: Submit campaign for review with authentication"""
    
    try:
        # Get authentication manager
        auth_manager = get_auth_manager()
        
        # Prepare campaign data
        campaign_data = {
            'id': str(uuid.uuid4()),
            'created_at': datetime.now().isoformat(),
            'user_role': get_current_user_role(),
            'status': 'pending_review',
            **st.session_state.campaign_draft
        }
        
        # Here you would normally submit to backend
        # For now, we'll simulate successful submission
        
        # Clear draft and show success
        del st.session_state.campaign_draft
        
        st.success("🎉 **Campaign Submitted Successfully!**")
        st.info("""
        **What happens next?**
        
        1. **AI Processing** (2-4 hours): Our AI system will review your campaign for completeness and compliance
        2. **Admin Review** (24-48 hours): Our team will manually review your campaign
        3. **Approval & Launch**: Once approved, your campaign will go live on the platform
        
        You'll receive email notifications at each stage of the review process.
        """)
        
        if st.button("🏠 Return to Dashboard", use_container_width=True, type="primary"):
            st.experimental_rerun()
            
    except Exception as e:
        logger.error(f"Campaign submission error: {e}")
        st.error(f"❌ Failed to submit campaign: {str(e)}")

# Utility functions for campaign management
def get_user_campaigns(user_id: str) -> List[Dict[str, Any]]:
    """UPDATED: Get campaigns for authenticated user"""
    
    if not is_authenticated():
        return []
    
    # Here you would fetch from backend API
    # For now, return empty list
    return []

def get_campaign_status(campaign_id: str) -> Dict[str, Any]:
    """UPDATED: Get campaign status with authentication"""
    
    if not is_authenticated():
        return {'error': 'Authentication required'}
    
    # Here you would fetch from backend API
    # For now, return mock status
    return {
        'id': campaign_id,
        'status': 'pending_review',
        'created_at': datetime.now().isoformat(),
        'review_stage': 'ai_processing'
    }

