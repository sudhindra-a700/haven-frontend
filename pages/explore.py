"""

# Import utilities with error handling
try:
    from utils.translation_service import t, format_currency
    from utils.auth_utils import get_current_user
    from utils.api_client import *
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

Explore Page for HAVEN Crowdfunding Platform
Browse and discover campaigns across different categories
"""

import streamlit as st
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def show():
    """
    Render the explore page for browsing campaigns
    """
    try:
        # Page header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: #2e7d32; font-size: 2.5rem; margin-bottom: 1rem;">
                🔍 Explore Campaigns
            </h1>
            <p style="color: #388e3c; font-size: 1.2rem;">
                Discover amazing projects and causes that need your support
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filters and search
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_query = st.text_input(
                "🔍 Search campaigns",
                placeholder="Search by title, description, or organizer...",
                help="Find specific campaigns or causes"
            )
        
        with col2:
            category_filter = st.selectbox(
                "📂 Category",
                ["All Categories", "Medical", "Education", "Disaster Relief", 
                 "Animal Welfare", "Environment", "Community Development",
                 "Technology", "Social Causes", "Arts & Culture", "Sports"]
            )
        
        with col3:
            sort_by = st.selectbox(
                "📊 Sort by",
                ["Most Recent", "Most Funded", "Ending Soon", "Most Supported", "Alphabetical"]
            )
        
        # Campaign statistics
        st.markdown("---")
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("🎯 Active Campaigns", "1,247", "+23 today")
        
        with col_stat2:
            st.metric("💰 Total Raised", "₹12.5 Cr", "+₹2.3L today")
        
        with col_stat3:
            st.metric("👥 Total Supporters", "45,678", "+156 this week")
        
        with col_stat4:
            st.metric("🏆 Success Rate", "78%", "+2% this month")
        
        # Featured campaigns
        st.markdown("---")
        st.markdown("### 🌟 Featured Campaigns")
        
        featured_campaigns = get_featured_campaigns()
        
        for i in range(0, len(featured_campaigns), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                if i < len(featured_campaigns):
                    display_campaign_card(featured_campaigns[i])
            
            with col2:
                if i + 1 < len(featured_campaigns):
                    display_campaign_card(featured_campaigns[i + 1])
        
        # Category-wise campaigns
        st.markdown("---")
        st.markdown("### 📂 Browse by Category")
        
        categories = [
            {"name": "Medical", "icon": "🏥", "count": 342, "color": "#f44336"},
            {"name": "Education", "icon": "📚", "count": 198, "color": "#2196f3"},
            {"name": "Disaster Relief", "icon": "🆘", "count": 156, "color": "#ff9800"},
            {"name": "Animal Welfare", "icon": "🐾", "count": 124, "color": "#4caf50"},
            {"name": "Environment", "icon": "🌱", "count": 98, "color": "#8bc34a"},
            {"name": "Community Development", "icon": "🏘️", "count": 87, "color": "#9c27b0"}
        ]
        
        for i in range(0, len(categories), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(categories):
                    category = categories[i + j]
                    with col:
                        if st.button(
                            f"{category['icon']} {category['name']}\n{category['count']} campaigns",
                            key=f"category_{category['name']}",
                            use_container_width=True
                        ):
                            st.session_state.selected_category = category['name']
                            st.rerun()
        
        # Recent campaigns
        st.markdown("---")
        st.markdown("### 🆕 Recently Added")
        
        recent_campaigns = get_recent_campaigns()
        
        for campaign in recent_campaigns:
            with st.expander(f"{campaign['icon']} {campaign['title']} - {campaign['organizer']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Category:** {campaign['category']}")
                    st.markdown(f"**Goal:** ₹{campaign['goal']:,}")
                    st.markdown(f"**Raised:** ₹{campaign['raised']:,} ({campaign['percentage']:.1f}%)")
                    st.markdown(f"**Description:** {campaign['description']}")
                
                with col2:
                    # Progress bar
                    progress = campaign['percentage'] / 100
                    st.progress(progress)
                    
                    # Action buttons
                    if st.button(f"💝 Support", key=f"support_{campaign['id']}"):
                        handle_support_campaign(campaign['id'])
                    
                    if st.button(f"📖 Learn More", key=f"learn_{campaign['id']}"):
                        handle_view_campaign(campaign['id'])
        
        # Load more button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📄 Load More Campaigns", use_container_width=True):
                load_more_campaigns()
        
    except Exception as e:
        logger.error(f"Error rendering explore page: {e}")
        st.error("Sorry, there was an error loading the explore page. Please try refreshing.")
        st.exception(e)

def display_campaign_card(campaign: Dict[str, Any]):
    """Display a campaign card"""
    progress_percentage = (campaign['raised'] / campaign['goal']) * 100
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
        <h4 style="color: #2e7d32; margin-bottom: 0.5rem;">
            {campaign['icon']} {campaign['title']}
        </h4>
        <p style="color: #666; margin-bottom: 1rem; font-size: 0.9rem;">
            by {campaign['organizer']} • {campaign['category']}
        </p>
        <p style="color: #333; margin-bottom: 1rem;">
            {campaign['description'][:100]}...
        </p>
        <div style="background: #e8f5e8; padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem;">
            <strong style="color: #2e7d32;">
                ₹{campaign['raised']:,} raised of ₹{campaign['goal']:,} goal
            </strong>
        </div>
        <div style="background: #4caf50; height: 8px; border-radius: 4px; margin-bottom: 1rem;">
            <div style="background: #2e7d32; height: 8px; border-radius: 4px; width: {min(progress_percentage, 100)}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <small style="color: #666;">{campaign['supporters']} supporters</small>
            <small style="color: #666;">{campaign['days_left']} days left</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"💝 Support", key=f"support_featured_{campaign['id']}", use_container_width=True):
            handle_support_campaign(campaign['id'])
    
    with col2:
        if st.button(f"📖 View", key=f"view_featured_{campaign['id']}", use_container_width=True):
            handle_view_campaign(campaign['id'])

def get_featured_campaigns() -> List[Dict[str, Any]]:
    """Get featured campaigns data"""
    return [
        {
            'id': 'feat_001',
            'title': 'Emergency Surgery for Child',
            'organizer': 'Helping Hands NGO',
            'category': 'Medical',
            'icon': '🏥',
            'description': 'Urgent medical support needed for a 7-year-old child requiring life-saving surgery. Every contribution counts.',
            'goal': 500000,
            'raised': 325000,
            'supporters': 156,
            'days_left': 12
        },
        {
            'id': 'feat_002',
            'title': 'School for Underprivileged Children',
            'organizer': 'Education First Foundation',
            'category': 'Education',
            'icon': '📚',
            'description': 'Building a school in rural area to provide quality education to underprivileged children.',
            'goal': 1000000,
            'raised': 680000,
            'supporters': 234,
            'days_left': 25
        },
        {
            'id': 'feat_003',
            'title': 'Flood Relief for Affected Families',
            'organizer': 'Disaster Response Team',
            'category': 'Disaster Relief',
            'icon': '🆘',
            'description': 'Providing immediate relief and rehabilitation support to families affected by recent floods.',
            'goal': 750000,
            'raised': 420000,
            'supporters': 189,
            'days_left': 8
        },
        {
            'id': 'feat_004',
            'title': 'Animal Shelter Expansion',
            'organizer': 'Paws & Hearts Shelter',
            'category': 'Animal Welfare',
            'icon': '🐾',
            'description': 'Expanding our animal shelter to rescue and care for more abandoned and injured animals.',
            'goal': 300000,
            'raised': 180000,
            'supporters': 98,
            'days_left': 18
        }
    ]

def get_recent_campaigns() -> List[Dict[str, Any]]:
    """Get recent campaigns data"""
    return [
        {
            'id': 'rec_001',
            'title': 'Clean Water Project',
            'organizer': 'Water for All Initiative',
            'category': 'Community Development',
            'icon': '💧',
            'description': 'Installing water purification systems in remote villages to provide clean drinking water.',
            'goal': 400000,
            'raised': 85000,
            'percentage': 21.3,
            'supporters': 42
        },
        {
            'id': 'rec_002',
            'title': 'Tech Education for Girls',
            'organizer': 'Code Sisters',
            'category': 'Education',
            'icon': '💻',
            'description': 'Teaching coding and technology skills to girls in underserved communities.',
            'goal': 250000,
            'raised': 120000,
            'percentage': 48.0,
            'supporters': 67
        },
        {
            'id': 'rec_003',
            'title': 'Reforestation Drive',
            'organizer': 'Green Earth Collective',
            'category': 'Environment',
            'icon': '🌳',
            'description': 'Planting 10,000 trees to combat deforestation and climate change.',
            'goal': 150000,
            'raised': 95000,
            'percentage': 63.3,
            'supporters': 134
        }
    ]

def handle_support_campaign(campaign_id: str):
    """Handle campaign support action"""
    st.success(f"💝 Thank you for your interest in supporting campaign {campaign_id}!")
    st.info("Redirecting to donation page...")
    # In a real implementation, this would redirect to the donation flow

def handle_view_campaign(campaign_id: str):
    """Handle view campaign action"""
    st.info(f"📖 Loading campaign details for {campaign_id}...")
    # In a real implementation, this would show the full campaign page

def load_more_campaigns():
    """Load more campaigns"""
    with st.spinner("Loading more campaigns..."):
        import time
        time.sleep(1)
        st.success("✅ More campaigns loaded!")
        st.rerun()

# Legacy function support
def render_explore_page(api_client=None):
    """Legacy function name support - redirects to show()"""
    show()

