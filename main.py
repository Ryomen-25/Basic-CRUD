from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Any

app = FastAPI(root_path="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello"}

data : Any = [
    {
        "campaign_id": 1,
        "name": "Summer Training",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    },     
    {
        "campaign_id": 2,
        "name": "Summer Internship",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    }
]

#  Retrieve all the campaigns data
@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}

# Retrieve the data of single chosen campaign
@app.get("/campaigns/{id}")
async def read_campaign(id: int): 
    for campaign in data:
        if campaign.get("campaign_id") == id:
            return {"campaign": campaign}
    raise HTTPException(status_code=404)

