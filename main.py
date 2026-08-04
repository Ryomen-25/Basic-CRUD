from fastapi import FastAPI

app = FastAPI(root_path="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": "example"}