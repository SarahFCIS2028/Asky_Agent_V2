from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from Core_Agent.main import run_agent

app=FastAPI(  title="Wiki Research API",
    description="Interactive AI Research Assistant",)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str
    mode: str = "beginner"

@app.get("/")
async def root():
    return{"message":"api is working"}

@app.post("/asky")
async def research(request: ResearchRequest):
    try:
        result = await run_agent(
            topic=request.topic,
            mode=request.mode
        )
        return result

    except Exception as e:
        print("🔥 ERROR:", repr(e))
        raise
# @app.post("/asky")
# async def research(request:ResearchRequest):
#     result = await run_agent(
#         topic= request.topic,
#         mode= request.mode
#     )
#     return result