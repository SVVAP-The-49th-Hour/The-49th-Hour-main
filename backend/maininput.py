import os
from dotenv import load_dotenv
from supabase import create_client
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, HTTPException

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()


class Project(BaseModel):
    id: str
    title: str
    hackathon: str
    track_domain: str
    description: str
    tech_stack: List[str]
    status: str
    stall_reason: str
    status_details: str
    original_repo: str
    open_for_collaboration: bool
    contact_method: str


@app.get("/")
def home():
    return {
        "message": "Hackathon backend is running"
    }


@app.get("/projects")
def get_projects():
    response = supabase.table("projects").select("*").execute()

    return {
        "projects": response.data
    }


@app.post("/projects")
def add_project(project: Project):
    response = supabase.table("projects").insert(
        project.model_dump()
    ).execute()

    return {
        "message": "Project added successfully",
        "project": response.data
    }

@app.get("/projects/{project_id}")
def get_project(project_id: str):
    response = supabase.table("projects").select("*").eq("id", project_id).execute()

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "project": response.data[0]
    }