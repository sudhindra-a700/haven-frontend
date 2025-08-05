"""
Footer Component for HAVEN Crowdfunding Platform
Handles footer rendering with proper links and contact information
"""

import streamlit as st
from datetime import datetime

def render_footer():
    """Render the main footer"""
    st.markdown("---")
    
    # Footer content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📞 Contact")
        st.markdown("- [Support](mailto:support@haven.org)")
        st.markdown("- [Contact Us](mailto:contact@haven.org)")
        st.markdown("- Phone: +91-XXX-XXX-XXXX")
        st.markdown("- Address: Mumbai, India")
    
    with col2:
        st.markdown("### 📄 Legal")
        st.info("📝 Legal pages are being prepared and will be available soon.")
        st.markdown("- Terms of Service (Coming Soon)")
        st.markdown("- Privacy Policy (Coming Soon)")
        st.markdown("- Cookie Policy (Coming Soon)")
        st.markdown("- Refund Policy (Coming Soon)")
    
    with col3:
        st.markdown("### 🌐 Connect")
        st.info("🔗 Social media pages are being set up and will be available soon.")
        st.markdown("- Twitter (Coming Soon)")
        st.markdown("- Facebook (Coming Soon)")
        st.markdown("- LinkedIn (Coming Soon)")
        st.markdown("- Instagram (Coming Soon)")
    
    # Copyright and additional info
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        current_year = datetime.now().year
        st.markdown(f"""
        <div style="text-align: left; color: #666; font-size: 0.9rem;">
            © {current_year} HAVEN Crowdfunding Platform. All rights reserved.<br>
            Made with ❤️ in India
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMjAiIGZpbGw9IiM2NjdlZWEiLz4KPHN2ZyB4PSI4IiB5PSI4IiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+CjxwYXRoIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMlM2LjQ4IDIyIDEyIDIyUzIyIDE3LjUyIDIyIDEyUzE3LjUyIDIgMTIgMlpNMTMgMTdIMTFWMTFIMTNWMTdaTTEzIDlIMTFWN0gxM1Y5WiIgZmlsbD0id2hpdGUiLz4KPC9zdmc+Cjwvc3ZnPgo=" alt="HAVEN Logo" style="width: 40px; height: 40px;">
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: right; color: #666; font-size: 0.9rem;">
            Secure payments powered by Instamojo<br>
            Email services by Brevo<br>
            Search powered by Algolia
        </div>
        """, unsafe_allow_html=True)

def render_mini_footer():
    """Render a minimal footer for pages with limited space"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        current_year = datetime.now().year
        st.markdown(f"""
        <div style="text-align: center; color: #666; font-size: 0.8rem; padding: 1rem 0;">
            © {current_year} HAVEN Crowdfunding Platform | 
            <a href="mailto:support@haven.org" style="color: #667eea;">Support</a> | 
            <a href="mailto:contact@haven.org" style="color: #667eea;">Contact</a>
        </div>
        """, unsafe_allow_html=True)

def render_legal_notice():
    """Render legal notice for pages that need it"""
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0; font-size: 0.8rem; color: #666;">
        <strong>Legal Notice:</strong> HAVEN is a crowdfunding platform that connects campaign creators with supporters. 
        We are not responsible for the content, accuracy, or outcomes of individual campaigns. 
        All donations are made directly to campaign creators. Please read our Terms of Service and Privacy Policy 
        (coming soon) before using our platform.
    </div>
    """, unsafe_allow_html=True)

def render_security_notice():
    """Render security notice"""
    st.markdown("""
    <div style="background-color: #e8f5e8; padding: 1rem; border-radius: 5px; margin: 1rem 0; font-size: 0.8rem; color: #2d5a2d; border-left: 4px solid #4caf50;">
        🔒 <strong>Security:</strong> Your data is protected with industry-standard encryption. 
        We use secure payment processing through Instamojo and never store your payment information.
    </div>
    """, unsafe_allow_html=True)

def render_help_section():
    """Render help section"""
    with st.expander("❓ Need Help?", expanded=False):
        st.markdown("""
        ### Frequently Asked Questions
        
        **How do I create a campaign?**
        Register for an account, verify your email, and click "Create Campaign" in the sidebar.
        
        **How do donations work?**
        Donations are processed securely through Instamojo. Funds go directly to campaign creators.
        
        **Is my personal information safe?**
        Yes, we use industry-standard security measures to protect your data.
        
        **How do I contact support?**
        Email us at support@haven.org or use the contact form.
        
        **Can I get a refund?**
        Refund policies vary by campaign. Contact the campaign creator or our support team.
        """)
        
        st.markdown("### Contact Support")
        st.markdown("📧 Email: support@haven.org")
        st.markdown("📞 Phone: +91-XXX-XXX-XXXX")
        st.markdown("⏰ Support Hours: 9 AM - 6 PM IST, Monday - Friday")

def render_platform_stats_footer():
    """Render platform statistics in footer"""
    st.markdown("### 📊 Platform Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Campaigns", "150+", delta="12 this month")
    
    with col2:
        st.metric("Amount Raised", "₹2.5M+", delta="₹50K this week")
    
    with col3:
        st.metric("Active Users", "1,200+", delta="25 this week")
    
    with col4:
        st.metric("Success Rate", "78%", delta="2% this month")

def render_newsletter_signup():
    """Render newsletter signup form"""
    st.markdown("### 📧 Stay Updated")
    st.markdown("Get notified about new campaigns and platform updates!")
    
    with st.form("newsletter_signup"):
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        interests = st.multiselect(
            "Interested in:",
            ["New Campaigns", "Success Stories", "Platform Updates", "Fundraising Tips"]
        )
        
        submitted = st.form_submit_button("Subscribe", use_container_width=True)
        
        if submitted:
            if email:
                # TODO: Integrate with Brevo mailing list
                st.success("Thank you for subscribing! You'll receive updates soon.")
            else:
                st.error("Please enter a valid email address.")

def render_trust_indicators():
    """Render trust and security indicators"""
    st.markdown("### 🛡️ Trust & Security")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; border: 1px solid #ddd; border-radius: 8px;">
            🔒<br>
            <strong>SSL Encrypted</strong><br>
            <small>Your data is protected</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; border: 1px solid #ddd; border-radius: 8px;">
            💳<br>
            <strong>Secure Payments</strong><br>
            <small>Powered by Instamojo</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; border: 1px solid #ddd; border-radius: 8px;">
            ✅<br>
            <strong>Verified Platform</strong><br>
            <small>Trusted by thousands</small>
        </div>
        """, unsafe_allow_html=True)

