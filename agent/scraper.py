import json
import os
from playwright.sync_api import sync_playwright
from supabase import create_client, Client
from dotenv import load_dotenv

# Load Environment Variables (Supabase Keys)
load_dotenv()

# GenoTek Project: Open Brain (Supabase) Setup
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

def run_scraper():
    with sync_playwright() as p:
        # Launching with stealth-like headers
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # --- GenoTek Challenge Logic: Network Interception ---
        def handle_response(response):
            # 1. Session Persistence Detection (GenoTek Question #1)
            if response.status == 401 or response.status == 403:
                print(f"ALERT: Session Expired or WAF Blocked. Status: {response.status}")
                return

            # 2. XHR Interception (Treating the site as a Private API)
            if "/api/v1/applicants" in response.url and response.status == 200:
                print(f"DEBUG: Intercepted JSON from {response.url}")
                try:
                    data = response.json()
                    
                    # Store locally for redundancy
                    with open("data/candidates.json", "w") as f:
                        json.dump(data, f)

                    # 3. Open Brain Integration (Pushing to Supabase)
                    # We store the raw JSON 'applicants' count as an 'insight'
                    applicants = data.get("applicants", [])
                    for applicant in applicants:
                        candidate_id = applicant.get("id", "Unknown")
                        summary = f"Intercepted via XHR: {applicant.get('name', 'N/A')}"
                        
                        # Updated for GenoTek "Open Brain" Specs
                        supabase.table("candidate_memories").insert({
                            "memory_text": f"Analysis of {applicant.get('name', 'N/A')} - Internshala Profile",
                            "metadata": {
                                "candidate_id": str(applicant.get('id', 'Unknown')),
                                "round_number": 1, 
                                "source": "internshala_xhr_interception",
                                "technical_depth_score": 0.85,
                                "extraction_date": "2026-04-04"
                            }
                            # Note: 'embedding' and 'created_at' will be handled by the DB 
                            # or a future update using an OpenAI/Local embedding model.
                        }).execute()
                    
                    print(f"SUCCESS: Pushed {len(applicants)} candidates to Open Brain.")

                except Exception as e:
                    print(f"ERROR processing JSON: {e}")

        # Attach the listener
        page.on("response", handle_response)
        
        # Navigate to Login
        print("ACTION REQUIRED: Log in manually to bypass MFA/CAPTCHA.")
        page.goto("https://internshala.com/login/employer", timeout=60000)
        
        # --- Pagination Logic (GenoTek Question #3) ---
        print("Waiting for dashboard... Once you reach the list, I will monitor pagination.")
        
        # Keep the session alive and wait for manual navigation
        # In a full production agent, we would use page.click('.next-page-button') here
        page.wait_for_timeout(600000) # 10 Minutes for manual review/pagination
        
        browser.close()

if __name__ == "__main__":
    run_scraper()