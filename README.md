# HAVEN Crowdfunding Platform - Frontend

A modern and intuitive Streamlit frontend for the HAVEN crowdfunding platform with OAuth authentication, campaign management, and multilingual support.

## Features

- **User Authentication**: Secure login with email/password and OAuth (Google, Facebook)
- **Campaign Management**: Create, view, and manage crowdfunding campaigns
- **Donation System**: Easy and secure donation process
- **Translation Support**: Multi-language content translation
- **Text Simplification**: Simplify complex terms for better understanding
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Live campaign progress tracking
- **User Dashboard**: Comprehensive user profile and statistics
- **Search and Filtering**: Advanced campaign discovery
- **Social Sharing**: Share campaigns on social media

## Technology Stack

- **Framework**: Streamlit 1.28.1
- **HTTP Client**: Requests/HTTPX for API communication
- **Authentication**: JWT with OAuth2 integration
- **Visualization**: Plotly for charts and graphs
- **Styling**: Custom CSS with responsive design
- **Deployment**: Docker with cloud platform support

## Quick Start

### Prerequisites

- Python 3.11+
- HAVEN Backend API running

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fixed_frontend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start the application**
   ```bash
   streamlit run app.py
   ```

The application will be available at `http://localhost:8501`

## Configuration

### Environment Variables

Key environment variables (see `.env.example` for complete list):

- `BACKEND_URL`: Backend API URL (e.g., `http://localhost:8000`)
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `FACEBOOK_APP_ID`: Facebook OAuth app ID
- `ENABLE_OAUTH`: Enable OAuth authentication
- `ENABLE_TRANSLATION`: Enable translation features
- `ENABLE_FRAUD_DETECTION`: Enable fraud detection features

### Backend Integration

The frontend communicates with the HAVEN backend API. Ensure the backend is running and accessible at the URL specified in `BACKEND_URL`.

## Application Structure

### Main Components

#### Pages
- **Home**: Landing page with featured campaigns and platform statistics
- **Login**: User authentication with email/password and OAuth
- **Register**: User registration with email verification
- **Dashboard**: User profile, statistics, and quick actions
- **Campaigns**: Browse and search campaigns with filtering
- **Profile**: User profile management and settings

#### Utilities
- **API Client**: Handles all backend API communication
- **Auth Utils**: Authentication and session management
- **Config Manager**: Environment and configuration management

### Code Structure
```
fixed_frontend/
├── app.py                # Main Streamlit application
├── pages/               # Page modules
│   ├── __init__.py
│   ├── home.py          # Home page
│   ├── login.py         # Login page
│   ├── register.py      # Registration page
│   ├── dashboard.py     # User dashboard
│   ├── campaigns.py     # Campaign pages
│   └── profile.py       # User profile
├── utils/               # Utility modules
│   ├── __init__.py
│   ├── api_client.py    # API communication
│   ├── auth_utils.py    # Authentication utilities
│   └── config.py        # Configuration management
├── .streamlit/          # Streamlit configuration
│   └── config.toml      # Streamlit settings
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
└── .env.example        # Environment template
```

## Features Guide

### Authentication

#### Email/Password Login
1. Navigate to Login page
2. Enter email and password
3. Click "Sign In"

#### OAuth Login
1. Navigate to Login page
2. Click "Continue with Google" or "Continue with Facebook"
3. Complete OAuth flow in popup window
4. Automatic redirect after successful authentication

### Campaign Management

#### Creating a Campaign
1. Login to your account
2. Click "Create Campaign" in sidebar
3. Fill in campaign details:
   - Title and description
   - Goal amount
   - Category
   - Organization details (if applicable)
4. Upload images and videos
5. Submit for review

#### Browsing Campaigns
1. Navigate to Campaigns page
2. Use filters to narrow down results:
   - Category
   - Status
   - Search terms
3. Click on campaigns to view details
4. Donate to campaigns you support

### User Dashboard

