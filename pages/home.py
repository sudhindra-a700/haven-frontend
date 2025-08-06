"""
Fixed Home Page for HAVEN Crowdfunding Platform
Standardized with show() function and improved UI
"""

import streamlit as st
from typing import Dict, Any
import logging

# Import utilities with error handling
try:
    from utils.translation_service import t, format_currency
    from utils.api_client import get_campaigns, get_platform_stats
    from utils.auth_utils import get_current_user
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

logger = logging.getLogger(__name__)

def show():
    """
    Render the home page for authenticated users
    """
    try:
        # Hero section with light green background
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: #2e7d32; font-size: 3rem; margin-bottom: 1rem;">
                🏠 Welcome to HAVEN
            </h1>
            <h3 style="color: #388e3c; margin-bottom: 2rem;">
                Empowering Communities Through Crowdfunding
            </h3>
            <p style="color: #4caf50; font-size: 1.2rem; max-width: 600px; margin: 0 auto;">
                Join thousands of changemakers who are making a difference in their communities. 
                Start your campaign today or support causes you care about.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h3 style="color: #2e7d32;">🎯 Create Campaign</h3>
                <p style="color: #666; margin-bottom: 1.5rem;">Launch your crowdfunding campaign</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Start Campaign", key="start_campaign", use_container_width=True):
                st.session_state.current_page = 'create_campaign'
                st.rerun()
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h3 style="color: #2e7d32;">🔍 Browse Projects</h3>
                <p style="color: #666; margin-bottom: 1.5rem;">Discover amazing projects</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🌟 Explore", key="explore_projects", use_container_width=True):
                st.session_state.current_page = 'explore'
                st.rerun()
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h3 style="color: #2e7d32;">💝 Support Causes</h3>
                <p style="color: #666; margin-bottom: 1.5rem;">Make a difference today</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("❤️ Donate", key="support_causes", use_container_width=True):
                st.session_state.current_page = 'search'
                st.rerun()
        
        # Featured campaigns section
        st.markdown("---")
        st.markdown("### 🌟 Featured Campaigns")
        
        # Sample featured campaigns
        campaign_col1, campaign_col2 = st.columns(2)
        
        with campaign_col1:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #2e7d32;">🏥 Medical Emergency Support</h4>
                <p style="color: #666; margin-bottom: 1rem;">
                    Help provide critical medical care for families in need.
                </p>
                <div style="background: #e8f5e8; padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem;">
                    <strong style="color: #2e7d32;">₹2,50,000 raised of ₹5,00,000 goal</strong>
                </div>
                <div style="background: #4caf50; height: 8px; border-radius: 4px; margin-bottom: 1rem;">
                    <div style="background: #2e7d32; height: 8px; border-radius: 4px; width: 50%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with campaign_col2:
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #2e7d32;">📚 Education for All</h4>
                <p style="color: #666; margin-bottom: 1rem;">
                    Supporting underprivileged children's education and school supplies.
                </p>
                <div style="background: #e8f5e8; padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem;">
                    <strong style="color: #2e7d32;">₹1,80,000 raised of ₹3,00,000 goal</strong>
                </div>
                <div style="background: #4caf50; height: 8px; border-radius: 4px; margin-bottom: 1rem;">
                    <div style="background: #2e7d32; height: 8px; border-radius: 4px; width: 60%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Platform statistics
        st.markdown("---")
        st.markdown("### 📊 Platform Impact")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric(
                label="💰 Total Raised",
                value="₹12.5 Cr",
                delta="↗️ +15% this month"
            )
        
        with stat_col2:
            st.metric(
                label="🎯 Active Campaigns",
                value="1,247",
                delta="↗️ +23 new today"
            )
        
        with stat_col3:
            st.metric(
                label="👥 Community Members",
                value="45,678",
                delta="↗️ +156 this week"
            )
        
        with stat_col4:
            st.metric(
                label="🏆 Success Rate",
                value="78%",
                delta="↗️ +2% improvement"
            )
        
        # Recent activity
        st.markdown("---")
        st.markdown("### 🔥 Recent Activity")
        
        activity_items = [
            "🎉 **Medical Campaign** reached 100% funding goal!",
            "🌟 **Education Initiative** received 50 new donations",
            "💝 **Animal Welfare** campaign launched by verified NGO",
            "🏆 **Community Development** project completed successfully",
            "🚀 **Technology Innovation** campaign trending today"
        ]
        
        for item in activity_items:
            st.markdown(f"• {item}")
        
        # Call to action
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; margin-top: 2rem;">
            <h3 style="color: #1b5e20; margin-bottom: 1rem;">Ready to Make a Difference?</h3>
            <p style="color: #2e7d32; font-size: 1.1rem; margin-bottom: 1.5rem;">
                Whether you're looking to start a campaign or support existing causes, 
                HAVEN makes it easy to create positive change in your community.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        st.error("Sorry, there was an error loading the home page. Please try refreshing.")
        st.exception(e)

def render_home_page(api_client=None):
    """
    Legacy function name support - redirects to show()
    """
    show()

