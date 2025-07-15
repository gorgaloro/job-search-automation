import os
import requests
import datetime
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HUBSPOT_TOKEN = os.getenv("HUBSPOT_TOKEN")

SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# === Insert or retrieve company by domain ===
def insert_company(data):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/companies",
        headers=SUPABASE_HEADERS,
        params={"domain": f"eq.{data['domain']}", "select": "id"}
    )
    response.raise_for_status()
    results = response.json()

    if results:
        return results[0]["id"]
    else:
        insert_response = requests.post(
            f"{SUPABASE_URL}/rest/v1/companies",
            headers=SUPABASE_HEADERS,
            json=data
        )
        insert_response.raise_for_status()

        confirm = requests.get(
            f"{SUPABASE_URL}/rest/v1/companies",
            headers=SUPABASE_HEADERS,
            params={"select": "id", "order": "id.desc", "limit": 1}
        )
        confirm.raise_for_status()
        return confirm.json()[0]["id"]

# === Insert job ===
def insert_job(data):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/jobs",
        headers=SUPABASE_HEADERS,
        json=data
    )
    response.raise_for_status()
    return response.status_code

# === Insert into HubSpot ===
def insert_hubspot_company(data, job_data):
    headers = {
        "Authorization": f"Bearer {HUBSPOT_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "properties": {
            "name": data["name"],
            "website": data["website"],
            "domain": data["domain"],
            "city": data["city"],
            "state": data["state"],
            "postal_code": data["postal_code"],
            "industry": data["industry"],
            "linkedin_url": data["linkedin_url"],
            "description": data.get("description", ""),  # ✅ NEW FIELD
            "job_board_url": job_data["company_job_board_url"],
            "research": "true"
        }
    }

    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/companies",
        headers=headers,
        json=payload
    )

    if response.status_code >= 400:
        print("❌ HubSpot Error:", response.status_code)
        print("❌ HubSpot Message:", response.text)
    else:
        print("✅ HubSpot Success:", response.status_code)
        print("✅ HubSpot Response:", response.json())

# === Cedars-Sinai example ===
company_data = {
    "name": "Cedars-Sinai Medical Center",
    "website": "https://www.cedars-sinai.org",
    "domain": "cedars-sinai.org",
    "industry": "Healthcare",
    "city": "Los Angeles",
    "state": "CA",
    "postal_code": "90048",
    "employees": 14000,
    "annual_revenue": None,
    "linkedin_url": "https://www.linkedin.com/company/cedars-sinai",
    "description": "Cedars-Sinai is a nonprofit academic healthcare organization serving the diverse Los Angeles community and beyond with leadership in medical education, biomedical research, and patient care."  # ✅ NEW FIELD
}

job_data = {
    "job_title": "IT Project Manager",
    "job_board_url": "https://careers.cedars-sinai.edu/jobs/IT-Project-Manager",
    "company_job_board_url": "https://careers.cedars-sinai.edu/",
    "salary_min": None,
    "salary_max": None,
    "job_description_url": "https://careers.cedars-sinai.edu/jobs/IT-Project-Manager",
    "research": True,
    "created_at": datetime.datetime.now().isoformat()
}

# === Run it all ===
if __name__ == "__main__":
    company_id = insert_company(company_data)
    job_data["company_id"] = company_id
    result = insert_job(job_data)
    print("✅ Job inserted to Supabase:", result)
    insert_hubspot_company(company_data, job_data)