#### Profile Management
- Update personal information
- Change password
- Manage KYC documents
- View account statistics

#### Campaign Tracking
- View your created campaigns
- Track donation history
- Monitor campaign performance
- Manage campaign updates

### Translation and Simplification

#### Text Translation
- Available on campaign pages
- Translate content to your preferred language
- Support for multiple languages

#### Term Simplification
- Hover over complex terms to see simplified explanations
- Available for financial, legal, technical, and medical terms
- Helps improve understanding of campaign content

## API Integration

### Authentication Flow
1. User logs in via frontend
2. Frontend receives JWT tokens from backend
3. Tokens stored in session state
4. All API requests include authentication headers
5. Automatic token refresh when needed

### Error Handling
- Network errors with retry logic
- Authentication errors with automatic logout
- Validation errors with user-friendly messages
- Rate limiting with appropriate feedback

## Deployment

### Docker Deployment

1. **Build image**
   ```bash
   docker build -t haven-frontend .
   ```

2. **Run container**
   ```bash
   docker run -p 8501:8501 --env-file .env haven-frontend
   ```

### Cloud Deployment (Render)

1. **Connect repository** to Render
2. **Set environment variables** in Render dashboard
3. **Deploy** with build command: `pip install -r requirements.txt`
4. **Start command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Environment Variables for Production

Required environment variables for deployment:
```
BACKEND_URL=https://your-backend-domain.com
GOOGLE_CLIENT_ID=...
FACEBOOK_APP_ID=...
ENABLE_OAUTH=true
ENABLE_TRANSLATION=true
ENABLE_FRAUD_DETECTION=true
```

## Customization

### Theming
Edit `.streamlit/config.toml` to customize:
- Primary colors
- Background colors
- Font styles
- Layout options

### Features
Use environment variables to enable/disable features:
- `ENABLE_OAUTH`: OAuth authentication
- `ENABLE_TRANSLATION`: Translation services
- `ENABLE_FRAUD_DETECTION`: Fraud detection
- `ENABLE_ANALYTICS`: Usage analytics

## Development

### Running in Development Mode
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
streamlit run app.py --server.runOnSave true
```

### Adding New Pages
1. Create new page module in `pages/` directory
2. Implement `render_page_name(api_client)` function
3. Add page to navigation in `app.py`
4. Update routing logic

### Adding New Features
1. Update API client with new endpoints
2. Create UI components for new features
3. Add configuration options if needed
4. Update documentation

## Performance Optimization

### Caching
- API responses cached using Streamlit caching
- User session data cached in session state
- Static content cached by browser

### Loading Optimization
- Lazy loading of page content
- Pagination for large datasets
- Optimized image loading
- Minimal API calls

## Security Considerations

- **Token Storage**: JWT tokens stored in session state only
- **HTTPS Only**: Force HTTPS in production
- **Input Validation**: Client-side validation for better UX
- **Error Handling**: Secure error messages without sensitive data
- **Session Management**: Automatic logout on token expiry

## Troubleshooting

### Common Issues

#### Backend Connection Error
- Check `BACKEND_URL` in environment variables
- Ensure backend is running and accessible
- Verify CORS configuration in backend

#### OAuth Login Issues
- Verify OAuth client IDs in environment variables
- Check OAuth redirect URIs in provider settings
- Ensure popup blockers are disabled

#### Session Expiry
- Tokens automatically refresh when possible
- Manual re-login required if refresh fails
- Clear browser cache if issues persist

### Debug Mode
Enable debug mode by setting `DEBUG=true` in environment variables for additional logging and error details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: support@haven.org
- Documentation: [Backend API Docs](http://localhost:8000/docs)
- Issues: GitHub Issues

## Changelog

### v1.0.0
- Initial release
- Core authentication and campaign browsing
- OAuth integration (Google, Facebook)
- User dashboard and profile management
- Translation and simplification features
- Responsive design and mobile support

