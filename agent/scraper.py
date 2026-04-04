import json
from playwright.sync_api import sync_playwright

def run_scraper():
    with sync_playwright() as p:
        # Launching with a real User-Agent is the first "Anti-Detection" step
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # PART B EVIDENCE: Intercepting the internal API instead of the DOM
        def handle_response(response):
            if "/api/v1/applicants" in response.url and response.status == 200:
                print(f"DEBUG: Intercepted JSON from {response.url}")
                data = response.json()
                with open("data/candidates.json", "w") as f:
                    json.dump(data, f)

        page.on("response", handle_response)
        
        # Navigate to login (You will need to manually solve the first CAPTCHA if it appears)
        # Set timeout to 60 seconds and wait for 'networkidle' to ensure data is loaded
        page.goto("https://internshala.com/login/employer", timeout=60000, wait_until="networkidle")
        print("ACTION REQUIRED: Log in manually in the browser window to bypass initial security.")
        
        # Wait for the dashboard to load the applicant XHR
        # Wait a long time (5 minutes) for YOU to log in and reach the applicants page
        print("Waiting for you to reach the Applicants list...")
        page.wait_for_timeout(300000) 
        browser.close()
if __name__ == "__main__":
    run_scraper()