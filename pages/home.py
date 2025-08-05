"""
Home Page for HAVEN Crowdfunding Platform
"""

import streamlit as st
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def render_home_page(api_client):
    """Render the home page"""
    try:
        # Hero section
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #667eea; font-size: 3rem; margin-bottom: 1rem;">
                🏠 Welcome to HAVEN
            </h1>
            <h3 style="color: #666; margin-bottom: 2rem;">
                Empowering Communities Through Crowdfunding
            </h3>
            <p style="font-size: 1.2rem; color: #888; max-width: 600px; margin: 0 auto;">
                Join thousands of changemakers who are making a difference in their communities. 
                Start your campaign today or support causes you care about.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Call-to-action buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🚀 Start a Campaign", key="start_campaign", use_container_width=True):
                    if st.session_state.get('authenticated'):
                        st.session_state.current_page = 'create_campaign'
                        st.experimental_rerun()
                    else:
                        st.session_state.current_page = 'register'
                        st.experimental_rerun()
            
            with col_b:
                if st.button("💝 Explore Campaigns", key="explore_campaigns", use_container_width=True):
                    st.session_state.current_page = 'campaigns'
                    st.experimental_rerun()
        
        st.markdown("---")
        
        # Platform statistics
        render_platform_stats(api_client)
        
        st.markdown("---")
        
        # Featured campaigns
        render_featured_campaigns(api_client)
        
        st.markdown("---")
        
        # How it works section
        render_how_it_works()
        
        st.markdown("---")
        
        # Success stories
        render_success_stories()
        
        st.markdown("---")
        
        # Categories section
        render_categories()
        
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        st.error("Unable to load home page. Please refresh and try again.")

def render_platform_stats(api_client):
    """Render platform statistics"""
    st.markdown("### 📊 Platform Impact")
    
    try:
        stats = api_client.get_platform_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Campaigns",
                value=f"{stats.get('total_campaigns', 0):,}",
                delta="+12 this week"
            )
        
        with col2:
            st.metric(
                label="Amount Raised",
                value=f"₹{stats.get('total_raised', 0):,.0f}",
                delta="+₹50,000 this week"
            )
        
        with col3:
            st.metric(
                label="Active Campaigns",
                value=f"{stats.get('active_campaigns', 0):,}",
                delta="+5 this week"
            )
        
        with col4:
            st.metric(
                label="Community Members",
                value=f"{stats.get('active_users', 0):,}",
                delta="+25 this week"
            )
    
    except Exception as e:
        logger.warning(f"Could not load platform stats: {e}")
        # Show placeholder stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Campaigns", "150+")
        with col2:
            st.metric("Amount Raised", "₹2.5M+")
        with col3:
            st.metric("Active Campaigns", "45+")
        with col4:
            st.metric("Community Members", "1,200+")

def render_featured_campaigns(api_client):
    """Render featured campaigns"""
    st.markdown("### ⭐ Featured Campaigns")
    
    try:
        # Get featured campaigns (active campaigns sorted by current amount)
        campaigns = api_client.get_campaigns(
            limit=6,
            status='active',
            sort_by='current_amount',
            sort_order='desc'
        )
        
        if campaigns:
            # Display campaigns in a grid
            for i in range(0, len(campaigns), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(campaigns):
                        campaign = campaigns[i + j]
                        with col:
                            render_campaign_card(campaign)
        else:
            st.info("No featured campaigns available at the moment.")
    
    except Exception as e:
        logger.warning(f"Could not load featured campaigns: {e}")
        st.info("Featured campaigns will be displayed here.")

def render_campaign_card(campaign: Dict[str, Any]):
    """Render a campaign card"""
    try:
        progress = min(100, (campaign.get('current_amount', 0) / campaign.get('goal_amount', 1)) * 100)
        
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; background: white;">
            <h4 style="margin: 0 0 0.5rem 0; color: #333;">{campaign.get('title', 'Untitled Campaign')}</h4>
            <p style="color: #666; font-size: 0.9rem; margin: 0 0 1rem 0;">
                {campaign.get('short_description', campaign.get('description', ''))[:100]}...
            </p>
            <div style="margin: 1rem 0;">
                <div style="background: #f0f0f0; border-radius: 10px; height: 8px;">
                    <div style="background: #667eea; height: 8px; border-radius: 10px; width: {progress}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.8rem;">
                    <span>₹{campaign.get('current_amount', 0):,.0f} raised</span>
                    <span>{progress:.1f}% of ₹{campaign.get('goal_amount', 0):,.0f}</span>
                </div>
            </div>
            <div style="text-align: center;">
                <small style="color: #888;">by {campaign.get('creator', {}).get('full_name', 'Anonymous')}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"View Campaign", key=f"view_campaign_{campaign.get('id')}", use_container_width=True):
            st.session_state.selected_campaign_id = campaign.get('id')
            st.session_state.current_page = 'campaign_detail'
            st.experimental_rerun()
    
    except Exception as e:
        logger.warning(f"Error rendering campaign card: {e}")

