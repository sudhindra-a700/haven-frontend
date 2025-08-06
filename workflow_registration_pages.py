"""
Registration Workflow Pages for HAVEN Platform
Handles individual and organization registration with role-based UI
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, Any, Optional
import re
from workflow_auth_utils import (
    register_individual, register_organization, 
    get_registration_status, is_authenticated
)

class RegistrationManager:
    """Manages registration workflows for individuals and organizations"""
    
    def __init__(self):
        self.organization_types = [
            "ngo", "organization", "government"
        ]
        self.id_types = [
            "aadhar", "pan", "passport", "driving_license", "voter_id"
        ]
        self.countries = [
            "India", "United States", "United Kingdom", "Canada", "Australia"
        ]
    
    def show_registration_selection(self):
        """Show registration type selection page"""
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center; margin: 0;'>
                🎯 Choose Your Registration Type
            </h1>
            <p style='color: white; text-align: center; margin-top: 1rem; font-size: 1.1rem;'>
                Select how you want to participate in HAVEN
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 10px; 
                        border: 2px solid #e0e0e0; height: 400px; display: flex; 
                        flex-direction: column; justify-content: space-between;'>
                <div>
                    <h3 style='color: #2196F3; text-align: center;'>👤 Individual</h3>
                    <p style='text-align: center; color: #666; margin-bottom: 1.5rem;'>
                        Register as an individual to donate to campaigns
                    </p>
                    <ul style='color: #333; padding-left: 1.5rem;'>
                        <li>✅ Donate to campaigns</li>
                        <li>✅ Track donation history</li>
                        <li>✅ Get tax receipts</li>
                        <li>✅ Support causes you care about</li>
                        <li>❌ Cannot create campaigns</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Register as Individual", key="register_individual", 
                       use_container_width=True, type="primary"):
                st.session_state.registration_type = "individual"
                st.rerun()
        
        with col2:
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 10px; 
                        border: 2px solid #e0e0e0; height: 400px; display: flex; 
                        flex-direction: column; justify-content: space-between;'>
                <div>
                    <h3 style='color: #4CAF50; text-align: center;'>🏢 Organization</h3>
                    <p style='text-align: center; color: #666; margin-bottom: 1.5rem;'>
                        Register as an organization to create campaigns
                    </p>
                    <ul style='color: #333; padding-left: 1.5rem;'>
                        <li>✅ Create fundraising campaigns</li>
                        <li>✅ Manage campaign updates</li>
                        <li>✅ Track donations received</li>
                        <li>✅ Engage with donors</li>
                        <li>❌ Cannot donate to campaigns</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Register as Organization", key="register_organization", 
                       use_container_width=True, type="secondary"):
                st.session_state.registration_type = "organization"
                st.rerun()
    
    def show_individual_registration(self):
        """Show individual registration form"""
        st.markdown("""
        <div style='background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center; margin: 0;'>
                👤 Individual Registration
            </h1>
            <p style='color: white; text-align: center; margin-top: 1rem;'>
                Join HAVEN as an individual donor
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("individual_registration_form"):
            st.subheader("📝 Personal Information")
            
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name *", placeholder="Enter your full name")
                email = st.text_input("Email Address *", placeholder="your.email@example.com")
                phone_number = st.text_input("Phone Number", placeholder="+91 9876543210")
            
            with col2:
                password = st.text_input("Password *", type="password", 
                                       placeholder="Create a secure password")
                confirm_password = st.text_input("Confirm Password *", type="password",
                                               placeholder="Confirm your password")
                date_of_birth = st.date_input("Date of Birth", 
                                            max_value=date.today(),
                                            value=date(1990, 1, 1))
            
            st.subheader("🏠 Address Information")
            
            col1, col2 = st.columns(2)
            with col1:
                address_line1 = st.text_input("Address Line 1", 
                                            placeholder="Street address")
                address_line2 = st.text_input("Address Line 2", 
                                            placeholder="Apartment, suite, etc.")
                city = st.text_input("City", placeholder="Your city")
            
            with col2:
                state = st.text_input("State", placeholder="Your state")
                postal_code = st.text_input("Postal Code", placeholder="PIN code")
                country = st.selectbox("Country", self.countries, index=0)
            
            st.subheader("🆔 Identity Verification (Optional)")
            
            col1, col2 = st.columns(2)
            with col1:
                id_type = st.selectbox("ID Type", [""] + self.id_types)
                id_number = st.text_input("ID Number", placeholder="Enter ID number")
            
            with col2:
                id_document_url = st.text_input("Document URL", 
                                              placeholder="Upload document URL (optional)")
            
            st.markdown("---")
            
            # Terms and conditions
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
            
            submitted = st.form_submit_button("🚀 Complete Registration", 
                                            use_container_width=True, type="primary")
            
            if submitted:
                # Validation
                errors = []
                
                if not full_name or len(full_name.strip()) < 2:
                    errors.append("Full name is required (minimum 2 characters)")
                
                if not email or not self._validate_email(email):
                    errors.append("Valid email address is required")
                
                if not password or len(password) < 8:
                    errors.append("Password must be at least 8 characters long")
                
                if password != confirm_password:
                    errors.append("Passwords do not match")
                
                if not terms_accepted:
                    errors.append("You must accept the Terms of Service and Privacy Policy")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Prepare registration data
                    registration_data = {
                        "full_name": full_name.strip(),
                        "email": email.lower().strip(),
                        "password": password,
                        "phone_number": phone_number.strip() if phone_number else None,
                        "date_of_birth": date_of_birth.isoformat() if date_of_birth else None,
                        "address_line1": address_line1.strip() if address_line1 else None,
                        "address_line2": address_line2.strip() if address_line2 else None,
                        "city": city.strip() if city else None,
                        "state": state.strip() if state else None,
                        "postal_code": postal_code.strip() if postal_code else None,
                        "country": country,
                        "id_type": id_type if id_type else None,
                        "id_number": id_number.strip() if id_number else None,
                        "id_document_url": id_document_url.strip() if id_document_url else None
                    }
                    
                    # Attempt registration
                    with st.spinner("Creating your account..."):
                        success, message = register_individual(registration_data)
                    
                    if success:
                        st.success("🎉 Registration successful! Welcome to HAVEN!")
                        st.balloons()
                        st.session_state.registration_type = None
                        st.rerun()
                    else:
                        st.error(f"Registration failed: {message}")
        
        # Back button
        if st.button("← Back to Registration Selection"):
            st.session_state.registration_type = None
            st.rerun()
    
    def show_organization_registration(self):
        """Show organization registration form"""
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center; margin: 0;'>
                🏢 Organization Registration
            </h1>
            <p style='color: white; text-align: center; margin-top: 1rem;'>
                Join HAVEN as an organization to create campaigns
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("organization_registration_form"):
            st.subheader("🏢 Organization Information")
            
            col1, col2 = st.columns(2)
            with col1:
                organization_name = st.text_input("Organization Name *", 
                                                placeholder="Your organization name")
                organization_type = st.selectbox("Organization Type *", 
                                               [""] + self.organization_types)
                email = st.text_input("Organization Email *", 
                                    placeholder="contact@organization.com")
                phone_number = st.text_input("Phone Number", 
                                           placeholder="+91 9876543210")
            
            with col2:
                website = st.text_input("Website", placeholder="https://www.organization.com")
                password = st.text_input("Password *", type="password",
                                       placeholder="Create a secure password")
                confirm_password = st.text_input("Confirm Password *", type="password",
                                               placeholder="Confirm your password")
            
            st.subheader("🏠 Organization Address")
            
            col1, col2 = st.columns(2)
            with col1:
                address_line1 = st.text_input("Address Line 1 *", 
                                            placeholder="Street address")
                address_line2 = st.text_input("Address Line 2", 
                                            placeholder="Suite, floor, etc.")
                city = st.text_input("City *", placeholder="Organization city")
            
            with col2:
                state = st.text_input("State *", placeholder="Organization state")
                postal_code = st.text_input("Postal Code *", placeholder="PIN code")
                country = st.selectbox("Country *", self.countries, index=0)
            
            st.subheader("📋 Legal Information")
            
            col1, col2 = st.columns(2)
            with col1:
                registration_number = st.text_input("Registration Number", 
                                                  placeholder="Legal registration number")
                tax_id = st.text_input("Tax ID", placeholder="Tax identification number")
                fcra_number = st.text_input("FCRA Number", 
                                          placeholder="For NGOs receiving foreign funds")
            
            with col2:
                ngo_garpan_id = st.text_input("NGO Darpan ID", 
                                            placeholder="NGO Darpan registration ID")
                registration_certificate_url = st.text_input("Registration Certificate URL",
                                                            placeholder="Upload certificate URL")
                tax_exemption_certificate_url = st.text_input("Tax Exemption Certificate URL",
                                                             placeholder="Upload certificate URL")
            
            st.subheader("👤 Contact Person")
            
            col1, col2 = st.columns(2)
            with col1:
                contact_person_name = st.text_input("Contact Person Name *",
                                                  placeholder="Primary contact person")
                contact_person_designation = st.text_input("Designation",
                                                         placeholder="Job title/position")
            
            with col2:
                contact_person_phone = st.text_input("Contact Person Phone",
                                                   placeholder="+91 9876543210")
                contact_person_email = st.text_input("Contact Person Email",
                                                    placeholder="contact.person@organization.com")
            
            st.markdown("---")
            
            # Terms and conditions
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
            verification_consent = st.checkbox("I consent to organization verification process *")
            
            submitted = st.form_submit_button("🚀 Complete Registration", 
                                            use_container_width=True, type="primary")
            
            if submitted:
                # Validation
                errors = []
                
                if not organization_name or len(organization_name.strip()) < 2:
                    errors.append("Organization name is required (minimum 2 characters)")
                
                if not organization_type:
                    errors.append("Organization type is required")
                
                if not email or not self._validate_email(email):
                    errors.append("Valid email address is required")
                
                if not password or len(password) < 8:
                    errors.append("Password must be at least 8 characters long")
                
                if password != confirm_password:
                    errors.append("Passwords do not match")
                
                if not address_line1 or not city or not state or not postal_code:
                    errors.append("Complete address is required")
                
                if not contact_person_name:
                    errors.append("Contact person name is required")
                
                if not terms_accepted:
                    errors.append("You must accept the Terms of Service and Privacy Policy")
                
                if not verification_consent:
                    errors.append("You must consent to the verification process")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Prepare registration data
                    registration_data = {
                        "organization_name": organization_name.strip(),
                        "organization_type": organization_type,
                        "email": email.lower().strip(),
                        "password": password,
                        "phone_number": phone_number.strip() if phone_number else None,
                        "website": website.strip() if website else None,
                        "address_line1": address_line1.strip(),
                        "address_line2": address_line2.strip() if address_line2 else None,
                        "city": city.strip(),
                        "state": state.strip(),
                        "postal_code": postal_code.strip(),
                        "country": country,
                        "registration_number": registration_number.strip() if registration_number else None,
                        "tax_id": tax_id.strip() if tax_id else None,
                        "fcra_number": fcra_number.strip() if fcra_number else None,
                        "ngo_garpan_id": ngo_garpan_id.strip() if ngo_garpan_id else None,
                        "registration_certificate_url": registration_certificate_url.strip() if registration_certificate_url else None,
                        "tax_exemption_certificate_url": tax_exemption_certificate_url.strip() if tax_exemption_certificate_url else None,
                        "fcra_certificate_url": None,  # Can be added later
                        "contact_person_name": contact_person_name.strip(),
                        "contact_person_designation": contact_person_designation.strip() if contact_person_designation else None,
                        "contact_person_phone": contact_person_phone.strip() if contact_person_phone else None,
                        "contact_person_email": contact_person_email.strip() if contact_person_email else None
                    }
                    
                    # Attempt registration
                    with st.spinner("Creating your organization account..."):
                        success, message = register_organization(registration_data)
                    
                    if success:
                        st.success("🎉 Organization registration successful! Welcome to HAVEN!")
                        st.info("📋 Your organization will be verified before you can create campaigns.")
                        st.balloons()
                        st.session_state.registration_type = None
                        st.rerun()
                    else:
                        st.error(f"Registration failed: {message}")
        
        # Back button
        if st.button("← Back to Registration Selection"):
            st.session_state.registration_type = None
            st.rerun()
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def show_registration_workflow(self):
        """Main registration workflow controller"""
        # Initialize session state
        if 'registration_type' not in st.session_state:
            st.session_state.registration_type = None
        
        # Check if user is already authenticated
        if is_authenticated():
            status = get_registration_status()
            if not status.get('needs_registration', False):
                st.success("✅ You are already registered and logged in!")
                return
        
        # Show appropriate registration page
        if st.session_state.registration_type == "individual":
            self.show_individual_registration()
        elif st.session_state.registration_type == "organization":
            self.show_organization_registration()
        else:
            self.show_registration_selection()

# Global registration manager instance
registration_manager = RegistrationManager()

# Utility functions
def show_registration_workflow():
    """Show registration workflow"""
    registration_manager.show_registration_workflow()

def show_registration_selection():
    """Show registration type selection"""
    registration_manager.show_registration_selection()

def show_individual_registration():
    """Show individual registration form"""
    registration_manager.show_individual_registration()

def show_organization_registration():
    """Show organization registration form"""
    registration_manager.show_organization_registration()

