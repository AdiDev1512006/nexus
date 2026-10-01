from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.command_processor import process_command

app = FastAPI(title="NEXUS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    command: str

@app.get("/")
def root():
    return {
        "system": "NEXUS",
        "status": "online"
    }

@app.get("/status")
def status():
    return {
        "system": "NEXUS",
        "status": "online"
    }

@app.post("/command")
def command(request: CommandRequest):
    response = process_command(request.command)
    return {
        "command": request.command,
        "response": response
    }