def render_how_it_works():
    """Render how it works section"""
    st.markdown("### 🔄 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
            <h4>1. Create Your Campaign</h4>
            <p style="color: #666;">
                Tell your story, set your goal, and share why your cause matters. 
                Add photos and videos to make it compelling.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📢</div>
            <h4>2. Share & Promote</h4>
            <p style="color: #666;">
                Share your campaign with friends, family, and social networks. 
                The more people know, the more support you'll receive.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💰</div>
            <h4>3. Receive Donations</h4>
            <p style="color: #666;">
                Collect donations securely and keep supporters updated 
                on your progress with regular updates.
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_success_stories():
    """Render success stories section"""
    st.markdown("### 🎉 Success Stories")
    
    stories = [
        {
            "title": "Clean Water for Rural Villages",
            "amount": "₹2,50,000",
            "impact": "Provided clean water access to 500+ families",
            "image": "💧"
        },
        {
            "title": "Education for Underprivileged Children",
            "amount": "₹1,80,000",
            "impact": "Sponsored education for 50 children for one year",
            "image": "📚"
        },
        {
            "title": "Medical Treatment Support",
            "amount": "₹3,20,000",
            "impact": "Helped 15 families with critical medical expenses",
            "image": "🏥"
        }
    ]
    
    for story in stories:
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; font-size: 3rem; padding: 1rem;">
                {story['image']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="padding: 1rem;">
                <h4 style="margin: 0 0 0.5rem 0; color: #333;">{story['title']}</h4>
                <p style="color: #667eea; font-weight: bold; margin: 0 0 0.5rem 0;">
                    {story['amount']} raised
                </p>
                <p style="color: #666; margin: 0;">
                    {story['impact']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")

def render_categories():
    """Render campaign categories"""
    st.markdown("### 🏷️ Campaign Categories")
    
    categories = [
        {"name": "Education", "icon": "📚", "count": "25+ campaigns"},
        {"name": "Healthcare", "icon": "🏥", "count": "18+ campaigns"},
        {"name": "Environment", "icon": "🌱", "count": "12+ campaigns"},
        {"name": "Community", "icon": "🏘️", "count": "30+ campaigns"},
        {"name": "Emergency", "icon": "🚨", "count": "8+ campaigns"},
        {"name": "Animals", "icon": "🐾", "count": "15+ campaigns"}
    ]
    
    cols = st.columns(3)
    
    for i, category in enumerate(categories):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; 
                        text-align: center; background: white; cursor: pointer;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{category['icon']}</div>
                <h4 style="margin: 0 0 0.25rem 0; color: #333;">{category['name']}</h4>
                <small style="color: #888;">{category['count']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Explore {category['name']}", key=f"category_{category['name']}", use_container_width=True):
                st.session_state.selected_category = category['name'].lower()
                st.session_state.current_page = 'campaigns'
                st.experimental_rerun()

