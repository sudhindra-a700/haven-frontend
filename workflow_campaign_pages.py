# Modified workflow_campaign_pages.py - Campaign Management with Bootstrap Icons
# This file replaces your existing workflow_campaign_pages.py

import streamlit as st
from utils.icon_utils import display_icon, get_icon_html, icon_button
from config.icon_mapping import get_icon, ICON_COLORS, ICON_SIZES

def render_campaign_creation_form():
    """Render campaign creation form with Bootstrap icons."""
    st.markdown(f"""
    <h1>{get_icon_html('plus-circle-fill', 32, ICON_COLORS['primary'])} Create New Campaign</h1>
    <p style="color: {ICON_COLORS['muted']};">Bring your project to life with crowdfunding</p>
    """, unsafe_allow_html=True)
    
    with st.form("campaign_creation"):
        # Basic Information
        st.markdown(f"""
        <h3>{get_icon_html('info-circle-fill', ICON_SIZES['lg'])} Basic Information</h3>
        """, unsafe_allow_html=True)
        
        title = st.text_input(f"{get_icon_html('type', ICON_SIZES['sm'])} Campaign Title")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox(
                f"{get_icon_html('tags', ICON_SIZES['sm'])} Category",
                ["Technology", "Arts", "Environment", "Education", "Health", "Games"]
            )
        with col2:
            location = st.text_input(f"{get_icon_html('geo-alt', ICON_SIZES['sm'])} Location")
        
        description = st.text_area(f"{get_icon_html('file-text', ICON_SIZES['sm'])} Description", height=150)
        
        # Funding Goals
        st.markdown(f"""
        <h3>{get_icon_html('currency-dollar', ICON_SIZES['lg'])} Funding Goals</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            funding_goal = st.number_input(f"{get_icon_html('bullseye', ICON_SIZES['sm'])} Funding Goal ($)", min_value=100)
        with col2:
            duration = st.number_input(f"{get_icon_html('calendar', ICON_SIZES['sm'])} Campaign Duration (days)", min_value=1, max_value=90)
        
        # Media Upload
        st.markdown(f"""
        <h3>{get_icon_html('images', ICON_SIZES['lg'])} Media</h3>
        """, unsafe_allow_html=True)
        
        main_image = st.file_uploader(f"{get_icon_html('image', ICON_SIZES['sm'])} Main Campaign Image", type=['png', 'jpg', 'jpeg'])
        video_url = st.text_input(f"{get_icon_html('play-circle', ICON_SIZES['sm'])} Video URL (optional)")
        
        # Rewards/Perks
        st.markdown(f"""
        <h3>{get_icon_html('gift', ICON_SIZES['lg'])} Rewards & Perks</h3>
        """, unsafe_allow_html=True)
        
        if st.checkbox(f"{get_icon_html('plus', ICON_SIZES['sm'])} Add Reward Tiers"):
            num_rewards = st.number_input("Number of reward tiers", min_value=1, max_value=10, value=3)
            
            for i in range(num_rewards):
                st.markdown(f"**{get_icon_html('award', ICON_SIZES['sm'])} Reward Tier {i+1}**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    reward_amount = st.number_input(f"Amount ($)", key=f"reward_amount_{i}", min_value=1)
                with col2:
                    reward_title = st.text_input(f"Title", key=f"reward_title_{i}")
                with col3:
                    reward_quantity = st.number_input(f"Quantity", key=f"reward_qty_{i}", min_value=1)
                
                reward_description = st.text_area(f"Description", key=f"reward_desc_{i}", height=80)
        
        # Submit button
        if st.form_submit_button(f"{get_icon_html('rocket-takeoff', ICON_SIZES['sm'])} Launch Campaign"):
            if validate_campaign_data(title, category, description, funding_goal):
                st.success(f"{get_icon_html('check-circle-fill', ICON_SIZES['sm'], ICON_COLORS['success'])} Campaign created successfully!")
                return True
            else:
                st.error(f"{get_icon_html('exclamation-triangle', ICON_SIZES['sm'], ICON_COLORS['warning'])} Please fill in all required fields")
    
    return False

def render_campaign_management_dashboard():
    """Render campaign management dashboard with Bootstrap icons."""
    st.markdown(f"""
    <h1>{get_icon_html('speedometer2', 32, ICON_COLORS['primary'])} Campaign Dashboard</h1>
    """, unsafe_allow_html=True)
    
    # Campaign stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {get_icon_html('currency-dollar', 32, ICON_COLORS['success'])}
            <h2 style="margin: 10px 0; color: {ICON_COLORS['success']};">$12,450</h2>
            <p style="margin: 0; color: {ICON_COLORS['muted']};">Total Raised</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {get_icon_html('people-fill', 32, ICON_COLORS['info'])}
            <h2 style="margin: 10px 0; color: {ICON_COLORS['info']};">156</h2>
            <p style="margin: 0; color: {ICON_COLORS['muted']};">Backers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {get_icon_html('calendar-event', 32, ICON_COLORS['warning'])}
            <h2 style="margin: 10px 0; color: {ICON_COLORS['warning']};">23</h2>
            <p style="margin: 0; color: {ICON_COLORS['muted']};">Days Left</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {get_icon_html('graph-up-arrow', 32, ICON_COLORS['primary'])}
            <h2 style="margin: 10px 0; color: {ICON_COLORS['primary']};">62%</h2>
            <p style="margin: 0; color: {ICON_COLORS['muted']};">Goal Reached</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown(f"""
    <h3>{get_icon_html('lightning-fill', ICON_SIZES['lg'])} Quick Actions</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if icon_button('pencil-square', 'Edit Campaign', 'edit_campaign', ICON_SIZES['sm']):
            st.info("Opening campaign editor...")
    
    with col2:
        if icon_button('megaphone', 'Post Update', 'post_update', ICON_SIZES['sm']):
            st.info("Opening update composer...")
    
    with col3:
        if icon_button('envelope', 'Message Backers', 'message_backers', ICON_SIZES['sm']):
            st.info("Opening messaging interface...")
    
    with col4:
        if icon_button('bar-chart', 'View Analytics', 'view_analytics', ICON_SIZES['sm']):
            st.info("Opening analytics dashboard...")

def render_campaign_browse_page():
    """Render campaign browsing page with Bootstrap icons."""
    st.markdown(f"""
    <h1>{get_icon_html('search', 32, ICON_COLORS['primary'])} Browse Campaigns</h1>
    """, unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = st.text_input(f"{get_icon_html('search', ICON_SIZES['sm'])} Search campaigns", placeholder="Enter keywords...")
    with col2:
        category_filter = st.selectbox(f"{get_icon_html('funnel', ICON_SIZES['sm'])} Category", ["All", "Technology", "Arts", "Environment", "Education"])
    with col3:
        sort_by = st.selectbox(f"{get_icon_html('sort-down', ICON_SIZES['sm'])} Sort by", ["Most Recent", "Most Funded", "Ending Soon", "Most Popular"])
    
    # Campaign grid
    render_campaign_grid()

def render_campaign_grid():
    """Render a grid of campaign cards with Bootstrap icons."""
    # Sample campaign data
    campaigns = [
        {
            "id": 1,
            "title": "Smart Home Garden System",
            "description": "Automated gardening for urban homes",
            "goal": 50000,
            "raised": 32500,
            "backers": 245,
            "days_left": 15,
            "category": "Technology",
            "status": "active",
            "image": None
        },
        {
            "id": 2,
            "title": "Eco-Friendly Water Bottles",
            "description": "Sustainable bottles made from ocean plastic",
            "goal": 25000,
            "raised": 28750,
            "backers": 412,
            "days_left": 3,
            "category": "Environment",
            "status": "completed",
            "image": None
        },
        {
            "id": 3,
            "title": "Educational Board Game",
            "description": "Teaching kids about climate change",
            "goal": 15000,
            "raised": 8200,
            "backers": 156,
            "days_left": 22,
            "category": "Education",
            "status": "active",
            "image": None
        },
        {
            "id": 4,
            "title": "Indie Music Album",
            "description": "Supporting local artists and musicians",
            "goal": 10000,
            "raised": 7500,
            "backers": 89,
            "days_left": 12,
            "category": "Arts",
            "status": "active",
            "image": None
        }
    ]
    
    for i in range(0, len(campaigns), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(campaigns):
                render_campaign_card(campaigns[i])
        
        with col2:
            if i + 1 < len(campaigns):
                render_campaign_card(campaigns[i + 1])

def render_campaign_card(campaign):
    """Render a single campaign card with Bootstrap icons."""
    # Determine category icon
    category_icons = {
        "Technology": "cpu-fill",
        "Environment": "tree-fill",
        "Education": "book-fill",
        "Health": "heart-pulse-fill",
        "Arts": "palette-fill",
        "Games": "controller"
    }
    
    category_icon = category_icons.get(campaign["category"], "tag-fill")
    
    # Calculate progress percentage
    progress = min((campaign["raised"] / campaign["goal"]) * 100, 100)
    
    # Status styling
    status_class = f"status-{campaign['status']}"
    status_icons = {
        "active": "play-circle-fill",
        "completed": "check-circle-fill",
        "pending": "clock-fill"
    }
    status_icon = status_icons.get(campaign["status"], "circle")
    
    st.markdown(f"""
    <div style="border: 1px solid #e0e0e0; border-radius: 12px; padding: 20px; margin: 10px 0; 
                background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: all 0.3s ease;">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                {get_icon_html(category_icon, 24, '#4CAF50')}
                <h3 style="margin: 0;">{campaign['title']}</h3>
            </div>
            <span style="display: inline-flex; align-items: center; gap: 5px; padding: 5px 12px; 
                         border-radius: 20px; font-size: 12px; font-weight: bold; 
                         background: #d4edda; color: #155724;">
                {get_icon_html(status_icon, 14)}
                {campaign['status'].title()}
            </span>
        </div>
        
        <p style="color: #666; margin-bottom: 15px;">{campaign['description']}</p>
        
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>{get_icon_html('currency-dollar', 16)} ${campaign['raised']:,} raised</span>
                <span>{progress:.1f}% of ${campaign['goal']:,}</span>
            </div>
            <div style="background: #e0e0e0; border-radius: 10px; height: 8px;">
                <div style="background: linear-gradient(90deg, #4CAF50, #66BB6A); 
                            height: 100%; border-radius: 10px; width: {progress}%;"></div>
            </div>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; gap: 20px;">
                <span style="display: flex; align-items: center; gap: 5px;">
                    {get_icon_html('people', 16, '#666')}
                    {campaign['backers']} backers
                </span>
                <span style="display: flex; align-items: center; gap: 5px;">
                    {get_icon_html('calendar', 16, '#666')}
                    {campaign['days_left']} days left
                </span>
            </div>
            <div style="display: flex; gap: 10px;">
                <button style="background: none; border: 1px solid #4CAF50; color: #4CAF50; 
                               padding: 5px 10px; border-radius: 5px; cursor: pointer;">
                    {get_icon_html('heart', 16)} Like
                </button>
                <button style="background: #4CAF50; border: none; color: white; 
                               padding: 5px 15px; border-radius: 5px; cursor: pointer;">
                    {get_icon_html('cash-coin', 16)} Back This
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_campaign_details_page(campaign_id):
    """Render detailed campaign page with Bootstrap icons."""
    st.markdown(f"""
    <h1>{get_icon_html('eye-fill', 32, ICON_COLORS['primary'])} Campaign Details</h1>
    """, unsafe_allow_html=True)
    
    # Campaign header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <h2>{get_icon_html('cpu-fill', 28, '#4CAF50')} Smart Home Garden System</h2>
        <p style="color: #666; font-size: 18px;">Automated gardening for urban homes</p>
        """, unsafe_allow_html=True)
        
        # Campaign description
        st.markdown(f"""
        <h3>{get_icon_html('file-text', ICON_SIZES['lg'])} About This Project</h3>
        """, unsafe_allow_html=True)
        
        st.write("""
        Our Smart Home Garden System revolutionizes urban gardening by providing 
        automated care for your plants. Using IoT sensors and AI, it monitors 
        soil moisture, light levels, and nutrient content to ensure optimal 
        growing conditions.
        """)
    
    with col2:
        # Funding progress
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0;">{get_icon_html('bullseye', 24)} Funding Progress</h3>
            <h2 style="color: #4CAF50;">$32,500</h2>
            <p style="color: #666;">raised of $50,000 goal</p>
            
            <div style="background: #e0e0e0; border-radius: 10px; height: 10px; margin: 15px 0;">
                <div style="background: linear-gradient(90deg, #4CAF50, #66BB6A); 
                            height: 100%; border-radius: 10px; width: 65%;"></div>
            </div>
            
            <div style="display: flex; justify-content: space-between; margin: 15px 0;">
                <span>{get_icon_html('people', 16)} 245 backers</span>
                <span>{get_icon_html('calendar', 16)} 15 days left</span>
            </div>
            
            <button style="width: 100%; background: #4CAF50; border: none; color: white; 
                           padding: 15px; border-radius: 8px; font-size: 16px; cursor: pointer;">
                {get_icon_html('cash-coin', 20)} Back This Project
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for additional content
    tab1, tab2, tab3, tab4 = st.tabs([
        f"{get_icon_html('info-circle', ICON_SIZES['sm'])} Story",
        f"{get_icon_html('gift', ICON_SIZES['sm'])} Rewards",
        f"{get_icon_html('chat-dots', ICON_SIZES['sm'])} Updates",
        f"{get_icon_html('people', ICON_SIZES['sm'])} Backers"
    ])
    
    with tab1:
        render_campaign_story_tab()
    
    with tab2:
        render_campaign_rewards_tab()
    
    with tab3:
        render_campaign_updates_tab()
    
    with tab4:
        render_campaign_backers_tab()

def render_campaign_story_tab():
    """Render campaign story tab."""
    st.markdown(f"""
    <h3>{get_icon_html('book', ICON_SIZES['lg'])} Project Story</h3>
    """, unsafe_allow_html=True)
    
    st.write("""
    ### The Problem
    Urban dwellers struggle to maintain healthy gardens due to busy lifestyles 
    and lack of gardening expertise. Many plants die from over or under-watering, 
    poor lighting, or nutrient deficiencies.
    
    ### Our Solution
    The Smart Home Garden System uses advanced sensors and machine learning to:
    - Monitor soil moisture and automatically water plants
    - Adjust LED grow lights based on plant needs
    - Track nutrient levels and alert users when fertilization is needed
    - Provide mobile app notifications and insights
    
    ### Why It Matters
    This system enables anyone to grow fresh herbs, vegetables, and flowers at home, 
    promoting healthier eating and sustainable living in urban environments.
    """)

def render_campaign_rewards_tab():
    """Render campaign rewards tab."""
    st.markdown(f"""
    <h3>{get_icon_html('gift-fill', ICON_SIZES['lg'])} Reward Tiers</h3>
    """, unsafe_allow_html=True)
    
    rewards = [
        {"amount": 25, "title": "Early Bird Special", "description": "Digital thank you + project updates", "claimed": 50, "total": 100},
        {"amount": 75, "title": "Starter Kit", "description": "Basic sensor kit + mobile app access", "claimed": 30, "total": 50},
        {"amount": 150, "title": "Complete System", "description": "Full garden system + installation guide", "claimed": 45, "total": 75},
        {"amount": 300, "title": "Premium Package", "description": "Complete system + premium plants + 1-year support", "claimed": 15, "total": 25}
    ]
    
    for reward in rewards:
        availability = f"{reward['claimed']}/{reward['total']} claimed"
        progress = (reward['claimed'] / reward['total']) * 100
        
        st.markdown(f"""
        <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin: 15px 0; background: white;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                <h4 style="margin: 0; color: #4CAF50;">${reward['amount']} - {reward['title']}</h4>
                <span style="color: #666; font-size: 14px;">{availability}</span>
            </div>
            <p style="color: #666; margin-bottom: 15px;">{reward['description']}</p>
            <div style="background: #f0f0f0; border-radius: 5px; height: 6px; margin-bottom: 10px;">
                <div style="background: #4CAF50; height: 100%; border-radius: 5px; width: {progress}%;"></div>
            </div>
            <button style="background: #4CAF50; border: none; color: white; padding: 10px 20px; 
                           border-radius: 5px; cursor: pointer;">
                {get_icon_html('cash-coin', 16)} Select Reward
            </button>
        </div>
        """, unsafe_allow_html=True)

def render_campaign_updates_tab():
    """Render campaign updates tab."""
    st.markdown(f"""
    <h3>{get_icon_html('megaphone-fill', ICON_SIZES['lg'])} Project Updates</h3>
    """, unsafe_allow_html=True)
    
    updates = [
        {"date": "2024-08-25", "title": "Prototype Testing Complete!", "content": "We've successfully tested our prototype with 10 beta users..."},
        {"date": "2024-08-20", "title": "Manufacturing Partner Confirmed", "content": "Excited to announce our partnership with GreenTech Manufacturing..."},
        {"date": "2024-08-15", "title": "50% Funding Milestone Reached", "content": "Thank you to all our amazing backers! We've reached 50% of our goal..."}
    ]
    
    for update in updates:
        st.markdown(f"""
        <div style="border-left: 4px solid #4CAF50; padding-left: 20px; margin: 20px 0;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                {get_icon_html('calendar-event', 20, '#4CAF50')}
                <span style="color: #666; font-size: 14px;">{update['date']}</span>
            </div>
            <h4 style="margin: 0 0 10px 0;">{update['title']}</h4>
            <p style="color: #666;">{update['content']}</p>
        </div>
        """, unsafe_allow_html=True)

def render_campaign_backers_tab():
    """Render campaign backers tab."""
    st.markdown(f"""
    <h3>{get_icon_html('people-fill', ICON_SIZES['lg'])} Our Backers</h3>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center; margin: 30px 0;">
        <h2>{get_icon_html('heart-fill', 32, '#FF6B6B')} 245 Amazing Backers</h2>
        <p style="color: #666;">Thank you to everyone who believes in our vision!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent backers
    recent_backers = [
        {"name": "John D.", "amount": 150, "time": "2 hours ago"},
        {"name": "Sarah M.", "amount": 75, "time": "5 hours ago"},
        {"name": "Mike R.", "amount": 300, "time": "1 day ago"},
        {"name": "Lisa K.", "amount": 25, "time": "1 day ago"}
    ]
    
    st.markdown(f"""
    <h4>{get_icon_html('clock', ICON_SIZES['md'])} Recent Backers</h4>
    """, unsafe_allow_html=True)
    
    for backer in recent_backers:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 10px; margin: 5px 0; background: #f8f9fa; border-radius: 5px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                {get_icon_html('person-circle', 20, '#4CAF50')}
                <span style="font-weight: 500;">{backer['name']}</span>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 500; color: #4CAF50;">${backer['amount']}</div>
                <div style="font-size: 12px; color: #666;">{backer['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Helper functions
def validate_campaign_data(title: str, category: str, description: str, funding_goal: float) -> bool:
    """Validate campaign creation data."""
    return (title and len(title) >= 5 and 
            category and 
            description and len(description) >= 50 and 
            funding_goal >= 100)

# Main campaign workflow function
def run_campaign_workflow():
    """Main function to run campaign workflow."""
    if 'campaign_page' not in st.session_state:
        st.session_state.campaign_page = 'browse'
    
    # Navigation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if icon_button('search', 'Browse', 'nav_browse', ICON_SIZES['sm']):
            st.session_state.campaign_page = 'browse'
    with col2:
        if icon_button('plus-circle-fill', 'Create', 'nav_create', ICON_SIZES['sm']):
            st.session_state.campaign_page = 'create'
    with col3:
        if icon_button('speedometer2', 'Dashboard', 'nav_dashboard', ICON_SIZES['sm']):
            st.session_state.campaign_page = 'dashboard'
    with col4:
        if icon_button('eye', 'View Details', 'nav_details', ICON_SIZES['sm']):
            st.session_state.campaign_page = 'details'
    
    # Render appropriate page
    if st.session_state.campaign_page == 'browse':
        render_campaign_browse_page()
    elif st.session_state.campaign_page == 'create':
        render_campaign_creation_form()
    elif st.session_state.campaign_page == 'dashboard':
        render_campaign_management_dashboard()
    elif st.session_state.campaign_page == 'details':
        render_campaign_details_page(1)  # Sample campaign ID

