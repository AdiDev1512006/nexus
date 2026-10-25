from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, field_validator
from core.command_processor import process_command

app = FastAPI(title="NEXUS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validate incoming command requests
class CommandRequest(BaseModel):
    command: str = Field(
        min_length=1,
        max_length=200,
        description="The command entered by the user.."
    )
    @field_validator("command")
    @classmethod
    
    def validate_command(cls, value: str) -> str:
        value = value.strip()
        if not value :
            raise ValueError("Command cannot be empty or whitespace only.")
        return value

# Return a consistent response when request validation fails
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "error": "Invalid request",
            "details": exc.errors()
        })
    )

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
    return process_command(request.command)