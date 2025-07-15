import requests
import datetime

# === Supabase Configuration ===
SUPABASE_URL = "https://bkujhyehrlmpnzpwnxzu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrdWpoeWVocmxtcG56cHdueHp1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1NDYyNjcsImV4cCI6MjA2ODEyMjI2N30.a6ZM1AiV_Qhce22axLhyMwYGbC_S0YXksXn0Q-0_WMI"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# === Insert or retrieve company by domain ===
def insert_company(data):
    # Step 1: Check if the company already exists (by domain)
    get_response = requests.get(
        f"{SUPABASE_URL}/rest/v1/companies",
        headers=HEADERS,
        params={
            "domain": f"eq.{data['domain']}",
            "select": "id"
        }
    )
    get_response.raise_for_status()
    results = get_response.json()

    if results:
        # Company already exists
        return results[0]["id"]
    else:
        # Insert new company
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/companies",
            headers=HEADERS,
            json=data
        )
        response.raise_for_status()

        # Fetch most recently inserted row
        confirm_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/companies",
            headers=HEADERS,
            params={"select": "id", "order": "id.desc", "limit": 1}
        )
        confirm_response.raise_for_status()
        return confirm_response.json()[0]["id"]

# === Insert job ===
def insert_job(data):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/jobs",
        headers=HEADERS,
        json=data
    )
    response.raise_for_status()
    return response.status_code

# === Example Data ===
company_data = {
    "name": "Notion Labs, Inc.",
    "website": "https://www.notion.so",
    "domain": "notion.so",
    "industry": "Productivity Software",
    "city": "San Francisco",
    "state": "CA",
    "postal_code": "94103",
    "employees": 600,
    "annual_revenue": None,
    "linkedin_url": "https://www.linkedin.com/company/notionhq"
}

job_data = {
    "job_title": "Head of Global Account Based Marketing",
    "job_board_url": "https://www.builtinsf.com/job/global-abm-lead/4012184",
    "company_job_board_url": "https://www.notion.so/careers",
    "salary_min": None,
    "salary_max": None,
    "job_description_url": "Not found on company site",
    "research": True,
    "created_at": datetime.datetime.now().isoformat()
}

# === Run It ===
if __name__ == "__main__":
    company_id = insert_company(company_data)
    job_data["company_id"] = company_id
    result = insert_job(job_data)
    print("✅ Job inserted successfully with status code:", result)