from fastapi import FastAPI, HTTPException
from agent.brain import HiringBrain
import os

app = FastAPI(title="GenoTek Autonomous Hiring Agent")

@app.get("/rank")
def rank_candidates():
    if not os.path.exists("data/candidates.json"):
        raise HTTPException(status_code=404, detail="No candidate data captured yet.")
    
    brain = HiringBrain()
    top_2 = brain.get_top_candidates()
    return {"status": "success", "top_picks": top_2}

@app.post("/trigger-agent")
def start_agent():
    # This would trigger the scraper.py script
    return {"message": "Agent dispatched to Internshala portal."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)