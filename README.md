# GenoTek Hiring Agent Challenge

## A. Architecture
1. **Access:** Playwright (Python) with Network Interception (`page.on("response")`).
2. **Intelligence:** Custom Scoring Engine in `brain.py` using technical-depth heuristics and AI-spam markers.
3. **API:** FastAPI wrapper to serve ranked candidates.

## B. Technical "Scars" & Evidence
During the 2-hour sprint, I encountered and logged:
- **Environment Issues:** Resolved Playwright binary path errors.
- **WAF/Cloudflare:** Handled 403/Timeout errors by tuning browser contexts.
- **Google OAuth Wall:** Identified that Google blocks automated Chromium. In production, I would utilize a **Remote Browser Isolation (RBI)** service or a **Persistent Chrome Profile** to maintain the session.

## C. Setup
1. `pip install -r requirements.txt`
2. `python -m uvicorn agent.server:app --reload`
3. Hit `localhost:8000/rank` to see the Intelligence Layer in action.