#!/usr/bin/env python
"""
Test script for Google OAuth authentication flow for reporters.

This script demonstrates how to use the Google OAuth flow for reporter authentication.
"""

import requests
import json
import webbrowser
from urllib.parse import urlencode

# Backend server URL
BASE_URL = 'http://localhost:8000'

def main():
    print("Google OAuth Authentication Flow for Reporters")
    print("=============================================")
    
    # Step 1: Redirect user to Google OAuth login page
    # In a real frontend application, this would be done by redirecting the user's browser
    auth_params = {
        'client_id': 'YOUR_GOOGLE_CLIENT_ID',  # Replace with your Google OAuth client ID
        'redirect_uri': f'{BASE_URL}/auth/complete/google-oauth2/',
        'response_type': 'code',
        'scope': 'email profile',
    }
    
    auth_url = f'https://accounts.google.com/o/oauth2/auth?{urlencode(auth_params)}'
    
    print(f"\n1. Open this URL in your browser to start the Google OAuth flow:")
    print(f"{auth_url}")
    print("\nAfter successful authentication, you will be redirected back to your application.")
    print("The redirect URL will contain a 'code' parameter that would be exchanged for a token.")
    
    print("\n2. In a real application, the frontend would:")
    print("   - Redirect the user to the Google OAuth URL")
    print("   - Receive the authorization code from the redirect")
    print("   - Send this code to the backend")
    
    print("\n3. The backend would then:")
    print("   - Exchange the code for tokens using the /auth/complete/google-oauth2/ endpoint")
    print("   - Create a new user with REPORTER role if they don't exist")
    print("   - Return a token for API authentication")
    
    print("\n4. Example API usage with the token:")
    print("   GET /api/issues/ - List issues (reporters see only their own)")
    print("   POST /api/issues/ - Create a new issue")
    
    print("\nNOTE: To complete this flow, you need to:")
    print("1. Register your application with Google Developer Console")
    print("2. Set the SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET in settings.py")
    print("3. Configure the authorized redirect URIs in Google Developer Console")

if __name__ == "__main__":
    main()
