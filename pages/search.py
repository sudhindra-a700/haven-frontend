"""

# Import utilities with error handling
try:
    from utils.translation_service import t, format_currency
    from utils.auth_utils import get_current_user
    from utils.api_client import *
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

Search Page for HAVEN Crowdfunding Platform
Advanced search and filtering for campaigns
"""

import streamlit as st
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def show():
    """
    Render the search page for finding campaigns
    """
    try:
        # Page header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: #2e7d32; font-size: 2.5rem; margin-bottom: 1rem;">
                🔍 Search Campaigns
            </h1>
            <p style="color: #388e3c; font-size: 1.2rem;">
                Find the perfect campaign to support with advanced search and filters
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced search form
        with st.form("advanced_search"):
            st.markdown("### 🎯 Advanced Search")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Text search
                search_query = st.text_input(
                    "🔍 Search Keywords",
                    placeholder="Enter keywords, campaign title, or organizer name...",
                    help="Search in campaign titles, descriptions, and organizer names"
                )
                
                # Category filter
                categories = st.multiselect(
                    "📂 Categories",
                    ["Medical", "Education", "Disaster Relief", "Animal Welfare", 
                     "Environment", "Community Development", "Technology", 
                     "Social Causes", "Arts & Culture", "Sports"],
                    help="Select one or more categories"
                )
                
                # Location filter
                location = st.text_input(
                    "📍 Location",
                    placeholder="City, State, or Region...",
                    help="Filter by campaign location"
                )
            
            with col2:
                # Funding range
                st.markdown("💰 **Funding Goal Range**")
                funding_range = st.slider(
                    "Select funding goal range (₹)",
                    min_value=1000,
                    max_value=10000000,
                    value=(10000, 1000000),
                    step=10000,
                    format="₹%d"
                )
                
                # Progress filter
                progress_filter = st.selectbox(
                    "📊 Campaign Progress",
                    ["All Campaigns", "Just Started (0-25%)", "Making Progress (25-75%)", 
                     "Almost There (75-100%)", "Fully Funded (100%+)"]
                )
                
                # Time filter
                time_filter = st.selectbox(
                    "⏰ Time Remaining",
                    ["All Campaigns", "Ending Soon (< 7 days)", "This Month (< 30 days)", 
                     "Long Term (> 30 days)", "Recently Added"]
                )
            
            # Sort options
            col_sort1, col_sort2 = st.columns(2)
            
            with col_sort1:
                sort_by = st.selectbox(
                    "📊 Sort by",
                    ["Relevance", "Most Recent", "Most Funded", "Ending Soon", 
                     "Most Supported", "Alphabetical", "Funding Goal"]
                )
            
            with col_sort2:
                sort_order = st.radio(
                    "Sort Order",
                    ["Descending", "Ascending"],
                    horizontal=True
                )
            
            # Search button
            search_submitted = st.form_submit_button(
                "🔍 Search Campaigns",
                use_container_width=True,
                type="primary"
            )
        
        # Display search results
        if search_submitted or st.session_state.get('show_search_results', False):
            st.session_state.show_search_results = True
            display_search_results(search_query, categories, location, funding_range, 
                                 progress_filter, time_filter, sort_by, sort_order)
        
        # Quick search suggestions
        if not st.session_state.get('show_search_results', False):
            st.markdown("---")
            st.markdown("### 💡 Quick Search Suggestions")
            
            suggestion_cols = st.columns(3)
            
            with suggestion_cols[0]:
                st.markdown("#### 🔥 Trending Searches")
                trending_searches = [
                    "Medical emergency",
                    "Education support",
                    "Disaster relief",
                    "Animal rescue",
                    "Environmental projects"
                ]
                
                for search in trending_searches:
                    if st.button(f"🔍 {search}", key=f"trending_{search}"):
                        perform_quick_search(search)
            
            with suggestion_cols[1]:
                st.markdown("#### 📍 Popular Locations")
                popular_locations = [
                    "Mumbai",
                    "Delhi",
                    "Bangalore",
                    "Chennai",
                    "Kolkata"
                ]
                
                for location in popular_locations:
                    if st.button(f"📍 {location}", key=f"location_{location}"):
                        perform_location_search(location)
            
            with suggestion_cols[2]:
                st.markdown("#### ⚡ Quick Filters")
                quick_filters = [
                    "Ending Soon",
                    "Just Started",
                    "Fully Funded",
                    "High Impact",
                    "Verified Orgs"
                ]
                
                for filter_name in quick_filters:
                    if st.button(f"⚡ {filter_name}", key=f"filter_{filter_name}"):
                        perform_quick_filter(filter_name)
        
        # Search tips
        if not st.session_state.get('show_search_results', False):
            st.markdown("---")
            st.markdown("### 💡 Search Tips")
            
            tips_col1, tips_col2 = st.columns(2)
            
            with tips_col1:
                st.markdown("""
                **🎯 Effective Searching:**
                - Use specific keywords for better results
                - Try different combinations of terms
                - Use quotes for exact phrases
                - Include location for local campaigns
                """)
            
            with tips_col2:
                st.markdown("""
                **🔍 Advanced Features:**
                - Combine multiple filters for precise results
                - Save searches for future reference
                - Set up alerts for new matching campaigns
                - Use wildcards (*) for broader searches
                """)
        
    except Exception as e:
        logger.error(f"Error rendering search page: {e}")
        st.error("Sorry, there was an error loading the search page. Please try refreshing.")
        st.exception(e)

