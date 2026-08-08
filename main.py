from fastapi import FastAPI, HTTPException , Request
from datetime import datetime
from typing import Any
from random import randint

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

@app.post("/campaigns")
async def create_campaign(body: dict[str, Any]):
    
    
    new : Any = {
        "campaign_id": randint(100,1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": body.get("created_at")
    }
    # add the new campaign data
    data.append(new)
    
    return {"campaign": new}