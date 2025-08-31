# Modified workflow_verification_funding.py - Verification and Funding with Bootstrap Icons
# This file replaces your existing workflow_verification_funding.py

import streamlit as st
from utils.icon_utils import display_icon, get_icon_html, icon_button
from config.icon_mapping import get_icon, ICON_COLORS, ICON_SIZES

def render_identity_verification():
    """Render identity verification process with Bootstrap icons."""
    st.markdown(f"""
    <h1>{get_icon_html('shield-check', 32, ICON_COLORS['primary'])} Identity Verification</h1>
    <p style="color: {ICON_COLORS['muted']};">Verify your identity to ensure platform security</p>
    """, unsafe_allow_html=True)
    
    # Verification steps
    steps = [
        {"icon": "person-vcard", "title": "Personal Information", "status": "completed", "description": "Basic details verified"},
        {"icon": "camera", "title": "Photo ID Upload", "status": "current", "description": "Upload government-issued ID"},
        {"icon": "bank", "title": "Bank Account Verification", "status": "pending", "description": "Link your bank account"},
        {"icon": "check-circle", "title": "Review & Approval", "status": "pending", "description": "Final verification review"}
    ]
    
    for i, step in enumerate(steps):
        status_color = {
            "completed": ICON_COLORS['success'],
            "current": ICON_COLORS['primary'],
            "pending": ICON_COLORS['muted']
        }[step['status']]
        
        status_icon = {
            "completed": "check-circle-fill",
            "current": "arrow-right-circle-fill",
            "pending": "circle"
        }[step['status']]
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 15px; margin: 10px 0; 
                    background: white; border-radius: 10px; border-left: 4px solid {status_color};">
            <div style="margin-right: 15px;">
                {get_icon_html(step['icon'], 24, status_color)}
            </div>
            <div style="flex-grow: 1;">
                <h4 style="margin: 0; color: {status_color};">{step['title']}</h4>
                <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">{step['description']}</p>
            </div>
            <div>
                {get_icon_html(status_icon, 20, status_color)}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Current step: Photo ID Upload
    if st.session_state.get('verification_step', 'id_upload') == 'id_upload':
        render_id_upload_step()

def render_id_upload_step():
    """Render ID upload step."""
    st.markdown(f"""
    <h3>{get_icon_html('camera-fill', ICON_SIZES['lg'])} Upload Photo ID</h3>
    <p style="color: {ICON_COLORS['muted']};">Please upload a clear photo of your government-issued ID</p>
    """, unsafe_allow_html=True)
    
    # ID type selection
    id_type = st.selectbox(
        f"{get_icon_html('card-checklist', ICON_SIZES['sm'])} ID Type",
        ["Driver's License", "Passport", "National ID Card", "State ID"]
    )
    
    # File upload
    uploaded_file = st.file_uploader(
        f"{get_icon_html('cloud-upload', ICON_SIZES['sm'])} Choose ID document", 
        type=['png', 'jpg', 'jpeg', 'pdf'],
        help="Accepted formats: PNG, JPG, JPEG, PDF (max 10MB)"
    )
    
    if uploaded_file:
        st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} ID uploaded successfully!")
        
        # Preview uploaded file
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, caption="Uploaded ID Document", width=300)
        
        # Verification checklist
        st.markdown(f"""
        <h4>{get_icon_html('list-check', ICON_SIZES['md'])} Verification Checklist</h4>
        """, unsafe_allow_html=True)
        
        checklist_items = [
            "Document is clearly visible and not blurred",
            "All text is readable",
            "Document is not expired",
            "Photo matches your appearance",
            "No information is covered or obscured"
        ]
        
        for item in checklist_items:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin: 5px 0;">
                {get_icon_html('check-square', ICON_SIZES['sm'], ICON_COLORS['success'])}
                <span>{item}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button(f"{get_icon_html('send', ICON_SIZES['sm'])} Submit for Verification"):
            st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} ID submitted for verification! You'll receive an update within 24 hours.")
            st.session_state.verification_step = 'bank_verification'

