from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class ProposalCreate(BaseModel):
    valentine_name: str = Field(..., min_length=1, max_length=100)
    custom_message: Optional[str] = Field(default="Will you be my Valentine?", max_length=500)
    character_choice: str = Field(default="panda")  # panda, bear, bunny

class ProposalResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    valentine_name: str
    custom_message: str
    character_choice: str
    created_at: str
    accepted: Optional[bool] = None
    accepted_at: Optional[str] = None

class ProposalUpdate(BaseModel):
    accepted: bool

class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Proposal endpoints
@api_router.post("/proposals", response_model=ProposalResponse)
async def create_proposal(input: ProposalCreate):
    proposal_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    
    doc = {
        "id": proposal_id,
        "valentine_name": input.valentine_name,
        "custom_message": input.custom_message or "Will you be my Valentine?",
        "character_choice": input.character_choice,
        "created_at": created_at,
        "accepted": None,
        "accepted_at": None
    }
    
    await db.proposals.insert_one(doc)
    
    return ProposalResponse(
        id=proposal_id,
        valentine_name=doc["valentine_name"],
        custom_message=doc["custom_message"],
        character_choice=doc["character_choice"],
        created_at=created_at,
        accepted=None,
        accepted_at=None
    )

@api_router.get("/proposals/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(proposal_id: str):
    proposal = await db.proposals.find_one({"id": proposal_id}, {"_id": 0})
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return ProposalResponse(**proposal)

@api_router.patch("/proposals/{proposal_id}", response_model=ProposalResponse)
async def update_proposal(proposal_id: str, update: ProposalUpdate):
    proposal = await db.proposals.find_one({"id": proposal_id}, {"_id": 0})
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    accepted_at = datetime.now(timezone.utc).isoformat() if update.accepted else None
    
    await db.proposals.update_one(
        {"id": proposal_id},
        {"$set": {"accepted": update.accepted, "accepted_at": accepted_at}}
    )
    
    proposal["accepted"] = update.accepted
    proposal["accepted_at"] = accepted_at
    
    return ProposalResponse(**proposal)

@api_router.get("/proposals", response_model=List[ProposalResponse])
async def list_proposals():
    proposals = await db.proposals.find({}, {"_id": 0}).to_list(1000)
    return [ProposalResponse(**p) for p in proposals]

# Root endpoint
@api_router.get("/")
async def root():
    return {"message": "Valentine Proposal API"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
