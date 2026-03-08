"""
Test Gmail API Credentials

This script verifies your Gmail API credentials are set up correctly
without starting the full watcher.
"""

import os
import sys
from pathlib import Path
import json

def test_credentials():
    """Test if Gmail credentials are properly configured"""

    print("=" * 60)
    print("Gmail API Credentials Test")
    print("=" * 60)
    print()

    # Check credentials file
    creds_path = Path(__file__).parent / "credentials" / "gmail_credentials.json"
    print(f"1. Checking credentials file...")
    print(f"   Location: {creds_path}")

    if not creds_path.exists():
        print("   [FAIL] Credentials file not found")
        print()
        print("   Next steps:")
        print("   1. Go to https://console.cloud.google.com/")
        print("   2. Create a new project")
        print("   3. Enable Gmail API")
        print("   4. Create OAuth 2.0 credentials (Desktop app)")
        print("   5. Download JSON and save as:")
        print(f"      {creds_path}")
        print()
        print("   See credentials/README.md for detailed instructions")
        return False

    print("   [OK] Credentials file exists")

    # Validate JSON structure
    print()
    print(f"2. Validating JSON structure...")

    try:
        with open(creds_path, 'r') as f:
            creds_data = json.load(f)

        # Check for required fields
        if 'installed' in creds_data:
            client_config = creds_data['installed']
        elif 'web' in creds_data:
            print("   [WARN] Found 'web' credentials, need 'installed' (Desktop app)")
            print("   Please create OAuth credentials for 'Desktop app' type")
            return False
        else:
            print("   [FAIL] Invalid credentials format")
            return False

        required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
        missing_fields = [f for f in required_fields if f not in client_config]

        if missing_fields:
            print(f"   [FAIL] Missing fields: {', '.join(missing_fields)}")
            return False

        print("   [OK] JSON structure is valid")
        print(f"   Client ID: {client_config['client_id'][:20]}...")

    except json.JSONDecodeError as e:
        print(f"   [FAIL] Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"   [FAIL] Error reading file: {e}")
        return False

    # Check for token file
    print()
    print(f"3. Checking authentication token...")
    token_path = Path(__file__).parent / "credentials" / "gmail_token.json"

    if not token_path.exists():
        print("   [WARN] Token not found (expected on first run)")
        print()
        print("   Next step: Run the watcher to authenticate:")
        print("   python gmail_watcher.py")
        print()
        print("   A browser will open for you to sign in and authorize access.")
        return True  # Credentials are valid, just need to authenticate

    print("   [OK] Token file exists")

    # Try to load token
    try:
        with open(token_path, 'r') as f:
            token_data = json.load(f)

        if 'token' in token_data or 'access_token' in token_data:
            print("   [OK] Token structure is valid")
        else:
            print("   [WARN] Token may be invalid, might need re-authentication")
    except Exception as e:
        print(f"   [WARN] Could not validate token: {e}")

    # Check Python dependencies
    print()
    print(f"4. Checking Python dependencies...")

    try:
        import google.auth
        print("   [OK] google-auth installed")
    except ImportError:
        print("   [FAIL] google-auth not installed")
        print("   Run: pip install google-auth google-auth-oauthlib google-auth-httplib2")
        return False

    try:
        import googleapiclient
        print("   [OK] google-api-python-client installed")
    except ImportError:
        print("   [FAIL] google-api-python-client not installed")
        print("   Run: pip install google-api-python-client")
        return False

    # Final summary
    print()
    print("=" * 60)
    print("[SUCCESS] ALL CHECKS PASSED")
    print("=" * 60)
    print()

    if not token_path.exists():
        print("Ready for first-time authentication!")
        print("Run: python gmail_watcher.py")
    else:
        print("Gmail API is fully configured and ready to use!")
        print("Run: python gmail_watcher.py")

    return True

if __name__ == "__main__":
    try:
        success = test_credentials()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
