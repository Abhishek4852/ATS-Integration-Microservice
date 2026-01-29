import requests
import sys

def get_refresh_token(client_id, client_secret, grant_code, redirect_uri, token_url):
    """
    Exchanges a Zoho Grant Token (Authorization Code) for an Access Token and Refresh Token.
    """
    payload = {
        "code": grant_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    
    print(f"Exchanging grant code at: {token_url}")
    try:
        response = requests.post(token_url, params=payload)
        response.raise_for_status()
        data = response.json()
        
        if "refresh_token" in data:
            print("\n" + "="*50)
            print("SUCCESS: Refresh Token Obtained!")
            print("="*50)
            print(f"Refresh Token: {data['refresh_token']}")
            print(f"Access Token:  {data['access_token']}")
            print("="*50)
            print("\nAdd this refresh token to your .env file.")
        else:
            print("\n" + "!"*50)
            print("ERROR: Could not find refresh token in response.")
            print("Response:", data)
            print("!"*50)
            
    except requests.exceptions.RequestException as e:
        print(f"\nAPI Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print("Response:", e.response.text)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 scripts/get_zoho_token.py <CLIENT_ID> <CLIENT_SECRET> <GRANT_CODE> <REDIRECT_URI> [TOKEN_URL]")
        print("\nExample:")
        print("python3 scripts/get_zoho_token.py 1000.XXXX 5789XXXX YYYY https://your-redirect.com")
        sys.exit(1)
        
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    grant_code = sys.argv[3]
    redirect_uri = sys.argv[4]
    token_url = sys.argv[5] if len(sys.argv) > 5 else "https://accounts.zoho.com/oauth/v2/token"
    
    get_refresh_token(client_id, client_secret, grant_code, redirect_uri, token_url)