def render_bank_verification():
    """Render bank account verification."""
    st.markdown(f"""
    <h1>{get_icon_html('bank', 32, ICON_COLORS['primary'])} Bank Account Verification</h1>
    <p style="color: {ICON_COLORS['muted']};">Link your bank account for secure transactions</p>
    """, unsafe_allow_html=True)
    
    # Bank connection methods
    st.markdown(f"""
    <h3>{get_icon_html('link-45deg', ICON_SIZES['lg'])} Connection Methods</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; text-align: center; margin: 10px 0;">
            {get_icon_html('lightning-charge-fill', 48, ICON_COLORS['primary'])}
            <h4>Instant Verification</h4>
            <p style="color: #666;">Connect securely through your online banking</p>
            <button style="background: #4CAF50; border: none; color: white; padding: 10px 20px; 
                           border-radius: 5px; cursor: pointer; width: 100%;">
                {get_icon_html('shield-check', 16)} Connect Bank
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; text-align: center; margin: 10px 0;">
            {get_icon_html('clock', 48, ICON_COLORS['warning'])}
            <h4>Manual Verification</h4>
            <p style="color: #666;">Verify with micro-deposits (1-2 business days)</p>
            <button style="background: #FF9800; border: none; color: white; padding: 10px 20px; 
                           border-radius: 5px; cursor: pointer; width: 100%;">
                {get_icon_html('pencil', 16)} Enter Details
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    # Manual bank details form
    if st.checkbox(f"{get_icon_html('pencil-square', ICON_SIZES['sm'])} Enter bank details manually"):
        render_manual_bank_form()

def render_manual_bank_form():
    """Render manual bank details form."""
    with st.form("bank_details_form"):
        st.markdown(f"""
        <h4>{get_icon_html('bank2', ICON_SIZES['md'])} Bank Account Details</h4>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            bank_name = st.text_input(f"{get_icon_html('building', ICON_SIZES['sm'])} Bank Name")
            account_number = st.text_input(f"{get_icon_html('hash', ICON_SIZES['sm'])} Account Number")
        with col2:
            routing_number = st.text_input(f"{get_icon_html('signpost', ICON_SIZES['sm'])} Routing Number")
            account_type = st.selectbox(f"{get_icon_html('list', ICON_SIZES['sm'])} Account Type", ["Checking", "Savings"])
        
        account_holder_name = st.text_input(f"{get_icon_html('person', ICON_SIZES['sm'])} Account Holder Name")
        
        # Security notice
        st.markdown(f"""
        <div style="background: #e3f2fd; border-left: 4px solid #2196F3; padding: 15px; margin: 15px 0;">
            {get_icon_html('shield-lock-fill', 20, '#2196F3')}
            <strong>Security Notice:</strong> Your banking information is encrypted and secure. 
            We use bank-level security to protect your data.
        </div>
        """, unsafe_allow_html=True)
        
        if st.form_submit_button(f"{get_icon_html('shield-check', ICON_SIZES['sm'])} Verify Account"):
            st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Bank account submitted for verification!")

def render_payment_methods():
    """Render payment methods management with Bootstrap icons."""
    st.markdown(f"""
    <h1>{get_icon_html('credit-card', 32, ICON_COLORS['primary'])} Payment Methods</h1>
    <p style="color: {ICON_COLORS['muted']};">Manage your payment and withdrawal methods</p>
    """, unsafe_allow_html=True)
    
    # Existing payment methods
    payment_methods = [
        {"type": "credit_card", "name": "Visa ending in 4242", "icon": "credit-card", "primary": True, "verified": True},
        {"type": "bank", "name": "Chase Bank Account", "icon": "bank", "primary": False, "verified": True},
        {"type": "paypal", "name": "PayPal Account", "icon": "paypal", "primary": False, "verified": False}
    ]
    
    st.markdown(f"""
    <h3>{get_icon_html('wallet2', ICON_SIZES['lg'])} Your Payment Methods</h3>
    """, unsafe_allow_html=True)
    
    for i, method in enumerate(payment_methods):
        primary_badge = f"""
        <span style="background: {ICON_COLORS['success']}; color: white; padding: 2px 8px; 
                     border-radius: 12px; font-size: 12px; margin-left: 10px;">
            {get_icon_html('star-fill', 12)} Primary
        </span>
        """ if method['primary'] else ""
        
        verified_badge = f"""
        <span style="background: {ICON_COLORS['info']}; color: white; padding: 2px 8px; 
                     border-radius: 12px; font-size: 12px; margin-left: 5px;">
            {get_icon_html('patch-check-fill', 12)} Verified
        </span>
        """ if method['verified'] else f"""
        <span style="background: {ICON_COLORS['warning']}; color: white; padding: 2px 8px; 
                     border-radius: 12px; font-size: 12px; margin-left: 5px;">
            {get_icon_html('clock', 12)} Pending
        </span>
        """
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; 
                    padding: 15px; margin: 10px 0; background: white; border-radius: 10px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center;">
                {get_icon_html(method['icon'], 24, ICON_COLORS['primary'])}
                <span style="margin-left: 15px; font-weight: 500;">{method['name']}</span>
                {primary_badge}
                {verified_badge}
            </div>
            <div>
                <button style="background: none; border: 1px solid {ICON_COLORS['muted']}; 
                               color: {ICON_COLORS['muted']}; padding: 5px 10px; border-radius: 5px; 
                               margin-right: 5px; cursor: pointer;">
                    {get_icon_html('pencil', 14)} Edit
                </button>
                <button style="background: none; border: 1px solid {ICON_COLORS['danger']}; 
                               color: {ICON_COLORS['danger']}; padding: 5px 10px; border-radius: 5px; 
                               cursor: pointer;">
                    {get_icon_html('trash', 14)} Remove
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add new payment method
    if st.button(f"{get_icon_html('plus-circle', ICON_SIZES['sm'])} Add Payment Method", key="add_payment"):
        render_add_payment_method_form()

def render_add_payment_method_form():
    """Render form to add new payment method."""
    st.markdown(f"""
    <h3>{get_icon_html('plus-circle-fill', ICON_SIZES['lg'])} Add New Payment Method</h3>
    """, unsafe_allow_html=True)
    
    # Payment method type selection
    payment_type = st.selectbox(
        f"{get_icon_html('list', ICON_SIZES['sm'])} Payment Method Type",
        ["Credit/Debit Card", "Bank Account", "PayPal", "Digital Wallet"]
    )
    
    if payment_type == "Credit/Debit Card":
        render_credit_card_form()
    elif payment_type == "Bank Account":
        render_bank_account_form()
    elif payment_type == "PayPal":
        render_paypal_form()
    elif payment_type == "Digital Wallet":
        render_digital_wallet_form()

def render_credit_card_form():
    """Render credit card form."""
    with st.form("credit_card_form"):
        st.markdown(f"""
        <h4>{get_icon_html('credit-card-fill', ICON_SIZES['md'])} Credit Card Information</h4>
        """, unsafe_allow_html=True)
        
        card_number = st.text_input(f"{get_icon_html('credit-card', ICON_SIZES['sm'])} Card Number", placeholder="1234 5678 9012 3456")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            expiry_month = st.selectbox("Month", [f"{i:02d}" for i in range(1, 13)])
        with col2:
            expiry_year = st.selectbox("Year", [str(2024 + i) for i in range(10)])
        with col3:
            cvv = st.text_input("CVV", placeholder="123", max_chars=4)
        
        cardholder_name = st.text_input(f"{get_icon_html('person', ICON_SIZES['sm'])} Cardholder Name")
        
        billing_address = st.text_area(f"{get_icon_html('house', ICON_SIZES['sm'])} Billing Address")
        
        if st.form_submit_button(f"{get_icon_html('plus-circle', ICON_SIZES['sm'])} Add Card"):
            st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Credit card added successfully!")

def render_bank_account_form():
    """Render bank account form."""
    with st.form("bank_account_form"):
        st.markdown(f"""
        <h4>{get_icon_html('bank2', ICON_SIZES['md'])} Bank Account Information</h4>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            bank_name = st.text_input(f"{get_icon_html('building', ICON_SIZES['sm'])} Bank Name")
            account_number = st.text_input(f"{get_icon_html('hash', ICON_SIZES['sm'])} Account Number")
        with col2:
            routing_number = st.text_input(f"{get_icon_html('signpost', ICON_SIZES['sm'])} Routing Number")
            account_type = st.selectbox(f"{get_icon_html('list', ICON_SIZES['sm'])} Account Type", ["Checking", "Savings"])
        
        if st.form_submit_button(f"{get_icon_html('plus-circle', ICON_SIZES['sm'])} Add Bank Account"):
            st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Bank account added successfully!")

def render_paypal_form():
    """Render PayPal form."""
    with st.form("paypal_form"):
        st.markdown(f"""
        <h4>{get_icon_html('paypal', ICON_SIZES['md'])} PayPal Account</h4>
        """, unsafe_allow_html=True)
        
        paypal_email = st.text_input(f"{get_icon_html('envelope', ICON_SIZES['sm'])} PayPal Email Address")
        
        st.markdown(f"""
        <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0;">
            {get_icon_html('info-circle', 20, '#856404')}
            <strong>Note:</strong> You'll be redirected to PayPal to authorize the connection.
        </div>
        """, unsafe_allow_html=True)
        
        if st.form_submit_button(f"{get_icon_html('paypal', ICON_SIZES['sm'])} Connect PayPal"):
            st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} PayPal connection initiated!")

def render_digital_wallet_form():
    """Render digital wallet form."""
    with st.form("digital_wallet_form"):
        st.markdown(f"""
        <h4>{get_icon_html('phone', ICON_SIZES['md'])} Digital Wallet</h4>
        """, unsafe_allow_html=True)
        
        wallet_type = st.selectbox(
            f"{get_icon_html('wallet2', ICON_SIZES['sm'])} Wallet Type",
            ["Apple Pay", "Google Pay", "Samsung Pay", "Other"]
        )
        
        phone_number = st.text_input(f"{get_icon_html('telephone', ICON_SIZES['sm'])} Phone Number")
        
        if st.form_submit_button(f"{get_icon_html('plus-circle', ICON_SIZES['sm'])} Add Digital Wallet"):
            st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Digital wallet added successfully!")

def render_funding_dashboard():
    """Render funding dashboard with transaction history."""
    st.markdown(f"""
    <h1>{get_icon_html('graph-up-arrow', 32, ICON_COLORS['primary'])} Funding Dashboard</h1>
    """, unsafe_allow_html=True)
    
    # Funding overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {get_icon_html('currency-dollar', 32, ICON_COLORS['success'])}
            <h2 style="margin: 10px 0; color: {ICON_COLORS['success']};">$2,450</h2>
            <p style="margin: 0; color: {ICON_COLORS['muted']};">Total Contributed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {get_icon_html('bookmark-star-fill', 32, ICON_COLORS['info'])}
            <h2 style="margin: 10px 0; color: {ICON_COLORS['info']};">12</h2>
            <p style="margin: 0; color: {ICON_COLORS['muted']};">Projects Backed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {get_icon_html('trophy-fill', 32, ICON_COLORS['warning'])}
            <h2 style="margin: 10px 0; color: {ICON_COLORS['warning']};">8</h2>
            <p style="margin: 0; color: {ICON_COLORS['muted']};">Successful Projects</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {get_icon_html('clock-history', 32, ICON_COLORS['primary'])}
            <h2 style="margin: 10px 0; color: {ICON_COLORS['primary']};">4</h2>
            <p style="margin: 0; color: {ICON_COLORS['muted']};">Active Campaigns</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Transaction history
    st.markdown(f"""
    <h3>{get_icon_html('list-ul', ICON_SIZES['lg'])} Recent Transactions</h3>
    """, unsafe_allow_html=True)
    
    transactions = [
        {"date": "2024-08-30", "type": "contribution", "project": "Smart Garden System", "amount": 150, "status": "completed"},
        {"date": "2024-08-28", "type": "contribution", "project": "Eco Water Bottles", "amount": 75, "status": "completed"},
        {"date": "2024-08-25", "type": "refund", "project": "Failed Project", "amount": 50, "status": "processed"},
        {"date": "2024-08-20", "type": "contribution", "project": "Educational Game", "amount": 25, "status": "completed"}
    ]
    
    for transaction in transactions:
        transaction_icon = {
            "contribution": "arrow-up-circle-fill",
            "refund": "arrow-down-circle-fill",
            "withdrawal": "cash-coin"
        }.get(transaction['type'], "circle")
        
        transaction_color = {
            "contribution": ICON_COLORS['success'],
            "refund": ICON_COLORS['warning'],
            "withdrawal": ICON_COLORS['info']
        }.get(transaction['type'], ICON_COLORS['muted'])
        
        status_color = ICON_COLORS['success'] if transaction['status'] == 'completed' else ICON_COLORS['warning']
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 15px; margin: 10px 0; background: white; border-radius: 8px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; gap: 15px;">
                {get_icon_html(transaction_icon, 24, transaction_color)}
                <div>
                    <h4 style="margin: 0;">{transaction['project']}</h4>
                    <p style="margin: 0; color: #666; font-size: 14px;">{transaction['date']}</p>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 500; color: {transaction_color};">
                    {'$' + str(transaction['amount'])}
                </div>
                <div style="font-size: 12px; color: {status_color};">
                    {get_icon_html('check-circle', 12, status_color)} {transaction['status']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Main verification and funding workflow function
def run_verification_funding_workflow():
    """Main function to run verification and funding workflow."""
    if 'verification_page' not in st.session_state:
        st.session_state.verification_page = 'identity'
    
    # Navigation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if icon_button('shield-check', 'Identity', 'nav_identity', ICON_SIZES['sm']):
            st.session_state.verification_page = 'identity'
    with col2:
        if icon_button('bank', 'Bank Verification', 'nav_bank', ICON_SIZES['sm']):
            st.session_state.verification_page = 'bank'
    with col3:
        if icon_button('credit-card', 'Payment Methods', 'nav_payment', ICON_SIZES['sm']):
            st.session_state.verification_page = 'payment'
    with col4:
        if icon_button('graph-up-arrow', 'Funding Dashboard', 'nav_funding', ICON_SIZES['sm']):
            st.session_state.verification_page = 'funding'
    
    # Render appropriate page
    if st.session_state.verification_page == 'identity':
        render_identity_verification()
    elif st.session_state.verification_page == 'bank':
        render_bank_verification()
    elif st.session_state.verification_page == 'payment':
        render_payment_methods()
    elif st.session_state.verification_page == 'funding':
        render_funding_dashboard()

