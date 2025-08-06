"""
Footer component for HAVEN Crowdfunding Platform
Matches the repository structure of sudhindra-a700/haven-frontend
"""

import streamlit as st
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def show():
    """Display the footer component"""
    try:
        # Footer styling
        st.markdown("""
        <style>
        .footer {
            background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
            color: white;
            padding: 2rem 1rem;
            margin-top: 3rem;
            border-radius: 15px 15px 0 0;
            text-align: center;
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .footer-section {
            margin-bottom: 1.5rem;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 2rem;
            margin: 1rem 0;
        }
        
        .footer-link {
            color: #c8e6c9;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        
        .footer-link:hover {
            color: white;
            text-decoration: underline;
        }
        
        .social-icons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .social-icon {
            font-size: 1.5rem;
            color: #c8e6c9;
            transition: transform 0.3s ease, color 0.3s ease;
        }
        
        .social-icon:hover {
            transform: scale(1.2);
            color: white;
        }
        
        .footer-divider {
            border: none;
            height: 1px;
            background: rgba(255, 255, 255, 0.2);
            margin: 1.5rem 0;
        }
        
        .footer-bottom {
            font-size: 0.9rem;
            color: #c8e6c9;
        }
        
        .footer-logo {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Footer content
        current_year = datetime.now().year
        
        st.markdown(f"""
        <div class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <div class="footer-logo">🏠 HAVEN</div>
                    <p style="margin: 0.5rem 0; color: #c8e6c9;">
                        Empowering Communities Through Crowdfunding
                    </p>
                </div>
                
                <div class="footer-section">
                    <div class="footer-links">
                        <a href="#" class="footer-link">About Us</a>
                        <a href="#" class="footer-link">How It Works</a>
                        <a href="#" class="footer-link">Success Stories</a>
                        <a href="#" class="footer-link">Help Center</a>
                        <a href="#" class="footer-link">Contact</a>
                        <a href="#" class="footer-link">Blog</a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <div class="footer-links">
                        <a href="#" class="footer-link">Privacy Policy</a>
                        <a href="#" class="footer-link">Terms of Service</a>
                        <a href="#" class="footer-link">Cookie Policy</a>
                        <a href="#" class="footer-link">Trust & Safety</a>
                        <a href="#" class="footer-link">Fraud Prevention</a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <div class="social-icons">
                        <span class="social-icon" title="Facebook">📘</span>
                        <span class="social-icon" title="Twitter">🐦</span>
                        <span class="social-icon" title="Instagram">📷</span>
                        <span class="social-icon" title="LinkedIn">💼</span>
                        <span class="social-icon" title="YouTube">📺</span>
                        <span class="social-icon" title="WhatsApp">💬</span>
                    </div>
                </div>
                
                <hr class="footer-divider">
                
                <div class="footer-bottom">
                    <p style="margin: 0.5rem 0;">
                        © {current_year} HAVEN Crowdfunding Platform. All rights reserved.
                    </p>
                    <p style="margin: 0.5rem 0; font-size: 0.8rem;">
                        Built with ❤️ using Streamlit | Secured with 🔒 Advanced Fraud Detection
                    </p>
                    <p style="margin: 0.5rem 0; font-size: 0.8rem;">
                        🌍 Supporting communities across India | 🚀 Powered by AI & ML
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional footer information
        with st.expander("📊 Platform Statistics", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Total Raised", "₹12.5 Cr", "↗️ +15%")
            
            with col2:
                st.metric("🎯 Campaigns", "1,247", "↗️ +8%")
            
            with col3:
                st.metric("👥 Users", "45,678", "↗️ +12%")
            
            with col4:
                st.metric("🏆 Success Rate", "78%", "↗️ +3%")
        
        # Trust indicators
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0; padding: 1rem; background: rgba(76, 175, 80, 0.1); border-radius: 10px;">
            <h4 style="color: #2e7d32; margin-bottom: 1rem;">🛡️ Trust & Security</h4>
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 2rem;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">🔒</div>
                    <div style="font-size: 0.9rem; color: #666;">SSL Encrypted</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">🛡️</div>
                    <div style="font-size: 0.9rem; color: #666;">Fraud Protected</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">✅</div>
                    <div style="font-size: 0.9rem; color: #666;">Verified Campaigns</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">💳</div>
                    <div style="font-size: 0.9rem; color: #666;">Secure Payments</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">📞</div>
                    <div style="font-size: 0.9rem; color: #666;">24/7 Support</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Footer display error: {e}")
        # Minimal fallback footer
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: #666; padding: 1rem;">
            © {datetime.now().year} HAVEN Crowdfunding Platform | Built with ❤️ using Streamlit
        </div>
        """, unsafe_allow_html=True)