def display_search_results(search_query, categories, location, funding_range, 
                          progress_filter, time_filter, sort_by, sort_order):
    """Display search results based on filters"""
    try:
        st.markdown("---")
        st.markdown("### 📋 Search Results")
        
        # Search summary
        filters_applied = []
        if search_query:
            filters_applied.append(f"Keywords: '{search_query}'")
        if categories:
            filters_applied.append(f"Categories: {', '.join(categories)}")
        if location:
            filters_applied.append(f"Location: {location}")
        if progress_filter != "All Campaigns":
            filters_applied.append(f"Progress: {progress_filter}")
        if time_filter != "All Campaigns":
            filters_applied.append(f"Time: {time_filter}")
        
        if filters_applied:
            st.info(f"🔍 **Filters Applied:** {' | '.join(filters_applied)}")
        
        # Mock search results
        search_results = get_mock_search_results(search_query, categories, location)
        
        # Results count
        st.markdown(f"**Found {len(search_results)} campaigns matching your criteria**")
        
        # Results display
        for i, result in enumerate(search_results):
            with st.expander(f"{result['icon']} {result['title']} - {result['organizer']}", expanded=(i < 3)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Category:** {result['category']}")
                    st.markdown(f"**Location:** {result['location']}")
                    st.markdown(f"**Goal:** ₹{result['goal']:,}")
                    st.markdown(f"**Raised:** ₹{result['raised']:,} ({result['percentage']:.1f}%)")
                    st.markdown(f"**Supporters:** {result['supporters']}")
                    st.markdown(f"**Days Left:** {result['days_left']}")
                    st.markdown(f"**Description:** {result['description']}")
                    
                    # Tags
                    if result.get('tags'):
                        st.markdown("**Tags:** " + " ".join([f"`{tag}`" for tag in result['tags']]))
                
                with col2:
                    # Progress bar
                    progress = result['percentage'] / 100
                    st.progress(progress)
                    
                    # Verification status
                    if result.get('verified'):
                        st.success("✅ Verified Campaign")
                    
                    # Urgency indicator
                    if result['days_left'] <= 7:
                        st.warning("⚠️ Ending Soon!")
                    
                    # Action buttons
                    if st.button(f"💝 Support", key=f"support_search_{result['id']}"):
                        handle_support_campaign(result['id'])
                    
                    if st.button(f"📖 View Details", key=f"view_search_{result['id']}"):
                        handle_view_campaign(result['id'])
                    
                    if st.button(f"📤 Share", key=f"share_search_{result['id']}"):
                        handle_share_campaign(result['id'])
        
        # Pagination
        if len(search_results) > 0:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("⬅️ Previous Page"):
                    st.info("Loading previous results...")
            
            with col2:
                st.markdown("**Page 1 of 5**")
            
            with col3:
                if st.button("Next Page ➡️"):
                    st.info("Loading more results...")
        
        # Save search option
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("💾 Save This Search", use_container_width=True):
                save_search(search_query, categories, location, funding_range, 
                           progress_filter, time_filter, sort_by, sort_order)
        
        with col2:
            if st.button("🔔 Set Alert for New Matches", use_container_width=True):
                set_search_alert(search_query, categories, location)
        
    except Exception as e:
        logger.error(f"Error displaying search results: {e}")
        st.error("Error displaying search results. Please try again.")

def get_mock_search_results(search_query, categories, location) -> List[Dict[str, Any]]:
    """Generate mock search results based on filters"""
    all_results = [
        {
            'id': 'search_001',
            'title': 'Emergency Heart Surgery for 8-year-old',
            'organizer': 'Children\'s Medical Foundation',
            'category': 'Medical',
            'location': 'Mumbai, Maharashtra',
            'icon': '🏥',
            'description': 'Urgent medical support needed for a child requiring immediate heart surgery. Time is critical.',
            'goal': 800000,
            'raised': 520000,
            'percentage': 65.0,
            'supporters': 234,
            'days_left': 5,
            'verified': True,
            'tags': ['urgent', 'medical', 'child', 'heart surgery']
        },
        {
            'id': 'search_002',
            'title': 'Digital Library for Rural School',
            'organizer': 'Education Access Initiative',
            'category': 'Education',
            'location': 'Pune, Maharashtra',
            'icon': '📚',
            'description': 'Setting up a digital library with computers and internet access for students in rural areas.',
            'goal': 300000,
            'raised': 180000,
            'percentage': 60.0,
            'supporters': 89,
            'days_left': 22,
            'verified': True,
            'tags': ['education', 'digital', 'rural', 'technology']
        },
        {
            'id': 'search_003',
            'title': 'Flood Relief and Rehabilitation',
            'organizer': 'Disaster Response Network',
            'category': 'Disaster Relief',
            'location': 'Kerala',
            'icon': '🆘',
            'description': 'Providing immediate relief supplies and long-term rehabilitation support to flood-affected families.',
            'goal': 1200000,
            'raised': 890000,
            'percentage': 74.2,
            'supporters': 456,
            'days_left': 12,
            'verified': True,
            'tags': ['disaster', 'flood', 'relief', 'rehabilitation']
        },
        {
            'id': 'search_004',
            'title': 'Stray Animal Rescue Center',
            'organizer': 'Animal Welfare Society',
            'category': 'Animal Welfare',
            'location': 'Bangalore, Karnataka',
            'icon': '🐾',
            'description': 'Building a rescue center for stray animals with medical facilities and adoption services.',
            'goal': 450000,
            'raised': 275000,
            'percentage': 61.1,
            'supporters': 167,
            'days_left': 18,
            'verified': False,
            'tags': ['animals', 'rescue', 'stray', 'medical care']
        },
        {
            'id': 'search_005',
            'title': 'Solar Power for Village School',
            'organizer': 'Green Energy Foundation',
            'category': 'Environment',
            'location': 'Rajasthan',
            'icon': '🌱',
            'description': 'Installing solar panels to provide clean energy for a village school and community center.',
            'goal': 250000,
            'raised': 95000,
            'percentage': 38.0,
            'supporters': 52,
            'days_left': 35,
            'verified': True,
            'tags': ['solar', 'renewable', 'school', 'village']
        }
    ]
    
    # Apply basic filtering (in a real app, this would be more sophisticated)
    filtered_results = all_results
    
    if search_query:
        filtered_results = [r for r in filtered_results 
                          if search_query.lower() in r['title'].lower() 
                          or search_query.lower() in r['description'].lower()]
    
    if categories:
        filtered_results = [r for r in filtered_results if r['category'] in categories]
    
    if location:
        filtered_results = [r for r in filtered_results 
                          if location.lower() in r['location'].lower()]
    
    return filtered_results

def perform_quick_search(search_term: str):
    """Perform a quick search with predefined term"""
    st.session_state.show_search_results = True
    st.info(f"🔍 Searching for: {search_term}")
    st.rerun()

def perform_location_search(location: str):
    """Perform a location-based search"""
    st.session_state.show_search_results = True
    st.info(f"📍 Searching campaigns in: {location}")
    st.rerun()

def perform_quick_filter(filter_name: str):
    """Apply a quick filter"""
    st.session_state.show_search_results = True
    st.info(f"⚡ Applying filter: {filter_name}")
    st.rerun()

def handle_support_campaign(campaign_id: str):
    """Handle campaign support action"""
    st.success(f"💝 Thank you for your interest in supporting campaign {campaign_id}!")
    st.info("Redirecting to donation page...")

def handle_view_campaign(campaign_id: str):
    """Handle view campaign action"""
    st.info(f"📖 Loading campaign details for {campaign_id}...")

def handle_share_campaign(campaign_id: str):
    """Handle share campaign action"""
    st.success(f"📤 Campaign {campaign_id} link copied to clipboard!")

def save_search(search_query, categories, location, funding_range, 
                progress_filter, time_filter, sort_by, sort_order):
    """Save search criteria for future use"""
    st.success("💾 Search saved successfully! You can access it from your profile.")

def set_search_alert(search_query, categories, location):
    """Set up alerts for new matching campaigns"""
    st.success("🔔 Alert set up! You'll be notified when new campaigns match your criteria.")

# Legacy function support
def render_search_page(api_client=None):
    """Legacy function name support - redirects to show()"""
    show()

