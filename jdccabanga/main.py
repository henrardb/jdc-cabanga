#!/usr/bin/env python3

import requests
import json
import os
import sys
from datetime import date, timedelta
from jdccabanga.models import Lesson
from .auth_manager import refresh_access_token
from .notifier import send_daily_report


SCHOOL_CODE = os.getenv("SCHOOL_CODE")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
STUDENT_ID = os.getenv("STUDENT_ID")

TODAY = date(2025, 11, 17)
END_DATE = TODAY + timedelta(days=14)

DIARY_URL = (
    f"https://api.scolares.be/cabanga/api/schools/{SCHOOL_CODE}/students/{STUDENT_ID}/diary"
    f"?from={TODAY.isoformat()}&to={END_DATE.isoformat()}"
)


def get_diary_data(token: str, url: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    }

    print(f"-> Connexion to API: {DIARY_URL}")

    try:
        response = requests.get(url, headers=headers, timeout=10)

        response.raise_for_status()

        print(f"Success: {response.status_code}")
        return response.json()

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP error: {errh}")
        if response.status_code == 401 or response.status_code == 403:
            print("   Access token expired or invalid.")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return None


if __name__ == "__main__":
    # Check if environment variable REFRESH_TOKEN exists, leave otherwize
    if not REFRESH_TOKEN:
        print("Environment variable REFRESH_TOKEN does not exist")
        sys.exit(1)

    try:
        # Get access and refresh token
        new_tokens = refresh_access_token(REFRESH_TOKEN)
        access_token = new_tokens['access_token']
        new_refresh_token = new_tokens['refresh_token']

        data = get_diary_data(access_token, DIARY_URL)

        if data:
            # diary_entries = [Lesson(**item) for item in data]
            report_content = json.dumps(data, indent=2, ensure_ascii=False)
            send_daily_report(report_content)


    except Exception as e:
        print(f"Main - General failure: {e}")
        sys.exit(1)
