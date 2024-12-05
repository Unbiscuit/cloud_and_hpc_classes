import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4, UUID
from fastapi.middleware.cors import CORSMiddleware


MONGODB_CONNECTION_STRING = os.environ["MONGODB_CONNECTION_STRING"]

client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING, uuidRepresentation="standard")
db = client.shlist
shl = db.shl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    content: str


class  ItemCreate(BaseModel):
    content: str


@app.post("/shl", response_model=Item)
async def create_item(item: ItemCreate):
    new_item = Item(content=item.content)
    await shl.insert_one(new_item.model_dump(by_alias=True))
    return new_item

@app.get("/shl", response_model=list[Item])
async def read_shl():
    return await shl.find().to_list(length=None)

@app.delete("/shl/{sh_id}")
async def delete_item(sh_id: UUID):
    delete_result = await shl.delete_one({"_id": sh_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted successfully"}
