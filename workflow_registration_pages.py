"""
UPDATED Registration Workflow Pages for HAVEN Platform
Integrates with fixed OAuth authentication system
Handles individual and organization registration with role-based UI
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, Any, Optional
import re
import logging

# Import updated authentication utilities
from workflow_auth_utils import (
    get_auth_manager, 
    get_user_role,
    check_user_authentication
)

logger = logging.getLogger(__name__)

class RegistrationManager:
    """UPDATED: Manages registration workflows for individuals and organizations with OAuth integration"""
    
    def __init__(self):
        self.organization_types = [
            "ngo", "organization", "government"
        ]
        self.id_types = [
            "aadhaar", "pan", "passport", "driving_license", "voter_id"
        ]
        self.countries = [
            "India", "United States", "United Kingdom", "Canada", "Australia"
        ]
        
        # Get authentication manager
        self.auth_manager = get_auth_manager()
    
    def show_registration_selection(self):
        """UPDATED: Show registration type selection page with OAuth integration"""
        
        # Check if user is already authenticated via OAuth
        if check_user_authentication():
            user_role = get_user_role()
            st.success(f"✅ You are already logged in as {user_role}")
            
            # Check if additional registration is needed
            registration_status = self.auth_manager.get_registration_status()
            
            if registration_status.get('is_registered', False):
                st.info("🎉 Your registration is complete!")
                return
            else:
                st.info("📝 Please complete your profile registration below.")
                if user_role == 'individual':
                    self.show_individual_registration()
                elif user_role == 'organization':
                    self.show_organization_registration()
                return
        
        # Show OAuth login options if not authenticated
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center; margin: 0;'>🏠 Choose Your Registration Type</h1>
            <p style='color: white; text-align: center; margin: 0;'>Join the Haven community and start making a difference</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; 
                        border-left: 4px solid #4CAF50; margin: 1rem 0;'>
                <h4>👤 Individual</h4>
                <ul>
                    <li>🎯 Donate to campaigns</li>
                    <li>❤️ Support causes you care about</li>
                    <li>📊 Track donation history</li>
                    <li>🧾 Get tax receipts</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Register as Individual", key="individual_reg", use_container_width=True, type="primary"):
                st.session_state.selected_registration_type = "individual"
                st.experimental_rerun()
        
        with col2:
            st.markdown("""
            <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; 
                        border-left: 4px solid #4CAF50; margin: 1rem 0;'>
                <h4>🏢 Organization</h4>
                <ul>
                    <li>🚀 Create fundraising campaigns</li>
                    <li>📈 Manage campaign updates</li>
                    <li>💰 Track donations received</li>
                    <li>🤝 Engage with donors</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Register as Organization", key="organization_reg", use_container_width=True, type="primary"):
                st.session_state.selected_registration_type = "organization"
                st.experimental_rerun()
        
        # Show OAuth login if registration type is selected
        if st.session_state.get("selected_registration_type"):
            self.show_oauth_login_section()
    
    def show_oauth_login_section(self):
        """UPDATED: Show OAuth login section with fixed integration"""
        
        selected_type = st.session_state.selected_registration_type
        
        st.markdown("---")
        st.markdown(f"### 🔐 Login as {selected_type.title()}")
        
        # Import and use fixed OAuth integration
        from fixed_oauth_integration import render_oauth_buttons
        
        # Render OAuth buttons with selected user type
        render_oauth_buttons(selected_type)
        
        # Back button
        if st.button("⬅️ Back to Registration Type Selection", key="back_to_selection"):
            if "selected_registration_type" in st.session_state:
                del st.session_state.selected_registration_type
            st.experimental_rerun()
    
    def show_individual_registration(self):
        """UPDATED: Show individual registration form with OAuth integration"""
        
        st.markdown("### 👤 Individual Registration")
        st.markdown("Complete your profile to start supporting campaigns")
        
        with st.form("individual_registration_form"):
            # Personal Information
            st.markdown("#### 📝 Personal Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input(
                    "First Name *",
                    placeholder="Enter your first name"
                )
                
                last_name = st.text_input(
                    "Last Name *",
                    placeholder="Enter your last name"
                )
                
                email = st.text_input(
                    "Email Address *",
                    placeholder="your.email@example.com",
                    help="This will be your login email"
                )
            
            with col2:
                phone = st.text_input(
                    "Phone Number *",
                    placeholder="+1234567890"
                )
                
                date_of_birth = st.date_input(
                    "Date of Birth *",
                    min_value=date(1900, 1, 1),
                    max_value=date.today(),
                    value=date(1990, 1, 1)
                )
                
                gender = st.selectbox(
                    "Gender",
                    options=["", "Male", "Female", "Other", "Prefer not to say"],
                    index=0
                )
            
            # Address Information
            st.markdown("#### 🏠 Address Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                address_line1 = st.text_input(
                    "Address Line 1 *",
                    placeholder="Street address"
                )
                
                address_line2 = st.text_input(
                    "Address Line 2",
                    placeholder="Apartment, suite, etc. (optional)"
                )
                
                city = st.text_input(
                    "City *",
                    placeholder="City name"
                )
            
            with col2:
                state = st.text_input(
                    "State/Province *",
                    placeholder="State or province"
                )
                
                postal_code = st.text_input(
                    "Postal Code *",
                    placeholder="ZIP/Postal code"
                )
                
                country = st.selectbox(
                    "Country *",
                    options=[""] + self.countries,
                    index=0
                )
            
            # Identity Verification (Optional)
            st.markdown("#### 🆔 Identity Verification (Optional)")
            st.info("💡 Identity verification helps build trust and may be required for certain features.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                id_type = st.selectbox(
                    "ID Type",
                    options=[""] + [id_type.replace("_", " ").title() for id_type in self.id_types],
                    index=0
                )
                
                id_number = st.text_input(
                    "ID Number",
                    placeholder="Enter ID number"
                )
            
            with col2:
                id_document = st.file_uploader(
                    "Upload ID Document",
                    type=['jpg', 'jpeg', 'png', 'pdf'],
                    help="Upload a clear photo or scan of your ID"
                )
            
            # Preferences
            st.markdown("#### ⚙️ Preferences")
            
            col1, col2 = st.columns(2)
            
            with col1:
                newsletter_subscription = st.checkbox(
                    "Subscribe to newsletter",
                    value=True,
                    help="Receive updates about campaigns and platform news"
                )
                
                email_notifications = st.checkbox(
                    "Enable email notifications",
                    value=True,
                    help="Receive notifications about your donations and campaigns"
                )
            
            with col2:
                preferred_language = st.selectbox(
                    "Preferred Language",
                    options=["English", "Spanish", "French", "German", "Hindi"],
                    index=0
                )
                
                preferred_currency = st.selectbox(
                    "Preferred Currency",
                    options=["USD", "EUR", "GBP", "INR", "CAD", "AUD"],
                    index=0
                )
            
            # Terms and Conditions
            st.markdown("#### 📋 Terms and Conditions")
            
            terms_accepted = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy *",
                value=False
            )
            
            age_confirmation = st.checkbox(
                "I confirm that I am at least 18 years old *",
                value=False
            )
            
            # Submit button
            submitted = st.form_submit_button(
                "Complete Registration",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                # Validation
                errors = self._validate_individual_form(
                    first_name, last_name, email, phone, address_line1,
                    city, state, postal_code, country, terms_accepted, age_confirmation
                )
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Prepare registration data
                    registration_data = {
                        'user_type': 'individual',
                        'first_name': first_name.strip(),
                        'last_name': last_name.strip(),
                        'email': email.strip().lower(),
                        'phone': phone.strip(),
                        'date_of_birth': date_of_birth.isoformat(),
                        'gender': gender if gender else None,
                        'address': {
                            'line1': address_line1.strip(),
                            'line2': address_line2.strip() if address_line2 else None,
                            'city': city.strip(),
                            'state': state.strip(),
                            'postal_code': postal_code.strip(),
                            'country': country
                        },
                        'identity_verification': {
                            'id_type': id_type.lower().replace(" ", "_") if id_type else None,
                            'id_number': id_number.strip() if id_number else None,
                            'id_document': id_document
                        },
                        'preferences': {
                            'newsletter_subscription': newsletter_subscription,
                            'email_notifications': email_notifications,
                            'preferred_language': preferred_language,
                            'preferred_currency': preferred_currency
                        },
                        'terms_accepted': terms_accepted,
                        'age_confirmed': age_confirmation,
                        'registration_date': datetime.now().isoformat()
                    }
                    
                    # Submit registration
                    self._submit_registration(registration_data)
    
    def show_organization_registration(self):
        """UPDATED: Show organization registration form with OAuth integration"""
        
        st.markdown("### 🏢 Organization Registration")
        st.markdown("Register your organization to start creating campaigns")
        
        with st.form("organization_registration_form"):
            # Organization Information
            st.markdown("#### 🏢 Organization Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                org_name = st.text_input(
                    "Organization Name *",
                    placeholder="Official organization name"
                )
                
                org_type = st.selectbox(
                    "Organization Type *",
                    options=[""] + [org_type.upper() for org_type in self.organization_types],
                    index=0
                )
                
                registration_number = st.text_input(
                    "Registration Number *",
                    placeholder="Official registration number"
                )
                
                tax_id = st.text_input(
                    "Tax ID/EIN",
                    placeholder="Tax identification number"
                )
            
            with col2:
                website = st.text_input(
                    "Website",
                    placeholder="https://www.organization.org"
                )
                
                founded_year = st.number_input(
                    "Founded Year *",
                    min_value=1800,
                    max_value=datetime.now().year,
                    value=2000
                )
                
                employee_count = st.selectbox(
                    "Employee Count",
                    options=["", "1-10", "11-50", "51-200", "201-500", "500+"],
                    index=0
                )
                
                annual_budget = st.selectbox(
                    "Annual Budget (USD)",
                    options=["", "Under $10K", "$10K-$50K", "$50K-$250K", "$250K-$1M", "Over $1M"],
                    index=0
                )
            
            # Contact Information
            st.markdown("#### 📞 Primary Contact Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                contact_first_name = st.text_input(
                    "Contact First Name *",
                    placeholder="Primary contact first name"
                )
                
                contact_last_name = st.text_input(
                    "Contact Last Name *",
                    placeholder="Primary contact last name"
                )
                
                contact_title = st.text_input(
                    "Contact Title *",
                    placeholder="e.g., Executive Director, CEO"
                )
            
            with col2:
                contact_email = st.text_input(
                    "Contact Email *",
                    placeholder="contact@organization.org"
                )
                
                contact_phone = st.text_input(
                    "Contact Phone *",
                    placeholder="+1234567890"
                )
                
                alternate_phone = st.text_input(
                    "Alternate Phone",
                    placeholder="Secondary contact number"
                )
            
            # Address Information
            st.markdown("#### 🏠 Organization Address")
            
            col1, col2 = st.columns(2)
            
            with col1:
                address_line1 = st.text_input(
                    "Address Line 1 *",
                    placeholder="Street address"
                )
                
                address_line2 = st.text_input(
                    "Address Line 2",
                    placeholder="Suite, floor, etc. (optional)"
                )
                
                city = st.text_input(
                    "City *",
                    placeholder="City name"
                )
            
            with col2:
                state = st.text_input(
                    "State/Province *",
                    placeholder="State or province"
                )
                
                postal_code = st.text_input(
                    "Postal Code *",
                    placeholder="ZIP/Postal code"
                )
                
                country = st.selectbox(
                    "Country *",
                    options=[""] + self.countries,
                    index=0
                )
            
            # Mission and Description
            st.markdown("#### 🎯 Mission and Description")
            
            mission_statement = st.text_area(
                "Mission Statement *",
                placeholder="Describe your organization's mission and purpose...",
                height=100
            )
            
            description = st.text_area(
                "Organization Description *",
                placeholder="Provide a detailed description of your organization's work and impact...",
                height=150
            )
            
            focus_areas = st.multiselect(
                "Focus Areas *",
                options=[
                    "Education", "Healthcare", "Environment", "Poverty Alleviation",
                    "Human Rights", "Animal Welfare", "Disaster Relief", "Community Development",
                    "Arts & Culture", "Technology", "Research", "Other"
                ],
                help="Select all areas that apply to your organization's work"
            )
            
            # Verification Documents
            st.markdown("#### 📄 Verification Documents")
            st.info("📋 Please upload official documents to verify your organization's legitimacy.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                registration_document = st.file_uploader(
                    "Registration Certificate *",
                    type=['pdf', 'jpg', 'jpeg', 'png'],
                    help="Upload your organization's registration certificate"
                )
                
                tax_exemption_doc = st.file_uploader(
                    "Tax Exemption Certificate",
                    type=['pdf', 'jpg', 'jpeg', 'png'],
                    help="Upload tax exemption certificate if applicable"
                )
            
            with col2:
                financial_statement = st.file_uploader(
                    "Recent Financial Statement",
                    type=['pdf'],
                    help="Upload recent financial statement or annual report"
                )
                
                additional_docs = st.file_uploader(
                    "Additional Documents",
                    type=['pdf', 'jpg', 'jpeg', 'png'],
                    accept_multiple_files=True,
                    help="Upload any additional supporting documents"
                )
            
            # Banking Information (Optional)
            st.markdown("#### 🏦 Banking Information (Optional)")
            st.info("💡 Banking information can be added later for receiving donations.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                bank_name = st.text_input(
                    "Bank Name",
                    placeholder="Name of your bank"
                )
                
                account_name = st.text_input(
                    "Account Name",
                    placeholder="Account holder name"
                )
            
            with col2:
                account_number = st.text_input(
                    "Account Number",
                    placeholder="Bank account number",
                    type="password"
                )
                
                routing_number = st.text_input(
                    "Routing Number",
                    placeholder="Bank routing number"
                )
            
            # Terms and Conditions
            st.markdown("#### 📋 Terms and Conditions")
            
            terms_accepted = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy *",
                value=False
            )
            
            authority_confirmation = st.checkbox(
                "I confirm that I have the authority to register this organization *",
                value=False
            )
            
            accuracy_confirmation = st.checkbox(
                "I confirm that all information provided is accurate and up-to-date *",
                value=False
            )
            
            # Submit button
            submitted = st.form_submit_button(
                "Submit Organization Registration",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                # Validation
                errors = self._validate_organization_form(
                    org_name, org_type, registration_number, contact_first_name,
                    contact_last_name, contact_title, contact_email, contact_phone,
                    address_line1, city, state, postal_code, country,
                    mission_statement, description, focus_areas, registration_document,
                    terms_accepted, authority_confirmation, accuracy_confirmation
                )
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Prepare registration data
                    registration_data = {
                        'user_type': 'organization',
                        'organization': {
                            'name': org_name.strip(),
                            'type': org_type.lower(),
                            'registration_number': registration_number.strip(),
                            'tax_id': tax_id.strip() if tax_id else None,
                            'website': website.strip() if website else None,
                            'founded_year': founded_year,
                            'employee_count': employee_count if employee_count else None,
                            'annual_budget': annual_budget if annual_budget else None,
                            'mission_statement': mission_statement.strip(),
                            'description': description.strip(),
                            'focus_areas': focus_areas
                        },
                        'contact': {
                            'first_name': contact_first_name.strip(),
                            'last_name': contact_last_name.strip(),
                            'title': contact_title.strip(),
                            'email': contact_email.strip().lower(),
                            'phone': contact_phone.strip(),
                            'alternate_phone': alternate_phone.strip() if alternate_phone else None
                        },
                        'address': {
                            'line1': address_line1.strip(),
                            'line2': address_line2.strip() if address_line2 else None,
                            'city': city.strip(),
                            'state': state.strip(),
                            'postal_code': postal_code.strip(),
                            'country': country
                        },
                        'verification_documents': {
                            'registration_document': registration_document,
                            'tax_exemption_doc': tax_exemption_doc,
                            'financial_statement': financial_statement,
                            'additional_docs': additional_docs
                        },
                        'banking': {
                            'bank_name': bank_name.strip() if bank_name else None,
                            'account_name': account_name.strip() if account_name else None,
                            'account_number': account_number.strip() if account_number else None,
                            'routing_number': routing_number.strip() if routing_number else None
                        },
                        'terms_accepted': terms_accepted,
                        'authority_confirmed': authority_confirmation,
                        'accuracy_confirmed': accuracy_confirmation,
                        'registration_date': datetime.now().isoformat()
                    }
                    
                    # Submit registration
                    self._submit_registration(registration_data)
    
    def _validate_individual_form(self, first_name, last_name, email, phone, 
                                address_line1, city, state, postal_code, country,
                                terms_accepted, age_confirmation):
        """Validate individual registration form"""
        errors = []
        
        if not first_name.strip():
            errors.append("First name is required")
        if not last_name.strip():
            errors.append("Last name is required")
        if not email.strip():
            errors.append("Email address is required")
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append("Please enter a valid email address")
        if not phone.strip():
            errors.append("Phone number is required")
        if not address_line1.strip():
            errors.append("Address is required")
        if not city.strip():
            errors.append("City is required")
        if not state.strip():
            errors.append("State/Province is required")
        if not postal_code.strip():
            errors.append("Postal code is required")
        if not country:
            errors.append("Country is required")
        if not terms_accepted:
            errors.append("You must accept the terms and conditions")
        if not age_confirmation:
            errors.append("You must confirm that you are at least 18 years old")
        
        return errors
    
    def _validate_organization_form(self, org_name, org_type, registration_number,
                                  contact_first_name, contact_last_name, contact_title,
                                  contact_email, contact_phone, address_line1, city,
                                  state, postal_code, country, mission_statement,
                                  description, focus_areas, registration_document,
                                  terms_accepted, authority_confirmation, accuracy_confirmation):
        """Validate organization registration form"""
        errors = []
        
        if not org_name.strip():
            errors.append("Organization name is required")
        if not org_type:
            errors.append("Organization type is required")
        if not registration_number.strip():
            errors.append("Registration number is required")
        if not contact_first_name.strip():
            errors.append("Contact first name is required")
        if not contact_last_name.strip():
            errors.append("Contact last name is required")
        if not contact_title.strip():
            errors.append("Contact title is required")
        if not contact_email.strip():
            errors.append("Contact email is required")
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', contact_email):
            errors.append("Please enter a valid contact email address")
        if not contact_phone.strip():
            errors.append("Contact phone is required")
        if not address_line1.strip():
            errors.append("Address is required")
        if not city.strip():
            errors.append("City is required")
        if not state.strip():
            errors.append("State/Province is required")
        if not postal_code.strip():
            errors.append("Postal code is required")
        if not country:
            errors.append("Country is required")
        if not mission_statement.strip():
            errors.append("Mission statement is required")
        if not description.strip():
            errors.append("Organization description is required")
        if not focus_areas:
            errors.append("At least one focus area is required")
        if not registration_document:
            errors.append("Registration certificate is required")
        if not terms_accepted:
            errors.append("You must accept the terms and conditions")
        if not authority_confirmation:
            errors.append("You must confirm your authority to register this organization")
        if not accuracy_confirmation:
            errors.append("You must confirm the accuracy of the information")
        
        return errors
    
    def _submit_registration(self, registration_data):
        """UPDATED: Submit registration data with authentication"""
        
        try:
            # Submit registration using auth manager
            success, result = self.auth_manager.register_user(registration_data)
            
            if success:
                st.success("🎉 **Registration Submitted Successfully!**")
                st.info("""
                **What happens next?**
                
                1. **Email Verification**: Check your email for a verification link
                2. **Document Review** (Organizations): Our team will review your documents (24-48 hours)
                3. **Account Activation**: Your account will be activated once verification is complete
                
                You'll receive email notifications at each stage of the process.
                """)
                
                # Clear registration state
                if "selected_registration_type" in st.session_state:
                    del st.session_state.selected_registration_type
                
                if st.button("🏠 Return to Home", use_container_width=True, type="primary"):
                    st.experimental_rerun()
            else:
                st.error(f"❌ Registration failed: {result}")
                
        except Exception as e:
            logger.error(f"Registration submission error: {e}")
            st.error(f"❌ Registration failed: {str(e)}")

# Utility functions
def show_registration_page():
    """UPDATED: Main function to show registration page with OAuth integration"""
    
    registration_manager = RegistrationManager()
    registration_manager.show_registration_selection()
