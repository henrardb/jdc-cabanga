import requests

TOKEN_URL = "https://login.scolares.be/auth/realms/horizon/protocol/openid-connect/token"
CLIENT_ID = "cabanga-frontend"


def refresh_access_token(current_refresh_token: str):
    print("-> Try token refresh...")

    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": current_refresh_token,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(TOKEN_URL, data=payload, headers=headers, timeout=10)
        response.raise_for_status()

        token_data = response.json()

        if "access_token" in token_data and "refresh_token" in token_data:
            print("Refresh token success.")
            return {
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_in": token_data.get("expires_in")
            }
        raise ValueError("Wrong response token.")

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Refresh token failed: {e}")
