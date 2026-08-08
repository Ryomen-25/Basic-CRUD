from fastapi import FastAPI, HTTPException , Request , Response , Depends
from datetime import datetime
from typing import Any , Annotated
from random import randint
from sqlmodel import SQLModel ,create_engine, Session

sqllite_file_name = "database.db"
sqllite_url = f"sqllite:///{sqllite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqllite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session   
        
SessionDep = Annotated[Session, Depends(get_session)]
        

    
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

# Create campaign endpoint
@app.post("/campaigns", status_code=201)
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

#Update campaign data endpoint
@app.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):
    
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            
            updated : Any = {
                "campaign_id": id,
                "name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get("created_at")
            }
            
            data[index] = updated
            return {"campaign": updated}
    
    raise HTTPException(status_code=404)


# Delete campaign endpoint
@app.delete("/campaigns/{id}")
async def delete_campaign(id: int):
    
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            data.pop(index)
            
            return Response(status_code=204)
    
    raise HTTPException(status_code=404)